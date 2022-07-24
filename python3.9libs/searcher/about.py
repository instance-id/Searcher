from __future__ import absolute_import
from searcher import about_ui
from searcher import util
import os
import hou

hver = 0
if os.environ["HFS"] != "":
    ver = os.environ["HFS"]
    # hver = int(ver[ver.rindex('.')+1:])
    from hutil.Qt import QtGui
    from hutil.Qt import QtCore
    from hutil.Qt import QtWidgets
else:
    from qtpy import QtGui
    from qtpy import QtCore
    from qtpy import QtWidgets

scriptpath = os.path.dirname(os.path.realpath(__file__))


# noinspection PyCallByClass,PyUnresolvedReferences
class About(QtWidgets.QWidget):
    """ Searcher Settings and Debug Menu"""

    def __init__(self, parent=None):
        super(About, self).__init__(parent=parent)
        self.setParent(parent)
        self.parentwindow = parent
        self.ui = about_ui.Ui_About()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.ui.web_icon.setIcon(hou.qt.createIcon(
            util.get_path(["images", "icons", "firefox-browser-brands.svg"])))
        self.ui.web_icon.clicked.connect(self.openWeb)
        web_icon_size = hou.ui.scaledSize(16)
        self.ui.web_icon.setProperty("flat", True)
        self.ui.web_icon.setIconSize(QtCore.QSize(
            web_icon_size,
            web_icon_size
        ))

        self.ui.github_icon.setIcon(hou.qt.createIcon(
            util.get_path(["images", "icons", "github-brands.svg"])))
        self.ui.github_icon.clicked.connect(self.openGithub)
        github_icon_size = hou.ui.scaledSize(16)
        self.ui.github_icon.setProperty("flat", True)
        self.ui.github_icon.setIconSize(QtCore.QSize(
            github_icon_size,
            github_icon_size
        ))

        self.ui.twitter_icon.setIcon(hou.qt.createIcon(
            util.get_path(["images", "icons", "twitter-brands.svg"])))
        self.ui.twitter_icon.clicked.connect(self.openTwitter)
        twitter_icon_size = hou.ui.scaledSize(16)
        self.ui.twitter_icon.setProperty("flat", True)
        self.ui.twitter_icon.setIconSize(QtCore.QSize(
            twitter_icon_size,
            twitter_icon_size
        ))

        self.ui.email_icon.setIcon(hou.qt.createIcon(
            util.get_path(["images", "icons", "at-solid.svg"])))
        self.ui.email_icon.clicked.connect(self.openEmail)
        email_icon_size = hou.ui.scaledSize(16)
        self.ui.email_icon.setProperty("flat", True)
        self.ui.email_icon.setIconSize(QtCore.QSize(
            email_icon_size,
            email_icon_size
        ))

        self.ui.web.mousePressEvent = self.openWeb
        self.ui.github.mousePressEvent = self.openGithub
        self.ui.twitter.mousePressEvent = self.openTwitter
        self.ui.email.mousePressEvent = self.openEmail

        self.installEventFilter(self)

    def initmenu(self):
        return

    def openWeb(self, _):
        weburl = '''https://instance.id/'''
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(weburl))
        self.parentwindow.parentwindow.close()

    def openGithub(self, _):
        ghurl = '''https://github.com/instance-id/'''
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(ghurl))
        self.parentwindow.parentwindow.close()

    def openTwitter(self, _):
        twitterurl = '''https://twitter.com/instance_id'''
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(twitterurl))
        self.parentwindow.parentwindow.close()

    def openEmail(self, _):
        email = '''mailto:support@instance.id'''
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(email))
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
