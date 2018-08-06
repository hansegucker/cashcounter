import rpyc

from const import R_MAX, G_MAX, B_MAX
from help import re_map


class EV3():
    def __init__(self):
        self.conn = rpyc.classic.connect('ev3dev.local')  # host name or IP address of the EV3
        self.ev3 = self.conn.modules['ev3dev.ev3']  # import ev3dev.ev3 remotely
        # fonts = self.conn.modules['ev3dev.fonts']

        # Init Motors
        self.band = self.ev3.LargeMotor('outA')
        self.trap = self.ev3.LargeMotor('outB')
        self.measuring_motor = self.ev3.MediumMotor('outD')

        # Init Sensors
        self.ir = self.ev3.InfraredSensor()
        self.ir.mode = 'IR-PROX'
        self.cl = self.ev3.ColorSensor()
        self.cl.mode = 'RGB-RAW'
        self.ts = self.ev3.TouchSensor()

    # MOVER
    def move_trap(self, deg):
        self.trap.run_to_rel_pos(position_sp=deg, speed_sp=300, stop_action="hold")
        self.trap.wait_while('running')

    def move_measure(self, deg):
        self.measuring_motor.run_to_rel_pos(position_sp=deg, speed_sp=1000, stop_action="hold")
        self.measuring_motor.wait_while('running')

    # POSITIONS
    def open_trap_completly(self):
        self.move_trap(-60)

    def open_trap_half(self):
        self.move_trap(-30)

    def close_trap(self):
        self.move_trap(59)

    def close_trap_at_half(self):
        self.move_trap(30)

    # SENSORS
    def get_color(self):
        # print(cl.value(0), cl.value(1), cl.value(2))
        r = round(re_map(self.cl.value(0), 0, R_MAX, 0, 255), 0)
        g = round(re_map(self.cl.value(1), 0, G_MAX, 0, 255), 0)
        b = round(re_map(self.cl.value(2), 0, B_MAX, 0, 255), 0)
        print("[COLOR] ", r, ",", g, ",", b)
        return int(r), int(g), int(b)

    def is_pressed(self):
        return self.ts.is_pressed

    # BAND
    def start_band(self):
        self.band.run_forever(speed_sp=50)
        print("[BAND] Started band")

    def stop_band(self):
        self.band.stop(stop_action="hold")
        print("[BAND] Stopped band")
