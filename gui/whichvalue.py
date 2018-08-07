import sys

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QDialog, QPushButton, QWidget, QApplication

from const import COINS


# class TestWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         lay = QVBoxLayout()
#         self.setLayout(lay)
#         lay.addWidget(QPushButton("HELLO"))
#         self.dialog = WhichValueDialog()
#         self.dialog.event = self.got_amount
#         self.dialog.exec_()
#
#         self.show()
#
#     def got_amount(self, amount):
#         print(amount)
#         self.dialog.close()


class WhichValueDialog(QDialog):
    def __init__(self, color=(0, 0, 0), size=0):
        super().__init__()

        self.color = color
        self.size = size

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.label = QLabel("<h3>Bitte wähle die Münze aus, die sich aktuell in der Klappe befindet.</h3>")
        self.vbox.addWidget(self.label)

        self.data_box = QHBoxLayout()
        self.vbox.addLayout(self.data_box)

        self.data_label = QLabel("<strong><u>Daten</u></strong>")
        self.data_box.addWidget(self.data_label)

        self.color_label = QLabel("<strong>Farbe</strong>")
        self.data_box.addWidget(self.color_label)

        self.color_show = QLabel("")
        self.color_show.setStyleSheet("QLabel { background-color : rgb(%s, %s, %s);}" % (
            str(self.color[0]), str(self.color[1]), str(self.color[2])))
        self.data_box.addWidget(self.color_show)

        self.size_label = QLabel("<strong>Größe</strong>")
        self.data_box.addWidget(self.size_label)

        self.size_show = QLabel("{} °".format(self.size))
        self.data_box.addWidget(self.size_show)

        self.hr = QLabel("<hr>")
        self.vbox.addWidget(self.hr)

        self.coin_buttons_box = QHBoxLayout()
        self.vbox.addLayout(self.coin_buttons_box)

        self.coin_buttons = {}
        for key, value in COINS.items():
            self.coin_buttons[key] = QPushButton()
            pixmap = QPixmap("res/{}".format(value["res"]))
            icon = QIcon(pixmap)
            self.coin_buttons[key].setIcon(icon)
            self.coin_buttons[key].setIconSize(QSize(100, 100))
            self.coin_buttons[key].clicked.connect(self.coin_clicked)
            self.coin_buttons_box.addWidget(self.coin_buttons[key])

        self.setWindowTitle("Münzerkennung")
        self.setWindowModality(Qt.ApplicationModal)

    def coin_clicked(self):
        sender = self.sender()
        print("COIN CLICKED")
        for key, value in COINS.items():
            if sender == self.coin_buttons[key]:
                print(value["amount"])
                self.event(value["amount"])


if __name__ == '__main__':
    pass
