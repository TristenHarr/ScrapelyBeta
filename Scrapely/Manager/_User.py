import sqlite3

from Manager._FileController import FileController
from Manager._passwords import check_password
from conf import load_in
from cryptography.fernet import Fernet, MultiFernet
settings = load_in()


class User:

    def __init__(self, username):
        self.con = sqlite3.connect(settings['MAIN_DB'])
        self.c = self.con.cursor()
        self.user_items = None
        self.user_dict = None
        self.keys = None
        if self.user_exists(username):
            self.username = username
            self.password = self.c.execute("SELECT password FROM"
                                           " users WHERE username='{}'".format(username)).fetchone()[0]

    def load_user(self):
        self.user_items = self.c.execute("""SELECT id, email, email_verified, username, is_authenticated, data_tables,
                                            logged_in, subscribed, charts, models, groups, first_name, last_name,
                                            friends, active, reset_request, data_sources, projects
                                            FROM users WHERE username='{}'""".format(self.username)).fetchall()[0]
        self.user_dict = {'id': self.user_items[0], 'email': self.user_items[1], 'email_verified': self.user_items[2],
                          'username': self.user_items[3], 'is_authenticated': self.user_items[4],
                          'data_tables': self.fetch_table_list(), 'logged_in': self.user_items[6],
                          'subscribed': self.user_items[7], 'charts': self.user_items[8], 'models': self.fetch_models(),
                          'groups': self.user_items[10], 'first_name': self.user_items[11],
                          'last_name': self.user_items[12], 'friends': self.user_items[13],
                          'active': self.user_items[14], 'reset_request': self.user_items[15],
                          'data_sources': self.fetch_data_list(), 'projects': self.user_items[17],
                          'table_count_keywords': list(zip(self.fetch_table_list(),
                                                           self.fetch_table_counts(),
                                                           self.fetch_keywords_list()))}
        return self.user_dict

    def user_exists(self, username):
        valid = self.c.execute("SELECT EXISTS(SELECT username "
                               "FROM users WHERE username = '{}')".format(username)).fetchone()[0]
        return valid

    def login_user(self, password):
        return check_password(password, self.password)

    def get_id(self):
        return self.user_dict['username']

    def is_authenticated(self):
        return self.user_dict['is_authenticated']

    def is_active(self):
        return self.user_dict['is_active']

    def create_data_source(self, datasource):
        FileController().make_item(self.username, datasource, 'data_source')

    def delete_source(self, datasource):
        FileController().delete_item(self.username, datasource, 'data_source')

    def create_model(self, model):
        FileController().make_item(self.username, model, 'model')

    def delete_model(self, model):
        FileController().delete_item(self.username, model, 'model')

    def fetch_models(self):
        return FileController().make_item(self.username, item=None, path_name='model', fetch=True)

    def fetch_data_list(self):
        return FileController().make_item(self.username, item=None, path_name='data_source', fetch=True)

    def fetch_table_counts(self):
        con = sqlite3.connect(settings['USERS_DB'].format(self.username))
        tables = self.fetch_table_list()
        my_list = []
        for table in tables:
            my_list.append(con.execute("SELECT Count(*) FROM '{}'".format(table)).fetchone()[0])
        return my_list

    def make_data(self, table_name):
        FileController().make_item(self.username, table_name, 'data_table')

    def fetch_table_list(self):
        return FileController().make_item(self.username, item=None, path_name='data_table', fetch=True)

    def fetch_keywords_list(self):
        con = sqlite3.connect(settings['MAIN_DB'])
        tables = self.fetch_table_list()
        my_list = []
        for table in tables:
            my_list.append(con.execute("SELECT keywords FROM KeywordTable"
                                       " WHERE username='{}' "
                                       "AND table_name='{}'".format(self.username, table)).fetchone()[0])
        return my_list

    def delete_data(self, table_name):
        FileController().delete_item(self.username, table_name, 'data_table')

    def load_in_keys(self):
        try:
            keys = self.c.execute("SELECT * FROM secrets WHERE username = '{}'".format(self.username)).fetchall()[0]
            ul = self.c.execute("SELECT * FROM secret_keys WHERE username = '{}'".format(self.username)).fetchall()[0]
            key1 = Fernet(ul[1])
            key2 = Fernet(ul[2])
            x = MultiFernet([key1, key2])
            access_token = x.decrypt(keys[1]).decode()
            access_token_secret = x.decrypt(keys[2]).decode()
            consumer_key = x.decrypt(keys[3]).decode()
            consumer_secret = x.decrypt(keys[4]).decode()
            token_dict = {"access_token": access_token, "access_token_secret": access_token_secret,
                          "consumer_key": consumer_key, "consumer_secret": consumer_secret}
            return token_dict

            # return token_dict
        except AttributeError:
            return None
