from __future__ import print_function
from __future__ import absolute_import

import hou
import os

from searcher import util
from searcher import searcher_data
from searcher import ptime as ptime
from searcher import database

import os
import threading
import hdefereval as hd

reload(database)

def get_db():
    return getattr(hou.session, "DATABASE", None)

def worker():
    hd.executeInMainThreadWithResult(DataHandler().updatedata)


class DataHandler(object):
    """Searcher data and communication handler"""

    def __init__(self, debug=None):
        self.db = get_db()
        if not self.db:
            hou.session.DATABASE = database.Databases()
            self.db = get_db()
            
        self.isdebug = debug
        self.scriptpath = os.path.dirname(os.path.realpath(__file__))
    # SECTION Function calls ------------------------------ Function calls
    # -------------------------------------------- Retrieve
    # NOTE Retrieve ---------------------------------------

    def getchangeindex(self):
        index = self.db.getchangeindex()
        return index

    def getdefaulthotkey(self):
        index = self.db.getdefhotkey()
        return index

    # --------------------------------------------- Updates
    # NOTE Updates ----------------------------------------
    def updatechangeindex(self, indexval, new=False):
        self.db.updatechangeindex(indexval, new)
        return

    def updatedataasync(self, debug):
        self.isdebug = debug
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()

    def updatedata(self):
        self.db.updatecontext(self.isdebug)
        return

    def updatetmphotkey(self, tmpkey):
        self.db.updatetmphk(tmpkey)
        return

    def updatelasthk(self, lastkey):
        self.db.updatelastkey(lastkey)
        return

    @staticmethod
    def gethcontext():
        results = self.db.gethcontexts()
        return results

    def gethcontextod(self, inputtext):
        results, timer = self.db.gethcontextod(inputtext)
        return results, timer

    def searchctx(self, txt):
        results = self.db.ctxfilterresults(txt)
        return results

    def searchtext(self, txt, debug, limit=0):
        self.isdebug = debug
        results, timer = self.db.searchresults(txt, self.isdebug, limit)
        return results, timer

    def cleardb(self):
        results = self.db.cleardatabase()
        return results
    # !SECTION