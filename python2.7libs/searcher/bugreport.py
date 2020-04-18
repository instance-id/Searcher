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
reload(bugreport_ui)

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
        self._webview = None
        self.blocker = False
        self.html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "bugsubmit.html"))
        self.base_url = QtCore.QUrl(self.html_path)
        self.installEventFilter(self)
        self.ui.title.installEventFilter(self)
        
    def initmenu(self):
        self.resize(self.width(), self.parentwindow.height() - 300)
        self._webview  = None
        self.isediting = True
        self.html = None
        self.html_out = ""
        self.html_str = ""
        self.priortext = ""
        self.ui.title.setText("")
        self.ui.edittitle_btn.pressed.connect(self.doweb)

        self.ui.title.setFocus()

    def edittitle_cb(self):
        if not self.blocker:
            self.blocker = True
            if (hou.ui.displayMessage(
                    title='Edit Title?',
                    text='Bug report text will be reset.',
                    buttons=("Ok", "Cancel")) == 0):
                self.isediting = True
                self.enabletitleedit()
                self.blocker = False

    def enabletitleedit(self):
        self._webview.hide()
        self.resize(self.width(), self.parentwindow.height() - 300)
        self.ui.title.setReadOnly(False)
        self.ui.edittitle_btn.setText("Set Title")
        
    def enablereporttext(self):
        self.resize(self.width(), self.parentwindow.height() - 50)
        self.ui.title.setReadOnly(True)
        self.ui.edittitle_btn.setText("Edit Title")

    def doweb(self):
        if self.ui.title.text() == "":
            self.parentwindow.parentwindow.setstatusmsg("Please enter a title for your bug report", "ImportantMessage")
            if hou.isUIAvailable():
                hou.ui.setStatusMessage(
                    "Please enter a title for your bug report.", severity=hou.severityType.Warning)        
            return
        
        if self.isediting: 
            self.enablereporttext() 
        else: 
            self.edittitle_cb()
            return
        
        if self._webview is None:
            self._webview = QtWebEngineWidgets.QWebEngineView(self.ui.webview)
            self._webview.setGeometry(QtCore.QRect(-10, 0, self.width(), self.height()))

        self.html = codecs.open(self.html_path, 'r')
        self.html_str = self.html.read()
        self.html_out = self.html_str.replace('ISSUE_TITLE', self.ui.title.text())
        # self._webview.setHtml(self.html_out, self.base_url)
        self._webview.load(QtCore.QUrl("https://instance.id/searcher/bugsubmit.html"))
        self._webview.show()
        self.isediting = False

    # ------------------------------------------------------------- Events
    # SECTION Events -----------------------------------------------------
    def eventFilter(self, obj, event):
        event_type = event.type()

        # ---------------------------------------- Keypress
        # NOTE Keypress -----------------------------------
        if event_type == QtCore.QEvent.KeyPress:
            self.priortext = self.ui.title.text()
            if event.key() == QtCore.Qt.Key_Escape:
                self.parentwindow.closeroutine()
                return True
            
        if event_type == QtCore.QEvent.Close:
            self._webview  = None
            self.isediting = True

        return QtCore.QObject.eventFilter(self, obj, event)
