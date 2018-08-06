import time

from const import TRAP_MODE_CLOSED, TRAP_MODE_HALF, TRAP_MODE_OPEN


class Band:
    def __init__(self, ev3):
        self.ev3 = ev3
        self.band_running = False
        self.band_manual_stopped = False

    def start_band(self, x=0, manual=True):
        if not manual:
            self.band_running = True
        else:
            self.band_manual_stopped = False

        self.ev3.start_band()

    def stop_band(self, x=0, manual=True):
        if not manual:
            self.band_manual_stopped = False
            self.band_running = False
        else:
            self.band_manual_stopped = True

        self.ev3.stop_band()
