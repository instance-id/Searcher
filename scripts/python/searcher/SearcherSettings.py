# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SearcherSettings.ui'
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


class Ui_SearcherSettings(object):
    def setupUi(self, SearcherSettings):
        if SearcherSettings.objectName():
            SearcherSettings.setObjectName(u"SearcherSettings")
        SearcherSettings.setWindowModality(Qt.NonModal)
        SearcherSettings.resize(600, 185)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SearcherSettings.sizePolicy().hasHeightForWidth())
        SearcherSettings.setSizePolicy(sizePolicy)
        SearcherSettings.setMinimumSize(QSize(600, 0))
        SearcherSettings.setBaseSize(QSize(0, 0))
        self.gridLayout = QGridLayout(SearcherSettings)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.projectTitle = QLabel(SearcherSettings)
        self.projectTitle.setObjectName(u"projectTitle")
        font = QFont()
        font.setPointSize(15)
        self.projectTitle.setFont(font)
        self.projectTitle.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.projectTitle)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.inmemory_chk = QCheckBox(SearcherSettings)
        self.inmemory_chk.setObjectName(u"inmemory_chk")
        self.inmemory_chk.setLayoutDirection(Qt.RightToLeft)
        self.inmemory_chk.setTristate(False)

        self.horizontalLayout_4.addWidget(self.inmemory_chk)

        self.windowsize_chk = QCheckBox(SearcherSettings)
        self.windowsize_chk.setObjectName(u"windowsize_chk")
        self.windowsize_chk.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_4.addWidget(self.windowsize_chk)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.label_2 = QLabel(SearcherSettings)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.hkinput_txt = QLineEdit(SearcherSettings)
        self.hkinput_txt.setObjectName(u"hkinput_txt")
        self.hkinput_txt.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.hkinput_txt)

        self.hotkey_icon = QToolButton(SearcherSettings)
        self.hotkey_icon.setObjectName(u"hotkey_icon")
        self.hotkey_icon.setPopupMode(QToolButton.InstantPopup)

        self.horizontalLayout_5.addWidget(self.hotkey_icon)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label = QLabel(SearcherSettings)
        self.label.setObjectName(u"label")

        self.horizontalLayout_7.addWidget(self.label)

        self.databasepath_txt = QLineEdit(SearcherSettings)
        self.databasepath_txt.setObjectName(u"databasepath_txt")

        self.horizontalLayout_7.addWidget(self.databasepath_txt)

        self.dbpath_icon = QToolButton(SearcherSettings)
        self.dbpath_icon.setObjectName(u"dbpath_icon")

        self.horizontalLayout_7.addWidget(self.dbpath_icon)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(SearcherSettings)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.test1_btn = QPushButton(SearcherSettings)
        self.test1_btn.setObjectName(u"test1_btn")

        self.horizontalLayout.addWidget(self.test1_btn)

        self.test_context_btn = QPushButton(SearcherSettings)
        self.test_context_btn.setObjectName(u"test_context_btn")

        self.horizontalLayout.addWidget(self.test_context_btn)

        self.cleardata_btn = QPushButton(SearcherSettings)
        self.cleardata_btn.setObjectName(u"cleardata_btn")

        self.horizontalLayout.addWidget(self.cleardata_btn)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(SearcherSettings)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.debugflag_chk = QCheckBox(SearcherSettings)
        self.debugflag_chk.setObjectName(u"debugflag_chk")
        self.debugflag_chk.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_3.addWidget(self.debugflag_chk)

        self.discard_btn = QPushButton(SearcherSettings)
        self.discard_btn.setObjectName(u"discard_btn")

        self.horizontalLayout_3.addWidget(self.discard_btn)

        self.save_btn = QPushButton(SearcherSettings)
        self.save_btn.setObjectName(u"save_btn")

        self.horizontalLayout_3.addWidget(self.save_btn)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.gridLayout.addLayout(self.verticalLayout_4, 1, 0, 1, 1)


        self.retranslateUi(SearcherSettings)

        QMetaObject.connectSlotsByName(SearcherSettings)
    # setupUi

    def retranslateUi(self, SearcherSettings):
        SearcherSettings.setWindowTitle(QCoreApplication.translate("SearcherSettings", u"Form", None))
        self.projectTitle.setText(QCoreApplication.translate("SearcherSettings", u"Searcher Settings", None))
        self.inmemory_chk.setText(QCoreApplication.translate("SearcherSettings", u"Use In-Memory Database", None))
        self.windowsize_chk.setText(QCoreApplication.translate("SearcherSettings", u"Remember Search Window Size", None))
        self.label_2.setText(QCoreApplication.translate("SearcherSettings", u"Hotkey to use for opening unassigned items: ", None))
#if QT_CONFIG(tooltip)
        self.hkinput_txt.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.hkinput_txt.setPlaceholderText(QCoreApplication.translate("SearcherSettings", u"Double Click", None))
        self.hotkey_icon.setText(QCoreApplication.translate("SearcherSettings", u"...", None))
        self.label.setText(QCoreApplication.translate("SearcherSettings", u"Database location: ", None))
        self.dbpath_icon.setText(QCoreApplication.translate("SearcherSettings", u"...", None))
        self.label_4.setText(QCoreApplication.translate("SearcherSettings", u"Maintenance utilities:", None))
        self.test1_btn.setText(QCoreApplication.translate("SearcherSettings", u"Test Button 1", None))
        self.test_context_btn.setText(QCoreApplication.translate("SearcherSettings", u"Test HContext", None))
        self.cleardata_btn.setText(QCoreApplication.translate("SearcherSettings", u"Clear Data", None))
        self.label_3.setText("")
        self.debugflag_chk.setText(QCoreApplication.translate("SearcherSettings", u"Debug Mode", None))
        self.discard_btn.setText(QCoreApplication.translate("SearcherSettings", u"Discard", None))
        self.save_btn.setText(QCoreApplication.translate("SearcherSettings", u"Save", None))
    # retranslateUi

