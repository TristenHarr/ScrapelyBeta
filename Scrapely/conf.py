import os
from setup import config, directory


class Config:
    def __init__(self):
        self.home_path = directory()
        self.user_defaults = None
        self.main_db = None
        self.users_db = None
        self.tests = None
        self.forms = None

    def setup_main_db(self, main_db_folder="DATABASE", main_db="data", main_db_extension='.db'):
        db = main_db + main_db_extension
        self.main_db = os.path.join(self.home_path, main_db_folder, db)
        file = open(directory()+"/CONFIG.txt", 'r')
        my_setup = {}
        for line in file:
            splitted = line.strip().split('`')
            my_setup[splitted[0]] = splitted[1]
        file.close()
        if "MAIN_DB" in my_setup.keys():
            raise IsADirectoryError("Configuration has already been set, to change use function edit_conf(current_conf_name, new)")
        else:
            file = open(directory()+"/CONFIG.txt", 'a')
            file.write("MAIN_DB`{}\n".format(self.main_db))
            file.close()

    def set_users_db(self, users_folder="USERS", users_db='data1', users_db_extenstion='.db'):
        file = open(directory()+"/CONFIG.txt", 'r')
        my_setup = {}
        for line in file:
            splitted = line.strip().split('`')
            my_setup[splitted[0]] = splitted[1]
        file.close()
        if "USERS_DB" in my_setup.keys():
            raise IsADirectoryError(
                "Configuration has already been set, to change use function edit_conf(current_conf_name, new)")
        else:
            userdb = directory()+"/{}".format(users_folder)+"/{}/"+users_db+users_db_extenstion
            file = open(directory()+"/CONFIG.txt", 'a')
            file.write("USERS_DB`{}\n".format(userdb))
            file.close()



def load_in():
    file = open(config(), 'r')
    my_setup = {}
    for line in file:
        splitted = line.strip().split('`')
        my_setup[splitted[0]] = splitted[1]
    file.close()
    return my_setup


