import json
import sys

from PyQt5.QtWidgets import QApplication

from gui.whichvalue import WhichValueDialog

BASE = {
    "measurements": []
}


class Handler:
    FILE = "data.json"

    def __init__(self):
        pass

    def handle(self, color, size):
        pass


class DetectHandler(Handler):
    def __init__(self, color, size):
        super().__init__()

        self.size = size
        self.color = color

        self.dialog = WhichValueDialog(self.color, self.size)
        self.dialog.event = self.got_amount
        self.dialog.exec_()

    def create_empty_file(self):
        with open(self.FILE, "w") as file:
            file.write(json.dumps(BASE))
            file.close()
            return True

    def get_data(self):
        try:
            with open(self.FILE) as file:
                data = json.load(file)
                file.close()
                print(data)
                return data
        except FileNotFoundError:
            return None

    def save_data(self, data):
        try:
            with open(self.FILE, "w") as file:
                file.write(json.dumps(data))
                file.close()
                print(data)
                return True
        except FileNotFoundError:
            return None

    def got_amount(self, amount):
        self.dialog.close()

        if amount != 0:
            data = self.get_data()

            if data is None:
                self.create_empty_file()
                data = self.get_data()

            new_record = {
                "rgb": self.color,
                "size": self.size,
                "amount": amount
            }

            data["measurements"].append(new_record)

            if self.save_data(data):
                print("[DETECT HANDLER] New record saved: ", new_record)
        else:
            print("[DETECT HANDLER] No coin.")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    handler = DetectHandler((139, 0, 0), 100)
