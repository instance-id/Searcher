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
        self.updatehkeys = self.ui.findChild(QtWidgets.QPushButton, "updatehotkeys_btn")

        # Create Connections
        self.sendgocommand.clicked.connect(self.sendgocommand_cb)
        self.updatehkeys.clicked.connect(self.updatehotkeys_cb)

        # Layout
        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.addWidget(self.ui)
        self.setLayout(mainlayout)

    # ------------------------------------------------------------------------------------------------------------------ Callbacks
    def sendgocommand_cb(self):
        self.gofunc.callgofunction(self.gocommandtext.text())
        return

    def updatehotkeys_cb(self):
        data = self.parser.updatehotkeys()

    # ------------------------------------------------------------------------------------------------------------------ Actions
    def getgofunctions(self, gofunctiondata):
        self.gofunc = gofunctiondata


