from const import STEP_WIDTH, STEP_BEGINN, STEP_MAX


class Measure:
    def __init__(self, ev3):
        self.ev3 = ev3

    def measure(self):
        print("[MEASURE] Beginn to measure width → Move to start position with ", STEP_BEGINN)
        self.ev3.move_measure(STEP_BEGINN)
        deg = 0
        print("[MEASURE] Pressed? ", self.ev3.is_pressed)
        while deg < STEP_MAX and self.ev3.is_pressed() is 0:
            self.ev3.move_measure(STEP_WIDTH)
            deg += STEP_WIDTH

            print("[MEASURE] Pressed? ", self.ev3.is_pressed)

            print("[MEASURE] Measured angle steps = ", deg)

        back_deg = (deg * -1) + -2000
        print("[MEASURE] Move back with ", back_deg)
        self.ev3.move_measure(back_deg)
        return deg
