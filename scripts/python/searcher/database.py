import os

from peewee import SqliteDatabase

scriptpath = os.path.dirname(os.path.realpath(__file__))
db = SqliteDatabase(scriptpath + '/db/searcher.db')
cur = db.cursor()


class Databases(object):
    def __init__(self):
        self.a = 1

    def searchresults(self, inputTerm):
        cur.execute("SELECT label, description, assignments, context FROM hotkeys WHERE label LIKE '%" + inputTerm + "%'")
        result = cur.fetchall()
        return result
