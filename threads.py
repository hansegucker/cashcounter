import sys
import threading
import time

import rpyc

#################
# EV3 INIT CODE #
#################

# Connect ev3 over rpyc
from const import TRAP_MODE_CLOSED, TRAP_MODE_HALF, TRAP_MODE_OPEN, R_MAX, G_MAX, B_MAX
from help import re_map

conn = rpyc.classic.connect('ev3dev.local')  # host name or IP address of the EV3
ev3 = conn.modules['ev3dev.ev3']  # import ev3dev.ev3 remotely
fonts = conn.modules['ev3dev.fonts']

# Init Motors
band = ev3.LargeMotor('outA')
trap = ev3.LargeMotor('outB')
detecting_motor = ev3.MediumMotor('outD')

# Init Sensors
ir = ev3.InfraredSensor()
ir.mode = 'IR-PROX'
cl = ev3.ColorSensor()
cl.mode = 'RGB-RAW'
ts = ev3.TouchSensor()


# Threading
class TrapLoop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_running = False
        self.running = False

        self.trap_mode = TRAP_MODE_CLOSED
        self.color = (1, 1, 1)
        self.trap_available = True
        self.refresh = self.dummy
        self.band_thread = BandLoop()
        self.band_thread.start()

    def dummy(self):
        pass

    def set_refresh(self, refresh):
        self.refresh = refresh
        self.band_thread.set_refresh(refresh)

    def open_trap_completly(self):
        print(self.trap_mode)
        if self.trap_mode == TRAP_MODE_CLOSED or self.trap_mode == TRAP_MODE_HALF:
            self.open_trap()
            self.refresh()
            time.sleep(0.5)
            self.close_trap()

    def open_trap_half(self):
        if self.trap_mode == TRAP_MODE_CLOSED:
            self.move_trap(-30)
            self.trap_mode = TRAP_MODE_HALF
            print(self.trap_mode)

    def open_trap(self):
        if self.trap_mode == TRAP_MODE_CLOSED:
            self.move_trap(-60)
            self.trap_mode = TRAP_MODE_OPEN
        elif self.trap_mode == TRAP_MODE_HALF:
            self.move_trap(-30)
            print("Minus 30")
            self.trap_mode = TRAP_MODE_OPEN

    def close_trap(self):
        if self.trap_mode == TRAP_MODE_OPEN:
            self.move_trap(59)
            print("PLUS FULL")
            self.trap_mode = TRAP_MODE_CLOSED
        elif self.trap_mode == TRAP_MODE_HALF:
            self.move_trap(30)
            self.trap_mode = TRAP_MODE_CLOSED

    def move_trap(self, deg):
        global trap
        trap.run_to_rel_pos(position_sp=deg, speed_sp=300, stop_action="hold")
        trap.wait_while('running')

    def get_color(self):
        # print(cl.value(0), cl.value(1), cl.value(2))
        r = round(re_map(cl.value(0), 0, R_MAX, 0, 255), 0)
        g = round(re_map(cl.value(1), 0, G_MAX, 0, 255), 0)
        b = round(re_map(cl.value(2), 0, B_MAX, 0, 255), 0)
        return int(r), int(g), int(b)

    def move_detect(self, deg):
        global detecting_motor
        detecting_motor.run_to_rel_pos(position_sp=deg, speed_sp=1000, stop_action="hold")
        detecting_motor.wait_while('running')

    def measure_width(self):
        global detecting_motor, ts
        self.move_detect(2000)
        count = 0
        print(ts.is_pressed)
        while count < 1000 and ts.is_pressed is 0:
            self.move_detect(200)
            print("#", ts.is_pressed)
            print("##", count)
            count += 200
        self.move_detect((count * -1) + -2000)
        return count

    def run(self):
        global cl

        self.thread_running = True
        while self.thread_running:
            while not self.running:
                pass

            if self.running:
                self.band_thread.start_work()
            while self.running:
                # print(cl.value(0), cl.value(1), cl.value(2))
                print(ts.is_pressed)
                self.color = self.get_color()
                # print(self.color)
                # time.sleep(2)
                if not self.trap_available:
                    # Measurement
                    print(self.color)
                    # time.sleep(0.5)
                    self.open_trap_half()
                    # time.sleep(0.2)
                    self.measure_width()
                    self.open_trap_completly()
                    self.trap_available = True

                if self.band_thread.ready_object_on_band and self.trap_available:
                    if self.band_thread.get_object_if_available():
                        self.trap_available = False
                        time.sleep(1)

            self.band_thread.stop_work()
            band.stop(stop_action="hold")

        self.refresh()

    def start_work(self):
        self.running = True

    def stop_work(self):
        self.running = False

    def close(self, code, and_exit=True):
        run = self.thread_running
        print(run)

        # run() beenden
        self.thread_running = False

        # Warten, bis run() beendet ist
        if run:
            self.join()

        # BandThread beenden
        self.band_thread.close()

        # Programm beenden
        if and_exit:
            sys.exit(code)


class BandLoop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_running = True
        self.running = False

        self.band_running = False
        self.band_manual_stopped = False
        self.ready_object_on_band = False
        self.refresh = self.dummy
        self.distance = 0

    def dummy(self):
        pass

    def set_refresh(self, refresh):
        self.refresh = refresh

    def run(self):
        while self.thread_running:
            # Warte solange, bis Band wieder in Betrieb gesetzt wird (von TrapLoop)
            while not self.running:
                pass

            while self.running:
                if not self.ready_object_on_band and not self.band_running and not self.band_manual_stopped:
                    self.start_band(manual=False)

                if not self.ready_object_on_band and self.band_running:
                    self.distance = ir.value()
                    # print(distance)

                    if self.distance < 15:
                        self.stop_band(manual=False)

                        self.ready_object_on_band = True
                self.refresh()

    def get_object_if_available(self):
        if self.ready_object_on_band and not self.band_manual_stopped:
            self.start_band(manual=False)
            time.sleep(1)
            self.ready_object_on_band = False
            return True
        return False

    def start_band(self, x=0, manual=True):
        global band
        if not manual:
            self.band_running = True
        else:
            self.band_manual_stopped = False
        band.run_forever(speed_sp=50)

    def stop_band(self, x=0, manual=True):
        global band
        if not manual:
            self.band_manual_stopped = False
            self.band_running = False
        else:
            self.band_manual_stopped = True

        band.stop(stop_action="hold")

    def start_work(self):
        self.running = True

    def stop_work(self):
        self.running = False

    def close(self):
        run = self.thread_running
        self.thread_running = False
        if run:
            self.join()
