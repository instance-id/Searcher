# -*- coding: utf-8 -*-
import os
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


# noinspection PyAttributeOutsideInit,DuplicatedCode,PyPep8Naming
class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.setWindowModality(QtCore.Qt.NonModal)
        About.resize(185, 251)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(About.sizePolicy().hasHeightForWidth())
        About.setSizePolicy(sizePolicy)
        About.setMinimumSize(QtCore.QSize(100, 0))
        About.setBaseSize(QtCore.QSize(0, 0))
        About.setStyleSheet("")

        # ------------------------------------------------- gridsetup
        # NOTE gridsetup --------------------------------------------
        self.gridLayout = QtWidgets.QGridLayout(About)
        self.gridLayout.setContentsMargins(-1, -1, -1, 6)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        # ------------------------------------------------- secondrow
        # NOTE Second Row -------------------------------------------
        self.secondrow = QtWidgets.QHBoxLayout()
        self.secondrow.setObjectName("secondrow")
        self.web_icon = QtWidgets.QToolButton(About)
        self.web_icon.setObjectName("web_icon")
        self.web = QtWidgets.QLabel(About)
        self.web.setObjectName("web")
        self.secondrow.addWidget(self.web_icon)
        self.secondrow.addWidget(self.web)
        self.verticalLayout.addLayout(self.secondrow)

        # -------------------------------------------------- thirdrow
        # NOTE Third Row --------------------------------------------
        self.thirdrow = QtWidgets.QHBoxLayout()
        self.thirdrow.setObjectName("thirdrow")
        self.github_icon = QtWidgets.QToolButton(About)
        self.github_icon.setObjectName("github_icon")
        self.github = QtWidgets.QLabel(About)
        self.github.setObjectName("github")
        self.thirdrow.addWidget(self.github_icon)
        self.thirdrow.addWidget(self.github)
        self.verticalLayout.addLayout(self.thirdrow)

        # ------------------------------------------------- fourthrow
        # NOTE fourthrow --------------------------------------------
        self.fourthrow = QtWidgets.QHBoxLayout()
        self.fourthrow.setObjectName("fourthrow")
        self.twitter_icon = QtWidgets.QToolButton(About)
        self.twitter_icon.setObjectName("twitter_icon")
        self.twitter = QtWidgets.QLabel(About)
        self.twitter.setObjectName("twitter")
        self.fourthrow.addWidget(self.twitter_icon)
        self.fourthrow.addWidget(self.twitter)
        self.verticalLayout.addLayout(self.fourthrow)

        # ------------------------------------------------- fifthrow
        # NOTE fifthrow --------------------------------------------
        self.fifthrow = QtWidgets.QHBoxLayout()
        self.fifthrow.setObjectName("fifthrow")
        self.email_icon = QtWidgets.QToolButton(About)
        self.email_icon.setObjectName("email_icon")
        self.email = QtWidgets.QLabel(About)
        self.email.setObjectName("email")
        self.fifthrow.addWidget(self.email_icon)
        self.fifthrow.addWidget(self.email)
        self.verticalLayout.addLayout(self.fifthrow)

        # ----------------------------------------------- columnsetup
        # NOTE columnsetup ------------------------------------------
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        # ----------------------------------------------------- image
        # NOTE image --- --------------------------------------------
        self.logo = QtWidgets.QLabel(About)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setMaximumSize(QtCore.QSize(120, 120))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(scriptpath + "/images/logo.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.gridLayout.addWidget(self.logo, 0, 1, 1, 1)

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "Form"))
        self.web.setText(_translate("About", '<a href="https://instance.id/"><font color=#E6E6E6>website</font></a>'))
        self.github.setText(_translate("About", '<a href="http://github.com/instance-id/"><font color=#E6E6E6>github</font></a>'))
        self.twitter.setText(_translate("About", '<a href="https://twitter.com/instance_id"><font color=#E6E6E6>twitter</font></a>'))
        self.email.setText(_translate("About", '<a href="mailto:support@instance.id"><font color=#E6E6E6>email</font></a>'))

# class LinkLabel(QtWidgets.QLabel):
#     def __init__(self, parent, text):
#         super(LinkLabel, self).__init__(parent)

#         self.setText(text)
#         self.setTextFormat(QtCore.Qt.RichText)
#         self.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
#         self.setOpenExternalLinks(True)