from __future__ import print_function
from __future__ import absolute_import

import hou
import os
from searcher import util
hver = 0
if os.environ["HFS"] != "":
    ver = os.environ["HFS"]
    hver = int(ver[ver.rindex('.')+1:])
    from hutil.Qt import QtGui
else:
    from PyQt5 import QtGui

script_path = os.path.dirname(os.path.realpath(__file__))
PATH = os.path.join(script_path, "images")
imgroot = PATH.replace("\\", "/")

settings = util.get_settings()

def count_chars(txt):
    result = 0
    for char in txt:
        result += 1
    return result

# --------------------------------------------------------------- UI Style
# SECTION UI Style -------------------------------------------------------
# ---------------------------------------------- MAINWINDOW
# NOTE MAINWINDOW -----------------------------------------
MAINWINDOW = """ background-color: rgb(42, 42, 42); """

# ------------------------------------------- CONTEXTTOGGLE
# NOTE CONTEXTTOGGLE --------------------------------------
CONTEXTTOGGLE = """ QPushButton { width: 8px; border: none; }
                    QPushButton:checked { width: 8px; border: none;} """

# ----------------------------------------------- MENUSTYLE
# NOTE MENUSTYLE ------------------------------------------
MENUSTYLE = """QMenu { background-color: rgb(64,64,64); menu-scrollable: 1; margin: 0px; }
                   QMenu:item { background-color: rgb(46,46,46);  padding: 5px 25px; margin: 1px; height:16px; }
                   QMenu:item:selected { background-color: rgb(64,64,64); }
                   QMenu:separator { background-color: rgb(0,0,0); height: 1px; margin: 5px; }
                   QMenu:icon { padding: 5px; }
                   QMenu:icon:checked { flat: true; }"""

# ------------------------------------------------- TOOLTIP
# NOTE TOOLTIP --------------------------------------------
TOOLTIP = """QToolTip { background-color: rgb(64,64,64); menu-scrollable: 1; margin: 0px; }
                   QToolTip:item { background-color: rgb(46,46,46);  padding: 5px 25px ; margin: 1px; height:16px; }
                   QToolTip:icon { padding: 5px; }
                   QToolTip:icon:checked { flat: true; }"""

# --------------------------------------- styleresizehandle
# NOTE styleresizehandle ----------------------------------
def styleresizehandle(obj, enter):
    if enter:
        resizeimg = (imgroot + "/%s.png" % obj.objectName())
        sheet = ""
        sheet += (
        """QSizeGrip {
                background-image: url(%s);
                background-repeat: no-repeat;
                background-position: center;
                padding-bottom: 15px;
                width: 25px;
                height: 25px;
                background-color: rgba(0, 0, 0, 0);
                }""" 
            % resizeimg
            )
        obj.setStyleSheet(sheet)
    else:
        sheet = ""
        sheet += (
        """QSizeGrip {
                image: url(None);
                width: 15px;
                height: 15px;
                background-color: rgba(0, 0, 0, 0);
                }""" 
            )
        obj.setStyleSheet(sheet)

# ----------------------------------------------- INFOLABEL
# NOTE INFOLABEL ------------------------------------------
INFOLABEL = """ background-color: rgba(11,11,11,1); border-bottom: 1px solid rgb(100, 100, 100); """

# -------------------------------------------- SETTINGSMENU
# NOTE SETTINGSMENU ---------------------------------------
SETTINGSMENU = """ QWidget { background: rgb(58, 58, 58); }
                   QWidget#SearcherSettings { border: 0px solid rgb(35, 35, 35); }  """

# ---------------------------------------- styleresulttotal
# NOTE styleresulttotal -----------------------------------
def styleresulttotal(treecatnum, treeitemsnum):
    appcolors = settings[util.SETTINGS_KEYS[14]]
    return (("<font color='%s'><b>%s</b></font> : <font color='%s'>Contexts </font> | " % (appcolors[util.COLORFIELDS[2]], treecatnum, appcolors[util.COLORFIELDS[0]]))
            + ("<font color='%s'><b>%s</b></font> : <font color='%s'>Results </font>  " % (appcolors[util.COLORFIELDS[2]],  treeitemsnum, appcolors[util.COLORFIELDS[0]])))

# --------------------------------------------- styletimers
# NOTE styletimers ----------------------------------------
def styletimers(outdata):
    appcolors = settings[util.SETTINGS_KEYS[14]]
    return (("<font color='%s'>Search Regex <font color='%s'> <b>%0.4f</b> </font> ms</font> | " % (str(appcolors[util.COLORFIELDS[0]]), str(appcolors[util.COLORFIELDS[2]]), outdata[0])) 
              + ("<font color='%s'>Context Search <font color='%s'> <b>%0.4f</b> </font> ms</font> | " % (str(appcolors[util.COLORFIELDS[0]]), str(appcolors[util.COLORFIELDS[2]]), outdata[1])) 
              + ("<font color='%s'>Hotkey Search <font color='%s'> <b>%0.4f</b> </font> ms</font> | " % (str(appcolors[util.COLORFIELDS[0]]), str(appcolors[util.COLORFIELDS[2]]), outdata[2])) 
              + ("<font color='%s'>Tree build <font color='%s'> <b>%0.4f</b> </font> ms</font> | " % (str(appcolors[util.COLORFIELDS[0]]), str(appcolors[util.COLORFIELDS[2]]), outdata[3]))
              + ("<font color='%s'>Total : <font color='%s'> <b>%0.4f</b> </font> ms</font> " % (str(appcolors[util.COLORFIELDS[0]]), str(appcolors[util.COLORFIELDS[2]]), outdata[4])))

# -------------------------------------------- returntimers
# NOTE returntimers ---------------------------------------
def returntimers(outdata):
    return (("Search Regex  %0.4f ms | " % outdata[0])
              + ("Context Search  %0.4f ms | " % outdata[1])
              + ("Hotkey Search  %0.4f ms | " % outdata[2])
              + ("Tree build  %0.4f ms | " % outdata[3])
              + ("Total :  %0.4f ms " % outdata[4]))

# ------------------------------------- gettooltipstyle
# NOTE gettooltipstyle --------------------------------
def gettooltipstyle(text):
    return (("<font color='%s'>%s</font>" % (settings[util.SETTINGS_KEYS[14]][util.COLORFIELDS[4]], text)))

# ---------------------------------------- gettreeviewstyle
# NOTE gettreeviewstyle -----------------------------------
def gettreeviewstyle():
    PATH = os.path.join(script_path, "images")
    root = PATH.replace("\\", "/")

    sheet = ""
    sheet += ("""QTreeWidget { 
            background: rgb(32, 32, 32); 
            alternate-background-color: rgb(39, 39, 39);
            border: 0px solid rgb(19, 19, 19); 
            } """
    )
    sheet += (
        """QHeaderView::section {
                            background: rgb(53, 53, 53); 
                            color: rgb(200, 200, 200); 
                            border: 0px solid rgb(150, 150, 150); 
                            border-bottom: 1px solid rgb(150, 150, 150); 
                            border-left:1px solid rgb(35, 35, 35); 
                            border-right:0px solid rgb(35, 35, 35);
                            height:20px; 
                            resize:both; 
                            overflow:auto; 
                            padding: 4px; 
                        }
        QScrollBar:vertical {
                            background: rgb(19, 19, 19);
                            border: 0px solid rgb(25, 25, 25);
                            width: 10px;
                            margin: 0px 0px 0px 0px;
                        }
        QScrollBar::handle:vertical {
                            background: rgb(53,53,53) 
                        }
        QScrollBar::add-line:vertical {
                            background: rgb(19, 19, 19);
                            border: 0px solid rgb(25, 25, 25);
                            height: 0px;
                            subcontrol-position: bottom;
                            subcontrol-origin: margin;
                        }
        QScrollBar::sub-line:vertical {
                            background: rgb(19, 19, 19);
                            border: 0px solid rgb(25,25,25);
                            height: 0px;
                            subcontrol-position: top;
                            subcontrol-origin: margin;
                        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                            color: rgba(255, 193, 7, 0.8);
                            background: rgb(19, 19, 19);
                            width: 0px;
                            height: 0px;
                        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                            background: none;
                        }
        QScrollBar:horizontal {
                            background: rgb(19, 19, 19);
                            border: 0px solid rgb(25, 25, 25);
                            height: 10px;
                            margin: 0x 0px 0px 0px;
                        }
        QScrollBar::handle:horizontal {
                            background: rgb(53, 53, 53);
                        }
        QScrollBar::add-line:horizontal {
                            background: rgb(19, 19, 19);
                            border: 0px solid rgb(25, 25, 25);
                            width: 0px;
                            subcontrol-position: right;
                            subcontrol-origin: margin;
                        }
        QScrollBar::sub-line:horizontal {
                            background: rgb(19, 19, 19);
                            border: 0px solid rgb(25, 25, 25);
                            width: 0px;
                            subcontrol-position: left;
                            subcontrol-origin: margin;
                        }
        QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                            background: rgb(19, 19, 19);
                            width: 0px;
                            height: 0px;
                        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                            background: none;
                        }
         """
    )
    sheet += (
        """QTreeWidget::item::has-children {
                            text-align: center;  
                            color: %s;  
                            border: 0px solid rgba(71, 71, 71, 0.8); 
                            padding-left: 0px;  padding-bottom: 0px; 
                            padding-top: 0px;  
                            border-radius: 0px;
                        } """
                        % str(settings[util.SETTINGS_KEYS[14]][util.COLORFIELDS[1]])
    )
    sheet += (
        """QTreeWidget::branch:has-siblings:!adjoins-item {
                            border-image: url(%s/icon_vline.png) 0;
                        }"""
        % root
    )
    sheet += ( 
        """QTreeWidget::branch:has-siblings:adjoins-item {
                            border-image: url(%s/icon_branch_more.png) 0; 
                        }""" 
        % root
    )
    sheet += ( 
        """QTreeWidget::branch:!has-children:!has-siblings:adjoins-item {
                            border-image: url(%s/icon_branch_end.png) 0;
                        }""" 
        % root
    )
    sheet += (
        """QTreeWidget::branch:has-children:!has-siblings:closed,"""
    )
    sheet += (
        """QTreeWidget::branch:closed:has-children:has-siblings {
                            margin: 4px; 
                            border-image: none; 
                            image: url(%s/icon_branch_closed.png);
                        }"""
        % root
    )
    sheet += (
        """QTreeWidget::branch:open:has-children:!has-siblings,"""
    )
    sheet += (
        """QTreeWidget::branch:open:has-children:has-siblings {
                            margin: 4px; 
                            border-image: none; 
                            image: url(%s/icon_branch_open.png);
                        }"""
        % root
    )
    sheet += (
        """QTreeWidget::indicator:unchecked {
                            image: url(%s/icon_branch_closed.png); 
                            padding-left: 15px;
                        }"""
        % root
    )
    sheet += (
        """QTreeWidget::indicator:checked {
                            image: url(%s/icon_branch_open.png); 
                            padding-left: 15px;
                        }"""
        % root
    )
    sheet += """QTreeWidget::indicator { 
                            width: 16px; 
                            height: 16px;
                        }"""
    sheet += (
        """QGroupBox::indicator:unchecked {
                            image: url(%s/icon_branch_closed.png); 
                            padding-left: 15px;
                        }"""
        % root
    )
    sheet += (
        """QGroupBox::indicator:checked {
                            image: url(%s/icon_branch_open.png); 
                            padding-left: 15px;
                        }"""
        % root
    )
    sheet += (
        """QGroupBox::indicator { 
                            width: 16px; 
                            height: 16px;
                        }"""
    )

    return sheet

# !SECTION UI Style