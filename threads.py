import sys
import threading
import time

#################
# EV3 INIT CODE #
#################

# Connect ev3 over rpyc
from ev3.band import Band
from ev3.ev3 import EV3

# Threading
from logic import TrapManagement


class TrapLoop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_running = False  # For thread system (e. g. stop)
        self.running = False

        self.ev3 = EV3()

        self.trap_management = TrapManagement(self.ev3)

        self.color = (1, 1, 1)
        self.refresh = self.dummy
        self.band_thread = BandLoop(ev3=self.ev3)
        self.band_thread.start()

    def dummy(self):
        pass

    def set_refresh(self, refresh):
        self.refresh = refresh
        self.band_thread.set_refresh(refresh)

    def run(self):
        self.thread_running = True
        while self.thread_running:
            # Wait for start by user
            while not self.running:
                pass

            # Start by user, start band
            if self.running:
                self.band_thread.start_work()

            # Start trap
            while self.running:
                # print(cl.value(0), cl.value(1), cl.value(2))
                # print(ts.is_pressed)
                self.color = self.ev3.get_color()
                # print(self.color)
                # time.sleep(2)
                # Check if band has an coin to measure
                if self.band_thread.ready_object_on_band and self.trap_management.trap_available:
                    if self.band_thread.get_object_if_available():
                        # Measure
                        self.trap_management.measure_coin()

            # Stop band
            self.band_thread.stop_work()

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
    def __init__(self, ev3):
        threading.Thread.__init__(self)
        self.thread_running = True
        self.running = False

        self.ev3 = ev3
        self.band = Band(self.ev3)

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
                if not self.ready_object_on_band and not self.band.band_running and not self.band.band_manual_stopped:
                    self.band.start_band(manual=False)

                if not self.ready_object_on_band and self.band.band_running:
                    self.distance = self.ev3.ir.value()
                    # print("[DISTANCE]", self.distance)

                    if self.distance < 15:
                        self.band.stop_band(manual=False)

                        self.ready_object_on_band = True

                # Refresh GUI
                self.refresh()

            # Stop band
            self.ev3.stop_band()

    def get_object_if_available(self):
        if self.ready_object_on_band and not self.band.band_manual_stopped:
            self.band.start_band(manual=False)
            time.sleep(1.5)
            self.ready_object_on_band = False
            return True
        return False

    def start_work(self):
        self.running = True

    def stop_work(self):
        self.running = False

    def close(self):
        run = self.thread_running
        self.thread_running = False
        if run:
            self.join()
