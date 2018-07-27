import sys
import fire
from PyQt4.QtGui import QApplication
from .menu_gui import MenuGUI
from .menu_manager import remove, add, show


def run_cli():
    fire.Fire({
        "remove": remove,
        "add": add,
        "show": show
    })


def run_gui():
    app = QApplication(sys.argv)
    ui_window = MenuGUI(None)
    ui_window.show()
    app.exec_()
