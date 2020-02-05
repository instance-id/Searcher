import sys

from hutil.Qt import QtCore, QtUiTools, QtWidgets, QtGui

import hou
import os

from parse import parsers
from . import database
from . import gofunctions
from . import searcher_settings

# info
__author__ = "instance.id"
__copyright__ = "2020 All rights reserved. See LICENSE for more details."
__status__ = "Prototype"

reload(parsers)
reload(database)
reload(gofunctions)
reload(searcher_settings)

script_path = os.path.dirname(os.path.realpath(__file__))

gofuncs = gofunctions.GoFunctions()
ui = searcher_settings.SearcherSettings()
ui.getgofunctions(gofuncs)

class Searcher(QtWidgets.QWidget):
    """instance.id Searcher for Houdini"""

    def __init__(self):
        super(Searcher, self).__init__()
        self.window = QtWidgets.QMainWindow()
        self.parser = parsers.ParseData()


        self.setGeometry((self.width() - 100) / 2, (self.height() - 100) / 2, 100, 100)

        # Load UI File
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(script_path + '/searcher.ui')

        # Get UI Elements
        self.opensettings = self.ui.findChild(QtWidgets.QPushButton, "opensettings_btn")
        self.searchresultslst = self.ui.findChild(QtWidgets.QListWidget, "searchresults_lst")
        self.searchresultstbl = self.ui.findChild(QtWidgets.QTableWidget, "searchresults_tbl")
        self.searchbox = self.ui.findChild(QtWidgets.QLineEdit, "searchbox_txt")

        # Create Connections
        self.opensettings.clicked.connect(self.opensettings_cb)
        self.searchbox.textChanged.connect(self.textchange_cb)

        # Layout
        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.setAlignment(QtCore.Qt.AlignTop)
        mainlayout.setContentsMargins(0, 0, 0, 0)
        mainlayout.setGeometry(QtCore.QRect(0, 0, 1400, 1200))
        mainlayout.addWidget(self.ui)
        self.setLayout(mainlayout)

    # ------------------------------------------------------------------------------------------------------------------ Callbacks
    def opensettings_cb(self):
        self.open_settings()

    def textchange_cb(self, text):
        if len(text) > 1:
            txt = self.parser.searchtext(text)
            self.searchtablepopulate(txt)
        else:
            self.searchresultstbl.clearContents()
            self.searchresultstbl.setRowCount(0)

    def searchclick_cb(self):
        self.searchresultslst.clear()
        return

    # ------------------------------------------------------------------------------------------------------------------ Actions
    # ---------------------------------------------- Navigation
    def open_settings(self):
        ui.show()

    # ---------------------------------------------- Search Functionality
    def searchtablepopulate(self, data):
        rows = len(data)
        if rows > 0:
            cols = len(data[0])
            self.searchresultstbl.clearContents()
            self.searchresultstbl.setHorizontalHeaderLabels(['Label', 'Description', 'Assignments', 'Context'])
            self.searchresultstbl.setRowCount(rows)
            self.searchresultstbl.setColumnCount(cols)
            self.searchresultstbl.setColumnWidth(0, 250)
            self.searchresultstbl.setColumnWidth(1, 250)
            self.searchresultstbl.setColumnWidth(2, 100)
            self.searchresultstbl.setColumnWidth(3, 150)
            for i in range(rows):
                for j in range(cols):
                    newitem = QtWidgets.QTableWidgetItem(str(data[i][j]))
                    self.searchresultstbl.setItem(i, j, newitem)

    def menuItemDoubleClicked(self, item):
        data = item.data()
        pref = hou.getPreference(data)
        print pref
        hou.ui.displayMessage(pref)

    def openscene(self, item):
        hipFile = self.proj + item.data()
        hou.hipFile.load(hipFile)

    def closeEvent(self, event):
        self.setParent(None)
