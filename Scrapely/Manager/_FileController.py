import os
from conf import load_in

settings = load_in()
settings['unique'] = settings["USERS_DB"][0:settings['USERS_DB'].rfind('/')]


class FileController:
    def __init__(self):
        """
        A FileController object that manages text-files used
        to populate the user's Control Panel and interface as well
        as provide the ability to add and remove items from a user's
        folder
        """
        self.primary_folder = settings['unique']
        data_source_path = self.primary_folder + "/_data_sources.txt"
        data_tables_path = self.primary_folder + "/_data_tables.txt"
        models_path = self.primary_folder + "/_models.txt"
        charts_path = self.primary_folder + "/_charts.txt"
        projects_path = self.primary_folder + "/_projects.txt"
        self.control_dict = {"data_source": data_source_path, "data_table": data_tables_path, "model": models_path,
                             "chart": charts_path, "project": projects_path}

    def file_handler(self, username):
        """
        Initiates creation of a user's directory, called on registration

        :type username: str
        :param username: The unique username provided upon registration
        :return: None
        """
        os.mkdir(self.primary_folder.format(username))
        first = open(self.control_dict['data_source'].format(username), 'a')
        first.close()
        first = open(self.control_dict['data_table'].format(username), 'a')
        first.close()
        first = open(self.control_dict['model'].format(username), 'a')
        first.close()
        first = open(self.control_dict['chart'].format(username), 'a')
        first.close()
        first = open(self.control_dict['project'].format(username), 'a')
        first.close()

    def make_item(self, username, item, path_name, fetch=False):
        """
        This function doubles as a way to add items to a user's folders
        and also as a way to retrieve a list of items from a users folder

        :type username: str
        :param username: The unique username provided upon registration
        :type item: str
        :type item: none        
        :param item: The item to be added to the users file
        :type path_name: str
        :param path_name: The key for the full path found in the control_dict
        :type fetch: bool
        :param fetch: When true, provides a list of items in the specified file
        :return: A list of items ***IF fetch == True***
        """
        control_dict = self.control_dict
        data = open(control_dict[path_name].format(username), 'r')
        my_items = []
        for line in data:
            my_items.append(line.strip())
        data.close()
        if fetch:
            return my_items
        if item not in my_items:
            data = open(control_dict[path_name].format(username), 'a')
            data.write(item + '\n')
            data.close()

    def delete_item(self, username, item, path_name):
        """
        Removes a specified item from a file

        :type username: str
        :param username: The unique username provided upon registration
        :type item: str
        :param item: The item to be deleted
        :type path_name: str
        :param path_name: The key for the full path name in control_dict
        :return: None
        """
        control_dict = self.control_dict
        data = open(control_dict[path_name].format(username), 'r')
        my_items = []
        for line in data:
            my_items.append(line.strip())
        data.close()
        if item in my_items:
            my_items.remove(item)
            data = open(control_dict[path_name].format(username), 'w')
            for line in my_items:
                data.write(line + '\n')
            data.close()

    def fetch_path(self, username):
        return self.primary_folder.format(username)
