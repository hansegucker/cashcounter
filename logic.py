import time

from ev3.measure import Measure
from ev3.trap import Trap


class TrapManagement:
    def __init__(self, ev3):
        self.ev3 = ev3

        self.trap = Trap(self.ev3)
        self.measure = Measure(self.ev3)

        self.trap_available = True

    def measure_coin(self):
        # Block trap
        self.trap_available = False

        # Wait a moment
        time.sleep(1)

        # Measurement
        # print(self.color)
        # time.sleep(0.5)

        # Open trap half
        self.trap.open_trap_half()
        # time.sleep(0.2)

        # Measure width
        size = self.measure.measure()

        # Measure color
        color = self.ev3.get_color()

        # Open trap
        self.trap.open_trap_completly()

        # Release trap
        self.trap_available = True
