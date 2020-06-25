from hutil.Qt import QtCore, QtGui, QtWidgets
import os

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
        self.secondrow = QtWidgets.QHBoxLayout()
        self.secondrow.setObjectName("secondrow")
        self.web = QtWidgets.QLabel(About)
        self.web.setObjectName("web")
        # self.web.setOpenExternalLinks(True)
        self.secondrow.addWidget(self.web)
        self.verticalLayout.addLayout(self.secondrow)
        self.headerrow = QtWidgets.QHBoxLayout()
        self.headerrow.setObjectName("headerrow")
        self.github = QtWidgets.QLabel(About)
        self.github.setObjectName("github")
        # self.github.setOpenExternalLinks(True)
        self.headerrow.addWidget(self.github)
        self.verticalLayout.addLayout(self.headerrow)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
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
        self.github.setText(_translate("About", '<a href="http://github.com/instance-id/"><font color=#E6E6E6>github/instance-id</font></a>'))
        self.web.setText(_translate("About", '<a href="https://instance.id/"><font color=#E6E6E6>instance.id</font></a>'))

# class LinkLabel(QtWidgets.QLabel):
#     def __init__(self, parent, text):
#         super(LinkLabel, self).__init__(parent)

#         self.setText(text)
#         self.setTextFormat(QtCore.Qt.RichText)
#         self.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
#         self.setOpenExternalLinks(True)