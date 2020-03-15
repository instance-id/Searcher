from __future__ import print_function
from __future__ import absolute_import

import os
from searcher import util

script_path = os.path.dirname(os.path.realpath(__file__))

settings = util.get_settings()

def count_chars(txt):
    result = 0
    for char in txt:
        result += 1     # same as result = result + 1
    return result

# ------------------------------------------------ UI Style
# NOTE UI Style -------------------------------------------
MENUSTYLE = """QMenu {background-color: rgb(64,64,64); menu-scrollable: 1; margin: 0px;}
                   QMenu:item {background-color: rgb(46,46,46);  padding: 5px 25px; margin: 1px; height:16px;}
                   QMenu:item:selected {background-color: rgb(64,64,64);}
                   QMenu:separator {background-color: rgb(0,0,0); height: 1px; margin: 5px;}
                   QMenu:icon {padding: 5px;}
                   QMenu:icon:checked {flat: true;}"""

TOOLTIP = """QToolTip {background-color: rgb(64,64,64); menu-scrollable: 1; margin: 0px;}
                   QToolTip:item {background-color: rgb(46,46,46);  padding: 5px 25px; margin: 1px; height:16px;}
                   QToolTip:icon {padding: 5px;}
                   QToolTip:icon:checked {flat: true;}"""

def styleresulttotal(appcolors, treecatnum, treeitemsnum, goalnum):
    catval = ("<font color='%s'>%d</font> : <font color='%s'>Contexts</font> | " % (appcolors.stats1, treecatnum, appcolors.text1 ))
    itmval = ("<font color='%s'>%d</font> : <font color='%s'>Results</font>  " % (appcolors.stats1,  treeitemsnum, appcolors.text1))
    catval = catval.rjust(goalnum - count_chars(str(treecatnum)), " ")
    itmval = itmval.rjust((goalnum + 2) - count_chars(str(treeitemsnum)), " ")
    return (catval + itmval)

def styletimers(appcolors, outdata):
    return (("<font color='%s'>Search regex <font color='%s'> %0.4f </font> ms</font> | " % (str(appcolors.text1), str(appcolors.stats1), outdata[0])) 
              + ("<font color='%s'>Context Search <font color='%s'> %0.4f </font> ms</font> | " % (str(appcolors.text1), str(appcolors.stats1), outdata[1])) 
              + ("<font color='%s'>Hotkey Search <font color='%s'> %0.4f </font> ms</font> | " % (str(appcolors.text1), str(appcolors.stats1), outdata[2])) 
              + ("<font color='%s'>Tree build <font color='%s'> %0.4f </font> ms</font> | " % (str(appcolors.text1), str(appcolors.stats1), outdata[3]))
              + ("<font color='%s'>Total : <font color='%s'> %0.4f </font> ms</font> " % (str(appcolors.text1), str(appcolors.stats1), outdata[4])))



def gettreeviewstyle():
    PATH = os.path.join(script_path, "images")
    root = PATH.replace("\\", "/")
    sheet = ""
    sheet += (
        "QTreeWidget { background: rgb(32, 32, 32); alternate-background-color: rgb(39, 39, 39) \n} "
    )
    sheet += (
        """QHeaderView::section {\n 
        background: rgb(53, 53, 53); 
        color: rgb(200, 200, 200); 
        resize:both; 
        overflow:auto; 
        padding: 4px; 
        height:20px; 
        border: 
        0px solid rgb(150, 150, 150); 
        border-bottom: 1px solid rgb(150, 150, 150); 
        border-left:0px solid rgb(25, 25, 25); 
        border-right:1px solid rgb(35, 35, 35) \n}\n

        QScrollBar::vertical { \n width: 12px; \n } \n
        QScrollBar::handle:vertical {\n background: rgb(19,19,19) \n}\n
         """
    )
    sheet += (
        "QTreeWidget::item::has-children { text-align: center;  color: rgba(255, 193, 7, 0.8);  border: 0px solid rgba(71, 71, 71, 0.8);  padding-bottom: 0px; padding-top: 0px;  border-radius: 0px; \n} "
    )
    sheet += (
        "QTreeWidget::branch:has-siblings:!adjoins-item\n {\n border-image: url(%s/icon_vline.png) 0; \n}"
        % root
    )
    sheet += ( 
        "QTreeWidget::branch:has-siblings:adjoins-item\n {\n border-image: url(%s/icon_branch_more.png) 0; \n}" 
        % root
    )
    sheet += ( 
        "QTreeWidget::branch:!has-children:!has-siblings:adjoins-item\n {\n border-image: url(%s/icon_branch_end.png) 0; \n}" 
        % root
    )
    sheet += (
        "QTreeWidget::branch:has-children:!has-siblings:closed,"
        )
    sheet += (
        "QTreeWidget::branch:closed:has-children:has-siblings\n {\n margin: 4px; border-image: none; image: url(%s/icon_branch_closed.png); \n}"
        % root
    )
    sheet += (
        "QTreeWidget::branch:open:has-children:!has-siblings,")
    sheet += (
        "QTreeWidget::branch:open:has-children:has-siblings\n {\n margin: 4px; border-image: none; image: url(%s/icon_branch_open.png); \n}"
        % root
    )
    sheet += (
        "QTreeWidget::indicator:unchecked\n {\n image: url(%s/icon_branch_closed.png); \n}"
        % root
    )
    sheet += (
        "QTreeWidget::indicator:checked\n {\n image: url(%s/icon_branch_open.png); \n}"
        % root
    )
    sheet += "QTreeWidget::indicator { width: 16px; height: 16px;}"
    sheet += (
        "QGroupBox::indicator:unchecked\n {\n image: url(%s/icon_branch_closed.png); \n}"
        % root
    )
    sheet += (
        "QGroupBox::indicator:checked\n {\n image: url(%s/icon_branch_open.png); \n}"
        % root
    )
    sheet += "QGroupBox::indicator { width: 16px; height: 16px;}"

    return sheet
