from __future__ import print_function
from __future__ import absolute_import

import os
import sys
from searcher import HelpButton
from searcher import language_en as la

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


# noinspection PyAttributeOutsideInit
class Ui_Searcher(object):
    def setupUi(self, Searcher, animated):
        self.animated = animated
        Searcher.setObjectName("Searcher")
        Searcher.setWindowModality(QtCore.Qt.NonModal)
        Searcher.setStyleSheet(u"background-color: rgb(42,42,42); border: 0px solid black")

        self.mainlayout = QtWidgets.QVBoxLayout()
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)

        self.titlerow = QtWidgets.QHBoxLayout()
        self.titlerow.setSpacing(5)

        self.titlespacer1 = QtWidgets.QSpacerItem(
            8, 0,
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Minimum
        )

        # ------------------------------------------ Header
        # NOTE Header -------------------------------------
        self.searcherlbl = QtWidgets.QLabel("Searcher")
        font = QtGui.QFont()
        font.setPointSize(15)
        self.searcherlbl.setFont(font)
        self.searcherlbl.setAlignment(QtCore.Qt.AlignCenter)

        self.titlespacer2 = QtWidgets.QSpacerItem(
            40, 30,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )

        self.expander = QtWidgets.QToolButton()
        self.expander.setObjectName("expander")

        self.metricpos = QtWidgets.QToolButton()
        self.metricpos.setObjectName("metricpos")

        self.contexttoggle = QtWidgets.QPushButton()
        self.contexttoggle.setObjectName("contexttoggle")

        self.helpButton = HelpButton.HelpButton("main", la.TT_MW['helpButton'], 16)
        self.helpButton.setObjectName("helpButton")

        self.pinwindow_btn = QtWidgets.QToolButton()
        self.pinwindow_btn.setObjectName("pinwindow")

        self.opensettings_btn = QtWidgets.QToolButton()
        self.opensettings_btn.setObjectName("opensettingstool")

        self.titlespacer3 = QtWidgets.QSpacerItem(
            8, 0,
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Minimum
        )

        # ----------------------------------- Search Filter
        # NOTE Search Filter ------------------------------
        self.searchrow = QtWidgets.QHBoxLayout()
        self.searchrow.setSpacing(0)
        self.frame = QtWidgets.QFrame()
        searchframe_details = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Preferred
        )
        searchframe_details.setHorizontalStretch(0)
        searchframe_details.setVerticalStretch(0)
        searchframe_details.setHeightForWidth(
            self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(searchframe_details)
        self.frame.setMinimumSize(QtCore.QSize(20, 20))
        self.frame.setMaximumSize(QtCore.QSize(500, 200))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setStyleSheet(u"background-color: rgb(19, 19, 19); color: rgb(19, 19, 19);")
        self.searchfilter_btn = QtWidgets.QToolButton(self.frame)
        self.searchfilter_btn.setObjectName("searchfilter")
        self.searchfilter_btn.setGeometry(QtCore.QRect(0, 0, 36, 36))
        self.searchfilter_btn.setBaseSize(QtCore.QSize(30, 30))
        self.searchfilter_btn.setStyleSheet(u"background-color: rgb(19, 19, 19);")
        self.searchfilter_btn.setArrowType(QtCore.Qt.NoArrow)
        self.searchfilter_btn.setParent(self.frame)

        # -------------------------------------- Search Box
        # NOTE Search Box ---------------------------------
        self.searchbox_txt = QtWidgets.QLineEdit()
        self.searchbox_txt.setObjectName("searchbox")
        searchbox_details = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        searchbox_details.setHorizontalStretch(99)
        searchbox_details.setVerticalStretch(0)
        # searchbox_details.setHeightForWidth(
        #     self.searchbox_txt.sizePolicy().hasHeightForWidth())
        self.searchbox_txt.setSizePolicy(searchbox_details)
        self.searchbox_txt.setMinimumSize(QtCore.QSize(50, 0))
        self.searchbox_txt.setMouseTracking(False)
        self.searchbox_txt.setStyleSheet(u"background-color: rgb(19, 19, 19);")
        self.searchbox_txt.setFrame(False)

        # ------------------------------------ Results Tree
        # NOTE Results Tree -------------------------------
        self.searchresults_tree = QtWidgets.QTreeWidget()
        self.searchresults_tree.setObjectName("searchresultstree")

        # Header ---------
        __qtreewidgetitem = QtWidgets.QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1")
        resultstree_header = QtGui.QFont()
        resultstree_header.setPointSize(9)
        __qtreewidgetitem.setFont(0, resultstree_header)
        self.searchresults_tree.setHeaderItem(__qtreewidgetitem)

        resultstree_details = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding
        )
        resultstree_details.setHorizontalStretch(0)
        resultstree_details.setVerticalStretch(0)
        self.searchresults_tree.setSizePolicy(resultstree_details)

        resultstree_font = QtGui.QFont()
        resultstree_font.setPointSize(9)
        self.searchresults_tree.setFont(resultstree_font)

        self.searchresults_tree.setMouseTracking(False)
        self.searchresults_tree.setFocusPolicy(QtCore.Qt.NoFocus)
        self.searchresults_tree.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.searchresults_tree.setLineWidth(0)

        self.searchresults_tree.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.searchresults_tree.setAlternatingRowColors(True)
        self.searchresults_tree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.searchresults_tree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # -------------------------------------- Info Panel
        # NOTE Info Panel ---------------------------------
        self.infobar = QtWidgets.QHBoxLayout()
        self.infobar.setObjectName("infobar")
        self.infobargrid = QtWidgets.QGridLayout()
        self.infobargrid.setObjectName("infobargrid")

        # -------------------------------------- Info Panel
        # NOTE Info Panel ---------------------------------
        self.info_lbl = QtWidgets.QLabel()
        self.infolbl_font = QtGui.QFont()
        self.infolbl_font.setPointSize(9)
        self.infolbl_font.setBold(False)
        self.infolbl_font.setWeight(40)
        self.info_lbl.setFont(self.infolbl_font)
        self.info_lbl.setStyleSheet(
            u"background-color: rgba(11, 11, 11, 0); border-bottom: 1px solid rgb(100, 100, 100);")
        self.info_lbl.setMargin(3)
        self.info_lbl.setIndent(5)

        # -------------------------------------- Info Panel
        # NOTE Info Panel ---------------------------------
        self.overlay = overlayLabel(self.info_lbl)
        self.overlay.setFont(self.infolbl_font)
        self.overlay.setStyleSheet(u"background-color: rgb(11, 11, 11); border-bottom: 1px solid rgb(100, 100, 100); ")
        self.overlay.setMargin(3)
        self.overlay.setIndent(5)

        # -------------------------------------- Info Panel
        # NOTE Info Panel ---------------------------------
        self.treetotal_lbl = QtWidgets.QLabel()
        self.treetotal_lbl.setObjectName("treetotal_lbl")
        # Size ----------
        treetotal_size = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        treetotal_size.setHorizontalStretch(0)
        treetotal_size.setVerticalStretch(0)
        treetotal_size.setHeightForWidth(self.treetotal_lbl.sizePolicy().hasHeightForWidth())
        self.treetotal_lbl.setSizePolicy(treetotal_size)
        self.treetotal_lbl.setMinimumSize(QtCore.QSize(160, 0))
        self.treetotal_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        # Style ---------
        self.treetotallbl_font = QtGui.QFont()
        self.treetotallbl_font.setPointSize(9)
        self.treetotallbl_font.setBold(False)
        self.treetotallbl_font.setWeight(50)
        self.treetotal_lbl.setFont(self.treetotallbl_font)
        self.treetotal_lbl.setStyleSheet(
            u"background-color: rgb(11, 11, 11); border-bottom: 1px solid rgb(100, 100, 100); ")
        self.treetotal_lbl.setMargin(3)
        self.treetotal_lbl.setIndent(5)

        # ------------------------------------------ Layout
        # NOTE Layout -------------------------------------
        self.titlerow.addItem(self.titlespacer1)
        self.titlerow.addWidget(self.searcherlbl)
        self.titlerow.addItem(self.titlespacer2)
        self.titlerow.addWidget(self.expander)
        self.titlerow.addWidget(self.metricpos)
        self.titlerow.addWidget(self.contexttoggle)
        self.titlerow.addWidget(self.helpButton)
        self.titlerow.addWidget(self.pinwindow_btn)
        self.titlerow.addWidget(self.opensettings_btn)
        self.titlerow.addItem(self.titlespacer3)
        self.verticalLayout.addLayout(self.titlerow)

        # self.searchrow.addWidget(self.frame)
        self.searchgrid = QtWidgets.QGridLayout()
        self.searchgrid.addWidget(self.frame, 1, 0, 1, 1)
        self.searchgrid.addWidget(self.searchfilter_btn, 1, 0, 1, 1)
        self.searchgrid.addWidget(self.searchbox_txt, 1, 1, 1, 1)
        self.searchrow.addLayout(self.searchgrid)
        self.verticalLayout.addLayout(self.searchrow)

        self.verticalLayout.addWidget(self.searchresults_tree)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.infobargrid.addWidget(self.overlay, 1, 0, 1, 1)
        self.infobargrid.addWidget(self.info_lbl, 1, 0, 1, 1)
        self.infobargrid.addWidget(self.treetotal_lbl, 1, 1, 1, 1)
        self.infobar.addLayout(self.infobargrid)
        self.gridLayout.addLayout(self.infobar, 3, 0, 1, 1)

        self.mainlayout.setContentsMargins(0, 0, 0, 0)

        # --------------------------------------- ResizeHandles
        # NOTE ResizeHandles ----------------------------------
        self.leftresize = QtWidgets.QSizeGrip(self.info_lbl)
        self.leftresize.setObjectName("resizeleft")
        self.leftresize.setMaximumSize(QtCore.QSize(25, 25))
        self.leftresize.setStyleSheet(u"color: rgba(0, 0, 0, 0); background-color: rgba(0, 0, 0, 0);")
        pos = self.info_lbl.mapToGlobal(
            QtCore.QPoint(-3, 0))
        self.leftresize.setGeometry(
            pos.x(),
            pos.y(),
            self.leftresize.width(),
            self.leftresize.height()
        )

        self.rightresize = QtWidgets.QSizeGrip(self.treetotal_lbl)
        self.rightresize.setMaximumSize(QtCore.QSize(25, 25))
        self.rightresize.setObjectName("resizeright")
        self.rightresize.setStyleSheet(u"color: rgba(0, 0, 0, 0); background-color: rgba(0, 0, 0, 0);")
        pos = self.treetotal_lbl.mapToGlobal(
            QtCore.QPoint(138, 0))
        self.rightresize.setGeometry(
            pos.x(),
            pos.y(),
            self.rightresize.width(),
            self.rightresize.height()
        )
        self.vlayout = self.gridLayout
        # self.mainlayout.addLayout(self.gridLayout)


class overlayLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(overlayLabel, self).__init__(parent)
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
