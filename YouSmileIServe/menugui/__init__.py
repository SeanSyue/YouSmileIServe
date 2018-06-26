import sys
from PyQt4.QtGui import QApplication

from menugui import MenuGUI

def run_gui():
    app = QApplication(sys.argv)
    ui_window = MenuGUI(None)
    ui_window.show()
    app.exec_()