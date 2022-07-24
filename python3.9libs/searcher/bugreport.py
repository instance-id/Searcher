from __future__ import absolute_import

from hutil.py23 import reload

from searcher import bugreport_ui
import os

import hou

hver = 0
if os.environ["HFS"] != "":
    ver = os.environ["HFS"]
    # hver = int(ver[ver.rindex('.') + 1:])
    from hutil.Qt import QtGui
    from hutil.Qt import QtCore
    from hutil.Qt import QtWidgets

try:
    pyside = os.environ['HOUDINI_QT_PREFERRED_BINDING']
    parent = hou.qt.mainWindow()
except KeyError:
    parent = hou.ui.mainQtWindow()
    pyside = 'PySide'

if pyside == 'PySide2':
    # noinspection PyUnresolvedReferences
    from PySide2 import QtWebEngineWidgets

elif pyside == 'PySide':
    # noinspection PyUnresolvedReferences
    from PySide.QtWebKit import QWebView

reload(bugreport_ui)

scriptpath = os.path.dirname(os.path.realpath(__file__))


def submittypeswitch(argument):
    switcher = {
        0: "assignees=&labels=bug&template=bug_report.md&title=",
        1: "assignees=&labels=enhancement&template=feature_request.md&title=",
        2: "assignees=&labels=&template=general-question.md&title=",
    }
    return switcher.get(argument, "nothing")


class BugReport(QtWidgets.QWidget):
    """ Searcher Settings and Debug Menu"""

    def __init__(self, parent=None):
        super(BugReport, self).__init__(parent=parent)
        self.priortext = ""
        self.isediting = True
        self.setParent(parent)
        self.parentwindow = parent
        self.ui = bugreport_ui.Ui_BugReport()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self._webview = None
        self.installEventFilter(self)
        self.ui.title.installEventFilter(self)

    def initmenu(self):
        self.resize(self.width(), self.parentwindow.height() - 300)
        self._webview = None
        self.ui.title.setText("")
        self.ui.edittitle_btn.pressed.connect(self.doweb)

        self.ui.title.setFocus()

    def doweb(self):
        if self.ui.title.text() == "":
            self.parentwindow.parentwindow.setstatusmsg("Please enter a title for your bug report", "ImportantMessage")
            if hou.isUIAvailable():
                hou.ui.setStatusMessage(
                    "Please enter a title for your bug report.", severity=hou.severityType.Warning)
            return

        submittype = submittypeswitch(self.ui.label_cbox.currentIndex())
        reporturl = '''https://github.com/instance-id/searcher_addon/issues/new?%s%s''' % (submittype, self.ui.title.text())

        QtGui.QDesktopServices.openUrl(QtCore.QUrl(reporturl))
        self.parentwindow.parentwindow.close()

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
            self._webview = None
            self.isediting = True

        return QtCore.QObject.eventFilter(self, obj, event)
