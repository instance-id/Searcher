from __future__ import absolute_import
from searcher import about_ui
from searcher import util
import os

hver = 0
if os.environ["HFS"] != "":
    ver = os.environ["HFS"]
    # hver = int(ver[ver.rindex('.')+1:])
    from hutil.Qt import QtGui
    from hutil.Qt import QtCore
    from hutil.Qt import QtWidgets

scriptpath = os.path.dirname(os.path.realpath(__file__))


class About(QtWidgets.QWidget):
    """ Searcher Settings and Debug Menu"""

    def __init__(self, parent=None):
        super(About, self).__init__(parent=parent)
        self.setParent(parent)
        self.parentwindow = parent
        self.ui = about_ui.Ui_About()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.ui.github.mousePressEvent = self.openGithub
        self.ui.web.mousePressEvent = self.openWeb

        self.installEventFilter(self)

    def initmenu(self):
        return

    def openGithub(self, event):
        ghurl = '''https://github.com/instance-id/'''
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(ghurl))
        self.parentwindow.parentwindow.close()

    def openWeb(self, event):
        weburl = '''https://instance.id/'''
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(weburl))
        self.parentwindow.parentwindow.close()

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
