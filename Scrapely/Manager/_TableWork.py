import pandas as pd
import sqlite3
from Scrapely.conf import load_in

settings = load_in()


class SuperTable(object):
    def __init__(self, table, username, roworder=None, columnorder=None):
        self.table = table
        self.con = sqlite3.connect(settings['USERS_DB'].format(username))
        self.primary_key = list(filter(lambda x: x[5]==1, self.con.execute("PRAGMA table_info({})".format(table)).fetchall()))[0][1]
        pd.set_option('display.max_colwidth', -1)
        self.frame = pd.read_sql_query("SELECT * FROM '{}'".format(table), self.con).sort_values(by=self.primary_key)
        self.Pkeys = pd.read_sql_query("SELECT {} FROM '{}'".format(self.primary_key, table), self.con)
        self.indices = list(self.frame.keys())
        if columnorder:
            self.columnorder = columnorder
        else:
            self.columnorder = [i for i in range(self.frame.shape[1])]
        if roworder:
            self.roworder = roworder
        else:
            self.roworder = [i for i in range(self.frame.shape[0])]


    def send_off(self):
        return [self.frame.shape, self.doit(), self.roworder, self.columnorder]

    def doit(self):
        the_list = list(map(lambda x: list(x), self.frame.as_matrix()))
        the_array = []
        the_labels = []
        for item in self.columnorder:
            the_labels.append(self.indices[item])
        for item in self.roworder:
            the_row = []
            for item2 in self.columnorder:
                the_row.append(the_list[item][item2])
            the_array.append(the_row)
        the_array.insert(0, the_labels)
        return the_array

test = SuperTable('WorkInP', 'Tristen')
x = test.doit()
print(test.send_off())