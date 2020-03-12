from hutil.Qt import QtCore, QtGui, QtWidgets
import os

scriptpath = os.path.dirname(os.path.realpath(__file__))


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
        self.gridLayout = QtWidgets.QGridLayout(About)
        self.gridLayout.setContentsMargins(-1, -1, -1, 6)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        # ------------------------------------------------------ logo
        # NOTE logo -------------------------------------------------
        self.logo = QtWidgets.QLabel(About)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setMaximumSize(QtCore.QSize(170, 170))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(scriptpath + "/images/logo.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.verticalLayout_4.addWidget(self.logo)

        # ------------------------------------------------- headerrow
        # NOTE headerrow --------------------------------------------
        self.headerrow = QtWidgets.QHBoxLayout()
        self.headerrow.setObjectName("headerrow")
        
        self.github = LinkLabel(About, '<a href="http://github.com/instance-id/">github/instance-id</a>')
        self.github.setObjectName("github")
        self.headerrow.addWidget(self.github)
        self.verticalLayout_4.addLayout(self.headerrow)

        # ------------------------------------------------- secondrow
        # NOTE Second Row -------------------------------------------
        self.secondrow = QtWidgets.QHBoxLayout()
        self.secondrow.setObjectName("secondrow")

        self.web = LinkLabel(About, "instance.id")
        self.web.setObjectName("web")
        self.secondrow.addWidget(self.web)
        self.verticalLayout_4.addLayout(self.secondrow)

        # -------------------------------------------------- thirdrow
        # NOTE Third Row --------------------------------------------
        self.thirdrow = QtWidgets.QHBoxLayout()
        self.thirdrow.setObjectName("fifthrow")
        spacerItem2 = QtWidgets.QSpacerItem(40, 2, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.thirdrow.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 2, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.thirdrow.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.thirdrow)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "Form"))
        self.github.setText(_translate("About", '<a href="http://github.com/instance-id/"><font color=#E6E6E6>github/instance-id</font></a>'))
        self.web.setText(_translate("About", '<a href="https://instance.id/"><font color=#E6E6E6>instance.id</font></a>'))

class LinkLabel(QtWidgets.QLabel):
    def __init__(self, parent, text):
        super(LinkLabel, self).__init__(parent)

        self.setText(text)
        self.setTextFormat(QtCore.Qt.RichText)
        self.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)