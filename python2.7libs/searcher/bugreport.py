from __future__ import absolute_import
from searcher import bugreport_ui
from searcher import util
import os
import sys
import codecs

import hou
hver = 0
if os.environ["HFS"] != "":
    ver = os.environ["HFS"]
    hver = int(ver[ver.rindex('.')+1:])
    from hutil.Qt import QtGui
    from hutil.Qt import QtCore
    from hutil.Qt import QtWidgets
    from hutil.Qt import QtUiTools

try:
    pyside = os.environ['HOUDINI_QT_PREFERRED_BINDING']
    parent = hou.qt.mainWindow()
except KeyError:
    parent = hou.ui.mainQtWindow()
    pyside = 'PySide'

if pyside == 'PySide2':
    from PySide2 import QtWebEngineWidgets

elif pyside == 'PySide':
    from PySide.QtWebKit import QWebView


scriptpath = os.path.dirname(os.path.realpath(__file__))


class BugReport(QtWidgets.QWidget):
    """ Searcher Settings and Debug Menu"""

    def __init__(self, parent=None):
        super(BugReport, self).__init__(parent=parent)
        self.setParent(parent)
        self.parentwindow = parent
        self.ui = bugreport_ui.Ui_BugReport()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.issuetitle = ""

        self.ui.pushButton.pressed.connect(self.doweb)

        self.installEventFilter(self)

    def doweb(self):
        issue = "Issue2"
        self._webview = QtWebEngineWidgets.QWebEngineView(self)
        self._webview.setGeometry(QtCore.QRect(0, 0, self.width(), self.height()))
        self.issuetitle = issue
        #set html content
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "bugsubmit.html"))
        base_url = QtCore.QUrl(html_path)


        html = codecs.open(html_path, 'r')
        html_str = html.read()
        html_out = html_str.replace('ISSUE_TITLE', self.issuetitle)
        self._webview.setHtml(html_out, base_url)
        self._webview.show()

    # ------------------------------------------------------------- Events
    # SECTION Events -----------------------------------------------------
    def eventFilter(self, obj, event):
        event_type = event.type()

        # ---------------------------------------- Keypress
        # NOTE Keypress -----------------------------------
        if event_type == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Escape:
                self.parentwindow.closeroutine()

        return QtCore.QObject.eventFilter(self, obj, event)