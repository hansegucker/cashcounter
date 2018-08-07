import sys
from PyQt5.QtWidgets import *

from gui.gui import Controller

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)

        w = Controller()

        sys.exit(app.exec_())
    except KeyboardInterrupt:
        pass

# Shutdown everything
