import os
dir_path = os.path.dirname(os.path.realpath(__file__))

import sqlite3

from passlib.hash import pbkdf2_sha256

def make_password(password):
    # TODO: Rewrite this, increase security, look into some kind of database-row rotations
    hashed = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
    return hashed


def check_password(password, hashed):
    return pbkdf2_sha256.verify(password, hashed)

def config():
    ABSOLUTE_PATH = dir_path+'/CONFIG.txt'
    return ABSOLUTE_PATH

def directory():
    ABSOLUTE_PATH = dir_path
    return ABSOLUTE_PATH

def go(Admin, Password):
    file = open('CONFIG.txt', 'a')
    file.close()
    from conf import Config
    manager = Config()
    manager.setup_main_db()
    manager.set_users_db()
    from conf import load_in
    settings = load_in()
    conn = sqlite3.connect(settings['MAIN_DB'])
    conn.execute("CREATE TABLE IF NOT EXISTS {tn} (id INTEGER,"
                 "email TEXT,"
                 "email_verified INTEGER,"
                 "username TEXT,"
                 "password TEXT,"
                 "data_tables TEXT,"
                 "logged_in INTEGER, "
                 "subscribed INTEGER,"
                 "charts TEXT,"
                 "models TEXT,"
                 "groups TEXT,"
                 "first_name TEXT,"
                 "last_name TEXT,"
                 "friends TEXT,"
                 "active INTEGER,"
                 "reset_request INTEGER,"
                 "data_sources TEXT,"
                 "projects TEXT,"
                 "is_authenticated INTEGER,"
                 "PRIMARY KEY (username))".format(tn='users'))
    conn.commit()
    conn.execute("""INSERT INTO users VALUES ('{id}',
                          '{email}',
                          '{email_verified}',
                          '{username}',
                          '{password}',
                          '{data_tables}',
                           {logged_in},
                           {subscribed},
                           '{charts}',
                           '{models}',
                           '{groups}',
                           '{first_name}',
                           '{last_name}',
                           '{friends}',
                           {active},
                           {reset_request},
                           '{data_sources}',
                           '{projects}',
                           {is_authenticated})""".format(
        id=1,
        email='admin@admin.com',
        email_verified=1,
        username=Admin,
        password=make_password(Password),
        data_tables='',
        logged_in=1,
        subscribed=0,
        charts="",
        models="",
        groups="",
        first_name="",
        last_name="",
        friends="",
        active=1,
        reset_request=0,
        data_sources="",
        projects="",
        is_authenticated=0))
    conn.commit()
    conn.close()
    from Manager._FileController import FileController
    FileController().file_handler(Admin)


if __name__ == '__main__':
    admin = input("Admin Username: ")
    password = input("Admin Password: ")
    go(admin, password)