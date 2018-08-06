import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QGroupBox, \
    QLineEdit

from const import TRAP_MODE_CLOSED, COINS
from threads import TrapLoop


class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout()
        self.setLayout(lay)
        lay.addWidget(QPushButton("HELLO"))
        self.dialog = WhichValueDialog()
        self.dialog.event = self.got_amount
        self.dialog.exec_()

        self.show()

    def got_amount(self, amount):
        print(amount)
        self.dialog.close()


class WhichValueDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.label = QLabel("<h3>Bitte wähle die Münze aus, die sich aktuell in der Klappe befindet.</h3>")
        self.vbox.addWidget(self.label)

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


MODE_MANUAL = 0
MODE_DETECT = 1
MODE_COUNT = 2


class Controller(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = TrapLoop()
        self.thread.start()

        self.vbox = QHBoxLayout()

        self.mode = MODE_MANUAL

        #########
        # MODUS #
        #########
        self.modus_group = QGroupBox()
        self.modus_group.setTitle("Betriebsmodus")
        self.modus_group_layout = QVBoxLayout()
        self.modus_group.setLayout(self.modus_group_layout)
        self.vbox.addWidget(self.modus_group)

        self.modus_label = QLabel("Manueller Betrieb")
        self.modus_group_layout.addWidget(self.modus_label)

        self.btn_manual_modus = QPushButton("Automatischen Modus ausschalten")
        self.btn_manual_modus.setEnabled(False)
        self.btn_manual_modus.clicked.connect(self.switch_modus_to_manual)
        self.modus_group_layout.addWidget(self.btn_manual_modus)

        self.btn_detect_modus = QPushButton("Erkennungsmodus einschalten")
        self.btn_detect_modus.clicked.connect(self.switch_modus_to_detect)
        self.modus_group_layout.addWidget(self.btn_detect_modus)

        self.btn_count_modus = QPushButton("Zählmodus einschalten")
        self.btn_count_modus.clicked.connect(self.switch_modus_to_count)
        self.modus_group_layout.addWidget(self.btn_count_modus)

        ##############
        # FLIESSBAND #
        ##############

        self.band_group = QGroupBox()
        self.band_group.setTitle("Fließband")
        self.band_group_layout = QVBoxLayout()
        self.band_group.setLayout(self.band_group_layout)
        self.vbox.addWidget(self.band_group)

        self.band_status_label = QLabel("Keine Information")
        self.band_group_layout.addWidget(self.band_status_label)

        self.btn_start_band = QPushButton("Fließband starten")
        self.btn_start_band.clicked.connect(self.thread.band_thread.start_band)
        self.band_group_layout.addWidget(self.btn_start_band)

        self.btn_stop_band = QPushButton("Fließband stoppen")
        self.btn_stop_band.clicked.connect(self.thread.band_thread.stop_band)
        self.band_group_layout.addWidget(self.btn_stop_band)

        ##########
        # KLAPPE #
        ##########

        self.trap_group = QGroupBox()
        self.trap_group.setTitle("Klappe")
        self.trap_group_layout = QHBoxLayout()
        self.trap_group.setLayout(self.trap_group_layout)
        self.vbox.addWidget(self.trap_group)

        self.trap_vbox1 = QVBoxLayout()
        self.trap_group_layout.addLayout(self.trap_vbox1)

        self.trap_status_label = QLabel()
        self.trap_vbox1.addWidget(self.trap_status_label)

        self.btn_open_trap_completly = QPushButton("Klappe öffnen")
        self.btn_open_trap_completly.clicked.connect(self.thread.open_trap_completly)
        self.trap_vbox1.addWidget(self.btn_open_trap_completly)

        self.trap_vbox2 = QVBoxLayout()
        self.trap_group_layout.addLayout(self.trap_vbox2)

        self.trap_deg_hbox = QHBoxLayout()
        self.trap_vbox2.addLayout(self.trap_deg_hbox)

        self.trap_deg_pos1_label = QLabel("Klappe um ")
        self.trap_deg_edit = QLineEdit()
        self.trap_deg_edit.setText("10")
        self.trap_deg_edit.textChanged.connect(self.check_trap_deg)
        self.trap_deg_pos2_label = QLabel(" Grad …")
        self.trap_deg_hbox.addWidget(self.trap_deg_pos1_label)
        self.trap_deg_hbox.addWidget(self.trap_deg_edit)
        self.trap_deg_hbox.addWidget(self.trap_deg_pos2_label)

        self.btn_open_trap_manual = QPushButton("… öffnen")
        self.btn_open_trap_manual.clicked.connect(self.open_trap_with_deg)
        self.trap_vbox2.addWidget(self.btn_open_trap_manual)

        self.btn_close_trap_manual = QPushButton("… schließen")
        self.btn_close_trap_manual.clicked.connect(self.close_trap_with_deg)
        self.trap_vbox2.addWidget(self.btn_close_trap_manual)

        ##########
        # KLAPPE #
        ##########

        self.detect_group = QGroupBox()
        self.detect_group.setTitle("Breitesensor")
        self.detect_group_layout = QVBoxLayout()
        self.detect_group.setLayout(self.detect_group_layout)
        self.vbox.addWidget(self.detect_group)

        self.detect_deg_hbox = QHBoxLayout()
        self.detect_group_layout.addLayout(self.detect_deg_hbox)

        self.detect_deg_pos1_label = QLabel("Breitesensor um ")
        self.detect_deg_edit = QLineEdit()
        self.detect_deg_edit.setText("10")
        self.detect_deg_edit.textChanged.connect(self.check_detect_deg)
        self.detect_deg_pos2_label = QLabel(" Grad …")
        self.detect_deg_hbox.addWidget(self.detect_deg_pos1_label)
        self.detect_deg_hbox.addWidget(self.detect_deg_edit)
        self.detect_deg_hbox.addWidget(self.detect_deg_pos2_label)

        self.btn_open_detect_manual = QPushButton("… nach vorne bewegen")
        self.btn_open_detect_manual.clicked.connect(self.open_detect_with_deg)
        self.detect_group_layout.addWidget(self.btn_open_detect_manual)

        self.btn_close_detect_manual = QPushButton("… nach hinten bewegen")
        self.btn_close_detect_manual.clicked.connect(self.close_detect_with_deg)
        self.detect_group_layout.addWidget(self.btn_close_detect_manual)

        ############
        # SENSOREN #
        ############
        self.sensor_group = QGroupBox()
        self.sensor_group.setTitle("Sensoren")
        self.sensor_group_layout = QVBoxLayout()
        self.sensor_group.setLayout(self.sensor_group_layout)
        self.vbox.addWidget(self.sensor_group)

        self.ir_sensor_box = QHBoxLayout()
        self.ir_sensor_label = QLabel("Infrarotsensor: ")
        self.ir_sensor = QLabel()
        self.ir_sensor_box.addWidget(self.ir_sensor_label)
        self.ir_sensor_box.addWidget(self.ir_sensor)
        self.sensor_group_layout.addLayout(self.ir_sensor_box)

        self.cl_sensor_box = QHBoxLayout()
        self.cl_sensor_label = QLabel("RGB-Farbsensor: ")
        self.cl_sensor = QLabel()
        self.cl_sensor_box.addWidget(self.cl_sensor_label)
        self.cl_sensor_box.addWidget(self.cl_sensor)
        self.sensor_group_layout.addLayout(self.cl_sensor_box)

        # btn = QPushButton('Beenden')
        # btn.clicked.connect(sys.exit)
        # self.vbox.addWidget(btn)

        self.thread.set_refresh(self.refresh)

        self.setLayout(self.vbox)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('CashCounter – Steuerung')
        self.show()

    def switch_modus_to_manual(self):
        if self.mode == MODE_COUNT or self.mode == MODE_DETECT:
            self.mode = MODE_MANUAL
            self.modus_label.setText("Manueller Betrieb")
            self.thread.stop_work()
            self.btn_detect_modus.setEnabled(True)
            self.btn_count_modus.setEnabled(True)
            self.btn_manual_modus.setEnabled(False)

    def switch_modus_to_count(self):
        if self.mode == MODE_MANUAL:
            self.mode = MODE_COUNT
            self.modus_label.setText("Zählmodus")
            self.thread.start_work()
            self.btn_detect_modus.setEnabled(False)
            self.btn_count_modus.setEnabled(False)
            self.btn_manual_modus.setEnabled(True)

    def switch_modus_to_detect(self):
        if self.mode == MODE_MANUAL:
            self.mode = MODE_DETECT
            self.modus_label.setText("Erkennungsmodus")
            self.thread.stop_work()
            self.btn_detect_modus.setEnabled(False)
            self.btn_count_modus.setEnabled(False)
            self.btn_manual_modus.setEnabled(True)

    def check_trap_deg(self):
        t = self.trap_deg_edit.text()
        try:
            i = int(t)
            if i < 100:
                self.btn_open_trap_manual.setEnabled(True)
                self.btn_close_trap_manual.setEnabled(True)
        except ValueError:
            self.btn_open_trap_manual.setEnabled(False)
            self.btn_close_trap_manual.setEnabled(False)

    def check_detect_deg(self):
        t = self.detect_deg_edit.text()
        try:
            i = int(t)
            if i < 1000:
                self.btn_open_detect_manual.setEnabled(True)
                self.btn_close_detect_manual.setEnabled(True)
        except ValueError:
            self.btn_open_detect_manual.setEnabled(False)
            self.btn_close_detect_manual.setEnabled(False)

    def get_trap_deg(self):
        t = self.trap_deg_edit.text()
        i = int(t)
        return i

    def open_trap_with_deg(self):
        print("HI")
        self.thread.move_trap(self.get_trap_deg() * -1)

    def close_trap_with_deg(self):
        self.thread.move_trap(self.get_trap_deg())

    def get_detect_deg(self):
        t = self.detect_deg_edit.text()
        i = int(t)
        return i

    def open_detect_with_deg(self):
        print("HI")
        self.thread.move_detect(self.get_detect_deg())

    def close_detect_with_deg(self):
        self.thread.move_detect(self.get_detect_deg() * -1)

    def refresh(self):
        # print("REFRESH BECAUSE STATE CHANGED")
        if self.thread.band_thread.band_manual_stopped:
            t = "Manuell gestoppt"
            self.btn_start_band.setEnabled(True)
            self.btn_stop_band.setEnabled(False)
        elif self.thread.band_thread.band_running:
            t = "In Betrieb (Automatisch)"
            self.btn_start_band.setEnabled(False)
            self.btn_stop_band.setEnabled(True)
        else:
            t = "Ausgeschaltet (Automatisch)"
            self.btn_start_band.setEnabled(False)
            self.btn_stop_band.setEnabled(False)

        self.band_status_label.setText(t)

        if self.thread.trap_mode == TRAP_MODE_CLOSED:
            t = "Geschlossen"
            self.btn_open_trap_completly.setEnabled(True)

        self.trap_status_label.setText(t)

        self.ir_sensor.setText(str(self.thread.band_thread.distance))

        # print(self.thread.color)

        # self.cl_sensor.update()

        # self.cl_sensor.setStyleSheet("QLabel { background-color : rgb(%s, %s, %s);}" % (
        #    str(self.thread.color[0]), str(self.thread.color[1]), str(self.thread.color[2])))
        # self.cl_sensor.update()

    # print("QLabel { background-color : rgb(%s, %s, %s);}" % (
    #    str(self.thread.color[0]), str(self.thread.color[1]), str(self.thread.color[2])))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = TestWindow()
