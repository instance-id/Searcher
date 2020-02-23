import os
import threading
import hdefereval as hd

from . import database

db = database.Databases()


def worker():
    hd.executeInMainThreadWithResult(DataHandler().updatedata)


class DataHandler(object):
    """Searcher data and communication handler"""

    def __init__(self, debug=None):
        self.isdebug = debug
        self.scriptpath = os.path.dirname(os.path.realpath(__file__))
    # ----------------------------------------------------------------------------------- Function calls
    # ----------------------------------------------------- Retrieve

    def getchangeindex(self):
        index = db.getchangeindex()
        return index

    def getdefaulthotkey(self):
        index = db.getdefhotkey()
        return index

    # ----------------------------------------------------- Updates
    def updatechangeindex(self, indexval, new=False):
        db.updatechangeindex(indexval, new)
        return

    def updatedataasync(self):
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()

    def updatedata(self):
        db.updatecontext(self.isdebug)
        return

    def updatetmphotkey(self, tmpkey):
        db.updatetmphk(tmpkey)
        return

    def updatelasthk(self, lastkey):
        db.updatelastkey(lastkey)
        return

    @staticmethod
    def gethcontext():
        results = db.gethcontexts()
        return results

    def gethcontextod(self, inputtext):
        results = db.gethcontextod(inputtext)
        return results

    def searchctx(self, txt):
        results = db.ctxfilterresults(txt)
        return results

    def searchtext(self, txt):
        results = db.searchresults(txt)
        return results

    def cleardb(self):
        results = db.cleardatabase()
        return results
