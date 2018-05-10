import pandas as pd
import sqlite3
from conf import load_in

settings = load_in()

def fetch_pk(username, table):
    con = sqlite3.connect(settings['USERS_DB'].format(username))
    return list(filter(lambda x: x[5]==1, con.execute("PRAGMA table_info({})".format(table)).fetchall()))[0][1]
