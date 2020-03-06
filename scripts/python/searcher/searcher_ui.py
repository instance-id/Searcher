# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'searcher_ui.ui'
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

from .HelpButton import HelpButton


class Ui_Searcher(object):
    def setupUi(self, Searcher):
        if Searcher.objectName():
            Searcher.setObjectName(u"Searcher")
        Searcher.setWindowModality(Qt.WindowModal)
        Searcher.resize(1000, 329)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Searcher.sizePolicy().hasHeightForWidth())
        Searcher.setSizePolicy(sizePolicy)
        Searcher.setMinimumSize(QSize(0, 0))
        Searcher.setBaseSize(QSize(1000, 350))
        Searcher.setStyleSheet(u"QTreeWidget QHeaderView::section {\n"
"    font-size: 9pt;\n"
"}")
        self.gridLayout = QGridLayout(Searcher)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(8, 2, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.projectTitle = QLabel(Searcher)
        self.projectTitle.setObjectName(u"projectTitle")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.projectTitle.sizePolicy().hasHeightForWidth())
        self.projectTitle.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(15)
        self.projectTitle.setFont(font)
        self.projectTitle.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.projectTitle)

        self.horizontalSpacer = QSpacerItem(40, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.HelpButton = HelpButton(Searcher)
        self.HelpButton.setObjectName(u"HelpButton")

        self.horizontalLayout.addWidget(self.HelpButton)

        self.pinwindow_btn = QToolButton(Searcher)
        self.pinwindow_btn.setObjectName(u"pinwindow_btn")

        self.horizontalLayout.addWidget(self.pinwindow_btn)

        self.opensettings_btn = QToolButton(Searcher)
        self.opensettings_btn.setObjectName(u"opensettings_btn")

        self.horizontalLayout.addWidget(self.opensettings_btn)

        self.horizontalSpacer_3 = QSpacerItem(8, 2, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.frame = QFrame(Searcher)
        self.frame.setObjectName(u"frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(2)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setMinimumSize(QSize(0, 20))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.searchfilter_btn = QToolButton(self.frame)
        self.searchfilter_btn.setObjectName(u"searchfilter_btn")
        self.searchfilter_btn.setGeometry(QRect(0, 0, 26, 20))
        self.searchfilter_btn.setBaseSize(QSize(16, 16))
        self.searchfilter_btn.setStyleSheet(u"background-color: rgb(19, 19, 19);")
        self.searchfilter_btn.setArrowType(Qt.NoArrow)

        self.horizontalLayout_3.addWidget(self.frame)

        self.searchbox_txt = QLineEdit(Searcher)
        self.searchbox_txt.setObjectName(u"searchbox_txt")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(99)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.searchbox_txt.sizePolicy().hasHeightForWidth())
        self.searchbox_txt.setSizePolicy(sizePolicy3)
        self.searchbox_txt.setMinimumSize(QSize(50, 0))
        self.searchbox_txt.setMouseTracking(False)
        self.searchbox_txt.setStyleSheet(u"background-color: rgb(19, 19, 19);")
        self.searchbox_txt.setFrame(False)

        self.horizontalLayout_3.addWidget(self.searchbox_txt)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.searchresults_tree = QTreeWidget(Searcher)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.searchresults_tree.setHeaderItem(__qtreewidgetitem)
        self.searchresults_tree.setObjectName(u"searchresults_tree")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.searchresults_tree.sizePolicy().hasHeightForWidth())
        self.searchresults_tree.setSizePolicy(sizePolicy4)
        font1 = QFont()
        font1.setPointSize(9)
        self.searchresults_tree.setFont(font1)
        self.searchresults_tree.setMouseTracking(False)
        self.searchresults_tree.setFocusPolicy(Qt.NoFocus)
        self.searchresults_tree.setFrameShadow(QFrame.Sunken)
        self.searchresults_tree.setLineWidth(0)
        self.searchresults_tree.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.searchresults_tree.setAlternatingRowColors(True)
        self.searchresults_tree.setSelectionMode(QAbstractItemView.SingleSelection)
        self.searchresults_tree.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout.addWidget(self.searchresults_tree)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.info_lbl = QLabel(Searcher)
        self.info_lbl.setObjectName(u"info_lbl")
        font2 = QFont()
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setWeight(50)
        self.info_lbl.setFont(font2)
        self.info_lbl.setStyleSheet(u"background-color: rgb(26, 26, 26);")
        self.info_lbl.setMargin(2)
        self.info_lbl.setIndent(5)

        self.gridLayout.addWidget(self.info_lbl, 2, 0, 1, 1)


        self.retranslateUi(Searcher)

        QMetaObject.connectSlotsByName(Searcher)
    # setupUi

    def retranslateUi(self, Searcher):
        Searcher.setWindowTitle(QCoreApplication.translate("Searcher", u"Searcher", None))
        self.projectTitle.setText(QCoreApplication.translate("Searcher", u"Searcher", None))
        self.HelpButton.setText(QCoreApplication.translate("Searcher", u"...", None))
        self.pinwindow_btn.setText(QCoreApplication.translate("Searcher", u"...", None))
        self.opensettings_btn.setText(QCoreApplication.translate("Searcher", u"...", None))
        self.searchfilter_btn.setText(QCoreApplication.translate("Searcher", u"...", None))
        self.info_lbl.setText(QCoreApplication.translate("Searcher", u"Begin typing to search or click magnifying glass icon to display options", None))
    # retranslateUi

