import sys

from hutil.Qt import QtCore, QtUiTools, QtWidgets, QtGui

import hou
import os

from datahandler import datahandler
from . import database
from . import gofunctions
from . import searcher_settings

# info
__author__ = "instance.id"
__copyright__ = "2020 All rights reserved. See LICENSE for more details."
__status__ = "Prototype"

reload(datahandler)
reload(database)
reload(gofunctions)
reload(searcher_settings)

script_path = os.path.dirname(os.path.realpath(__file__))

gofuncs = gofunctions.GoFunctions()
ui = searcher_settings.SearcherSettings()
ui.getgofunctions(gofuncs)
name = "Searcher"


def CreateSearcherPanel(position=(750, 300), size=(1000, 450)):
    desktop = hou.ui.curDesktop()
    panel = desktop.createFloatingPaneTab(
        hou.paneTabType.PythonPanel,
        python_panel_interface="searcher",
        position=position,
        size=size,
    )
    panel.setIsCurrentTab()
    panel.setName("searcher")


def kill_pane_tab(thispanel):
    thispanel.close()


class Searcher(QtWidgets.QWidget):
    """instance.id Searcher for Houdini"""

    def __init__(self):
        super(Searcher, self).__init__()
        self.window = QtWidgets.QMainWindow()
        self.handler = datahandler.DataHandler()

        # self.setGeometry((self.width() - 100) / 2, (self.height() - 100) / 2, 100, 100)
        self.main_widget = QtWidgets.QWidget(self)
        # Load UI File
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(script_path + "/searcher.ui")

        # Get UI Elements
        self.opensettings = self.ui.findChild(
            QtWidgets.QPushButton, "opensettings_btn")
        self.searchresultstree = self.ui.findChild(
            QtWidgets.QTreeWidget, "searchresults_tbl"
        )

        self.searchbox = self.ui.findChild(
            QtWidgets.QLineEdit, "searchbox_txt")
        self.searchbox.setPlaceholderText("Search..")
        self.searchbox.setFocusPolicy(QtCore.Qt.StrongFocus)

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

        self.searchbox.setFocus()
        self.hcontext = self.handler.gethcontext()

    # ------------------------------------------------------------------------------------------------------------------ Callbacks
    def opensettings_cb(self):
        self.open_settings()

    def textchange_cb(self, text):
        if len(text) > 1:
            txt = self.handler.searchtext(text)
            self.searchtablepopulate(txt)
        else:
            self.searchresultstree.clear()
            self.searchresultstree.setRowCount(0)

    def searchclick_cb(self):
        self.searchresultstree.clear()
        return

    # ------------------------------------------------------------------------------------------------------------------ Actions
    # ---------------------------------------------- Navigation
    def open_settings(self):
        ui.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            panel = hou.ui.findPaneTab("searcher")
            panel.setIsCurrentTab()
            panel.close()
            # kill_pane_tab(panel)

    # ---------------------------------------------- Search Functionality
    def searchtablepopulate(self, data):
        rows = len(data)
        if rows > 0:
            cols = len(data[0])
            self.searchresultstree.clear()

            # self.searchresultstree.setRowCount(rows)
            self.searchresultstree.setColumnCount(cols)
            self.searchresultstree.setColumnWidth(0, 250)
            self.searchresultstree.setColumnWidth(1, 250)
            self.searchresultstree.setColumnWidth(2, 100)
            self.searchresultstree.setColumnWidth(3, 150)

            self.searchresultstree.setHeaderLabels(
                ["Label", "Description", "Assignments", "Symbol"]
            )
            # self.searchresultstree.addTopLevelItem(hotkeys)
            hcontext_tli = []

            hrows = len(self.hcontext)
            for h in range(hrows):
                hcontext_tli.append(QtWidgets.QTreeWidgetItem(
                    self.searchresultstree, self.hcontext[h][0]))

            for i in range(rows):
                hotkeys = QtWidgets.QTreeWidgetItem(hcontext_tli, data[i])

            self.searchresultstree.insertTopLevelItems(0, hcontext_tli)
            #     item = QtWidgets.QTreeWidgetItem()
            #     item.setText(0, data[i])
            #     item.setData(0, Qt.UserRole, ('report', report))
            #     hotkeys.addChild(item)
            #     cnt += 1
            #     hotkeys.setText(0, "Reports ({})".format(cnt))

            #     items.append(QtWidgets.QTreeWidgetItem(None, QtGui.QStringList(QtGui.QString("item: %1").arg(i))))
            # self.searchresultstree.insertTopLevelItems(None, items)

            # for i in range(rows):
            #     for j in range(cols):
            #         newitem = QtWidgets.QTableWidgetItem(str(data[i][j]))
            #         self.searchresultstree.setItem(i, j, newitem)

            # self.searchresultstree.setHorizontalHeaderLabels(['Label', 'Description', 'Assignments', 'Symbol'])

            # self.searchresultstree.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
            # self.searchresultstree.horizontalHeaderItem(0).setSizeHint(QtGui.QSize(20, 20))
            # self.searchresultstree.horizontalHeaderItem(1).setSizeHint(QtWidgets.QSize(20, 20))
            # self.searchresultstree.horizontalHeaderItem(2).setSizeHint(QtWidgets.QSize(20, 20))
            # self.searchresultstree.horizontalHeaderItem(3).setSizeHint(QtWidgets.QSize(20, 20))

    def menuItemDoubleClicked(self, item):
        data = item.data()
        pref = hou.getPreference(data)
        print pref
        hou.ui.displayMessage(pref)

    def closeEvent(self, event):
        self.setParent(None)
