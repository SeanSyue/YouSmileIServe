import os.path
import sys
from PyQt4 import uic
from PyQt4.QtGui import QApplication, QMainWindow

from menu_cli import add, remove, show

ui_filename = os.path.splitext(__file__)[0] + '.ui'
ui_menu = uic.loadUiType(ui_filename)[0]


class MenuGUI(QMainWindow, ui_menu):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.action_Exit.triggered.connect(QApplication.exit)
        self.menu_list_show()

        self.deletebm1.clicked.connect(self.rice_delete)
        self.deletebm2.clicked.connect(self.noodle_delete)

        self.addbm.clicked.connect(self.addmenu)

    def menu_list_show(self):
        self.ricemenu = show("rice")
        self.noodlemenu = show("noodle")

        self.ricelist.clear()
        self.noodlelist.clear()
        for item in self.ricemenu:
            self.ricelist.addItem(item)

        for item in self.noodlemenu:
            self.noodlelist.addItem(item)

    def rice_delete(self):
        remove("rice", str(self.ricelist.currentItem().text()))
        self.menu_list_show()

    def noodle_delete(self):
        remove("noodle", str(self.noodlelist.currentItem().text()))
        self.menu_list_show()

    def addmenu(self):
        add(str(self.cbmenu.currentText()), str(self.lineEdit.text()))
        self.menu_list_show()
        self.lineEdit.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui_window = MenuGUI(None)
    ui_window.show()
    app.exec_()
