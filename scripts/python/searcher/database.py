import os

from peewee import SqliteDatabase

scriptpath = os.path.dirname(os.path.realpath(__file__))
db = SqliteDatabase(scriptpath + '/db/searcher.db')
cur = db.cursor()


# class Hotkeys(Model):
#     hotkey_symbol = CharField()
#     context = CharField()
#     label = CharField()
#     description = CharField()
#     assignments = CharField()
# 
#     class Meta:
#         database = db # This model uses the "people.db" database.
#         
# class HCONTEXT(Model):
#     HCONTEXT = CharField()
#     context = CharField()
#     description = CharField()
#     title = CharField()
# 
#     class Meta:
#         database = db # This model uses the "people.db" database.

# db.connect()


class Databases(object):
    def __init__(self):
        self.a = 1

    def searchresults(self, inputTerm):# gdy """ """ przygotowanie zapytania
        cur.execute("SELECT  label, description, assignments, context FROM hotkeys WHERE label LIKE '%" + inputTerm + "%'")
        result = cur.fetchall()
        return result

# db = TinyDB(scriptpath + '/db/db.json',  default_table='data',  sort_keys=True, indent=4, separators=(',', ': '))


# def performindex(self):
#     # with fastss.open('fastss.dat') as index:
#     #     for word in open(scriptpath + '/db/db.json'):
#     #         index.add(word.strip())
#     return

# def searchresults(self, tet):
#     results = db.search(where("label")).any(tet)
#     # results = db.search(where("label").any(lambda x: re.match(".+%s.+" % self.outfile, x)))
#     print results
#     # with fastss.open('fastss.dat') as index:
#     #     # return a dict like: {0: ['test'], 1: ['text', 'west'], 2: ['taft']}
#     #     print(index.query(text))
#     return


#     def savetodatabase(self, data):
#         keytableq = Query()
#         keyfiles = data.keys()
#         # -------------------------------------------------------------------- Update or add keys to proper context list
#         for key in keyfiles:
#             for i in range(len(data[key])):
#                 if data[key][i][0] == "HCONTEXT":
#                     try:
#                         self.keytable.upsert({ str(data[key][i][1]) :
#                                               [{'HCONTEXT': data[key][i][1],
#                                                'context': data[key][i][1],
#                                                'title': data[key][i][2],
#                                                'description': data[key][i][3]
#                                                }]
#                         }, where('context') == data[key][i][1])
#                     except Exception as e:
#                         traceback.print_exc()
#                 else:
#                     try:
#                         self.keytable.upsert({  str(data[key][i][0]) : 
#                                           [{'hotkey_symbol': data[key][i][0],
#                                           'label': data[key][i][1],
#                                           'description': data[key][i][2],
#                                           'assignments': data[key][i][3]
#                                             }]
#                         }, where('hotkey_symbol') == data[key][i][0])
#                     except Exception as e:
#                         traceback.print_exc()


        