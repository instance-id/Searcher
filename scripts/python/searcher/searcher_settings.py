import sys

from hutil.Qt import QtCore, QtUiTools, QtWidgets, QtGui

import hou
import os

from . import gofunctions


# info
__author__ = "instance.id"
__copyright__ = "2020 All rights reserved. See LICENSE for more details."
__status__ = "Prototype"

scriptpath = os.path.dirname(os.path.realpath(__file__))


class SearcherSettings(QtWidgets.QWidget):
    def __init__(self):
        super(SearcherSettings, self).__init__()

        # Load UI File
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(scriptpath + '/searchersettings.ui')

        # Get UI Elements
        self.gocommandtext = self.ui.findChild(QtWidgets.QLineEdit, "gocommand_txt")
        self.sendgocommand = self.ui.findChild(QtWidgets.QPushButton, "sendgocommand_btn")
        self.addhkeys = self.ui.findChild(QtWidgets.QPushButton, "addhotkeys_btn")
        self.updatehkeys = self.ui.findChild(QtWidgets.QPushButton, "updatehotkeys_btn")
        self.cleardata = self.ui.findChild(QtWidgets.QPushButton, "cleardata_btn")

        # Create Connections
        self.sendgocommand.clicked.connect(self.sendgocommand_cb)
        self.addhkeys.clicked.connect(self.addhotkeys_cb)
        self.updatehkeys.clicked.connect(self.updatehotkeys_cb)
        self.cleardata.clicked.connect(self.cleardata_cb)

        # Layout
        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.addWidget(self.ui)
        self.setLayout(mainlayout)

    # ------------------------------------------------------------------------------------------------------------------ Callbacks
    def sendgocommand_cb(self):
        self.gofunc.callgofunction("-q", self.gocommandtext.text().strip())

    def addhotkeys_cb(self):
        self.gofunc.callgofunction("ahk", self.gocommandtext.text().strip())

    def updatehotkeys_cb(self):
        self.gofunc.callgofunction("uhk", self.gocommandtext.text().strip())

    def cleardata_cb(self):
        self.gofunc.callgofunction("c", self.gocommandtext.text().strip())

    # ------------------------------------------------------------------------------------------------------------------ Actions
    def getgofunctions(self, gofunctiondata):
        self.gofunc = gofunctiondata

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            print("esc")
