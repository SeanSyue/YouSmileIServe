import os.path
import sys
from PyQt4 import uic
from PyQt4.QtGui import QApplication, QMainWindow

from menu_cli import add, remove, show

# MUST use '.py' instead of 'py', cus we don't wanna modify the "python 3.x" statement in '__file__' string
ui_filename = __file__.replace('.py', '.ui')
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
