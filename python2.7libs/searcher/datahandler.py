from __future__ import print_function
from __future__ import absolute_import

import hou
import os

from searcher import util
from searcher import settings_data
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

    # ----------------------------------------------------------- Retrieve
    # SECTION Retrieve ---------------------------------------------------
    # -------------------------------------- getchangeindex
    # NOTE getchangeindex ---------------------------------
    def getchangeindex(self):
        index = self.db.getchangeindex()
        return index

    # ------------------------------------ getdefaulthotkey
    # NOTE getdefaulthotkey -------------------------------
    def getdefaulthotkey(self):
        index = self.db.getdefhotkey()
        return index

    # ----------------------------------------- gethcontext
    # NOTE gethcontext ------------------------------------
    @staticmethod
    def gethcontext():
        results = self.db.gethcontexts()
        return results

    # --------------------------------------- gethcontextod
    # NOTE gethcontextod ----------------------------------
    def gethcontextod(self, inputtext):
        results, timer = self.db.gethcontextod(inputtext)
        return results, timer

    # ------------------------------------------- searchctx
    # NOTE searchctx --------------------------------------
    def searchctx(self, txt):
        results = self.db.ctxfilterresults(txt)
        return results

    # ------------------------------------------ searchtext
    # NOTE searchtext -------------------------------------
    def searchtext(self, txt, debug, limit=0):
        self.isdebug = debug
        results, timer = self.db.searchresults(txt, self.isdebug, limit)
        return results, timer

    # !SECTION Retrieve

    # ------------------------------------------------------------- Update
    # SECTION Update -----------------------------------------------------
    # ----------------------------------- updatechangeindex
    # NOTE updatechangeindex ------------------------------
    def updatechangeindex(self, indexval, new=False):
        self.db.updatechangeindex(indexval, new)
        return

    # ------------------------------------- updatedataasync
    # NOTE updatedataasync --------------------------------
    def updatedataasync(self, debug):
        self.isdebug = debug
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()

    # ------------------------------------------ updatedata
    # NOTE updatedata -------------------------------------
    def updatedata(self):
        self.db.updatecontext(self.isdebug)
        return

    # ------------------------------------- updatetmphotkey
    # NOTE updatetmphotkey --------------------------------
    def updatetmphotkey(self, tmpkey):
        self.db.updatetmphk(tmpkey)
        return

    # ---------------------------------------- updatelasthk
    # NOTE updatelasthk -----------------------------------
    def updatelasthk(self, lastkey):
        self.db.updatelastkey(lastkey)
        return
    
    # !SECTION Update

    # --------------------------------------------- cleardb
    # NOTE cleardb ----------------------------------------
    def cleardb(self):
        results = self.db.cleardatabase()
        return results