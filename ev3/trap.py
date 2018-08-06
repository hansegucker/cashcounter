import time

from const import TRAP_MODE_CLOSED, TRAP_MODE_HALF, TRAP_MODE_OPEN


class Trap:
    def __init__(self, ev3):
        self.ev3 = ev3
        self.trap_mode = TRAP_MODE_CLOSED

    def open_trap_completly(self):
        if self.trap_mode == TRAP_MODE_CLOSED or self.trap_mode == TRAP_MODE_HALF:
            self.open_trap()
            time.sleep(0.5)
            self.close_trap()
            print("[TRAP] Opened trap at one")

    def open_trap_half(self):
        if self.trap_mode == TRAP_MODE_CLOSED:
            self.ev3.open_trap_half()
            self.trap_mode = TRAP_MODE_HALF
            print("[TRAP] Opened trap from 0% to 50%")

    def open_trap(self):
        if self.trap_mode == TRAP_MODE_CLOSED:
            self.ev3.open_trap_completly()
            self.trap_mode = TRAP_MODE_OPEN
            print("[TRAP] Opened trap from 0% to 100%")
        elif self.trap_mode == TRAP_MODE_HALF:
            self.ev3.open_trap_half()
            self.trap_mode = TRAP_MODE_OPEN
            print("[TRAP] Opened trap from 50% to 100%")

    def close_trap(self):
        if self.trap_mode == TRAP_MODE_OPEN:
            self.ev3.close_trap()
            self.trap_mode = TRAP_MODE_CLOSED
            print("[TRAP] Closed trap from 100% to 0%")
        elif self.trap_mode == TRAP_MODE_HALF:
            self.ev3.close_trap_at_half()
            self.trap_mode = TRAP_MODE_CLOSED
            print("[TRAP] Closed trap from 50% to 0%")
