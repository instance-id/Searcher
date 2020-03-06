# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'searcher_util.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Searcher(object):
    def setupUi(self, Searcher):
        if Searcher.objectName():
            Searcher.setObjectName(u"Searcher")
        Searcher.setWindowModality(Qt.NonModal)
        Searcher.resize(1000, 113)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Searcher.sizePolicy().hasHeightForWidth())
        Searcher.setSizePolicy(sizePolicy)
        Searcher.setMinimumSize(QSize(0, 0))
        Searcher.setBaseSize(QSize(1000, 350))
        self.gridLayout = QGridLayout(Searcher)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.projectTitle = QLabel(Searcher)
        self.projectTitle.setObjectName(u"projectTitle")
        font = QFont()
        font.setPointSize(15)
        self.projectTitle.setFont(font)
        self.projectTitle.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.projectTitle)

        self.gocommand_txt = QLineEdit(Searcher)
        self.gocommand_txt.setObjectName(u"gocommand_txt")

        self.horizontalLayout_4.addWidget(self.gocommand_txt)

        self.sendgocommand_btn = QPushButton(Searcher)
        self.sendgocommand_btn.setObjectName(u"sendgocommand_btn")

        self.horizontalLayout_4.addWidget(self.sendgocommand_btn)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.opensearchwindow_btn = QPushButton(Searcher)
        self.opensearchwindow_btn.setObjectName(u"opensearchwindow_btn")

        self.horizontalLayout.addWidget(self.opensearchwindow_btn)

        self.gethotkeys_btn = QPushButton(Searcher)
        self.gethotkeys_btn.setObjectName(u"gethotkeys_btn")

        self.horizontalLayout.addWidget(self.gethotkeys_btn)

        self.updatehotkeys_btn = QPushButton(Searcher)
        self.updatehotkeys_btn.setObjectName(u"updatehotkeys_btn")

        self.horizontalLayout.addWidget(self.updatehotkeys_btn)

        self.loadhotkeys_btn = QPushButton(Searcher)
        self.loadhotkeys_btn.setObjectName(u"loadhotkeys_btn")

        self.horizontalLayout.addWidget(self.loadhotkeys_btn)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout_4, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.callgo_btn = QPushButton(Searcher)
        self.callgo_btn.setObjectName(u"callgo_btn")

        self.horizontalLayout_2.addWidget(self.callgo_btn)

        self.other_btn = QPushButton(Searcher)
        self.other_btn.setObjectName(u"other_btn")

        self.horizontalLayout_2.addWidget(self.other_btn)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)


        self.retranslateUi(Searcher)

        QMetaObject.connectSlotsByName(Searcher)
    # setupUi

    def retranslateUi(self, Searcher):
        Searcher.setWindowTitle(QCoreApplication.translate("Searcher", u"Form", None))
        self.projectTitle.setText(QCoreApplication.translate("Searcher", u"Searcher Settings", None))
        self.sendgocommand_btn.setText(QCoreApplication.translate("Searcher", u"Send Go Cmd", None))
        self.opensearchwindow_btn.setText(QCoreApplication.translate("Searcher", u"Open Search", None))
        self.gethotkeys_btn.setText(QCoreApplication.translate("Searcher", u"Get Hotkeys", None))
        self.updatehotkeys_btn.setText(QCoreApplication.translate("Searcher", u"Update HotKeys", None))
        self.loadhotkeys_btn.setText(QCoreApplication.translate("Searcher", u"Load Hotkeys", None))
        self.callgo_btn.setText(QCoreApplication.translate("Searcher", u"Call Go", None))
        self.other_btn.setText(QCoreApplication.translate("Searcher", u"Clear Data", None))
    # retranslateUi

