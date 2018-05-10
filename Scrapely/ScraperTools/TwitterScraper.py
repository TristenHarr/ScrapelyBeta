from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import time
import sqlite3
import random
import re
from datetime import date
from conf import load_in

settings = load_in()

# TODO: *PROJECT MILESTONE* Turn this into a wrapper for any JSON formatted data


class Extraction(object):

    def __init__(self):
        """
        An Object designed to allow for data to be easily extracted from twitter, and placed
        inside a database
        """
        self.data = None
        self.conn = None
        self.database = None
        self.table = None
        self.manage = None
        self.limiting = 0

    def connect(self, username, table_name):
        # TODO: The CONTROL database is currently only slightly operational.
        # The long-term goal is for the CONTROL database to allow multiple users with multiple
        # API keys to manage their accounts online in a data driven web-app and so the security
        # and also the functionality of the CONTROL database need major upgrades.
        """
        Creates the connection to the database, if the database or table does not exist it will
        automatically be created, and it will be added into the CONTROL database which contains
        records of all databases and what information they hold

        :type username: str
        :param username: The name of the database to connect to
        :type table_name: str
        :param table_name: The name of the table to connect to
        :return: None
        """
        self.database = username
        self.table = table_name
        # Connects to a SQLite database with the specified database name
        self.conn = sqlite3.connect(settings['USERS_DB'].format(username))
        # Creates a table with the specified table name if it doesn't already exist
        self.conn.execute("CREATE TABLE IF NOT EXISTS {tn} (days INTEGER,"
                          "favorites INTEGER,"
                          "favpd FLOAT,"
                          "followers INTEGER,"
                          "folpd FLOAT,"
                          "hashtags TEXT,"
                          "in_reply_to TEXT,"
                          "lang TEXT,"
                          "links_mentioned TEXT,"
                          "original_author_handle TEXT,"
                          "original_author_id TEXT,"
                          "place TEXT,"
                          "plain_desc TEXT,"
                          "plain_text TEXT,"
                          "source TEXT,"
                          "statpd FLOAT,"
                          "user_statuses INTEGER,"
                          "tweet TEXT,"
                          "tweet_id TEXT,"
                          "tweet_location TEXT,"
                          "tweet_mentions TEXT,"
                          "tweeted_time TEXT,"
                          "user_twitter_birthday TEXT,"
                          "user_description TEXT,"
                          "user_handle TEXT,"
                          "user_id TEXT,"
                          "user_location TEXT,"
                          "user_name TEXT, PRIMARY KEY (tweet))".format(tn=self.table))
        # The below allows for the Datamanager object to add the database the CONTROL table
        # self.manage = DataManager()
        # self.manage.connect()
        # self.manage.addition(username, table_name)

    def locate(self):
        # TODO: The random location generation should only occur on a city-wide level, and should be optional
        """
        This function is designed to pull geo-location data, and it will generate a random precise
        positioning inside a given geo-box, this will allow for easy use of choropleth mapping.

        :return: A dictionary to be unpacked into the main load-in set for the database
        """

        # If a set of coordinates does exist return them
        if self.data['coordinates'] is not None:
            my_location = self.data['coordinates']['coordinates']
            return {'tweet_location': '`'.join(list(map(lambda x: str(x), my_location)))}
        # If they don't exist, but place does exist, look for a coordinates bounding box
        elif self.data['place'] is not None and self.data['place']['bounding_box']['coordinates']:
            boxes = self.data['place']['bounding_box']['coordinates'][0]
            my_lat = [boxes[0][1], boxes[1][1]]
            my_long = [boxes[0][0], boxes[2][0]]
            my_lat_range = random.randint(int(my_lat[0] * 100000), int(my_lat[1] * 100000)) / 100000
            my_long_range = random.randint(int(my_long[0] * 100000), int(my_long[1] * 100000)) / 100000
            return {'tweet_location': str(my_long_range) + '`' + str(my_lat_range)}
        # If the above fails, just return None
        else:
            return {'tweet_location': 'None'}

    def user_data(self):
        """
        This extracts information on the user who posted the tweet. It sends it to be unpacked and loaded
        into the database

        :return: A dictionary to be unpacked into the main load-in set for the database
        """
        itemuser = self.data['user']
        my_user_dict = {'user_id': itemuser['id'], 'user_name': itemuser['name'],
                        'user_handle': itemuser['screen_name'], 'user_desc': itemuser['description'],
                        'twitter_birthday': itemuser['created_at'], 'user_location': itemuser['location'],
                        'followers': itemuser['followers_count'], 'favorites': itemuser['favourites_count'],
                        'statuses': itemuser['statuses_count']}
        return my_user_dict

    def entities_data(self):
        """
        This function loads in the entities data

        :return: A dictionary to be unpacked into the main load-in set for the database
        """
        entities_item = self.data['entities']
        my_entities_dict = {"hashtags": ""}
        for tag in entities_item['hashtags']:
            # Delimits hashtags with ` this is temporary, eventually there will be foreign keys linkng these values
            my_entities_dict['hashtags'] += tag['text'] + '`'
        my_entities_dict['tweet_mentions'] = ""
        my_entities_dict['links_mention'] = ''
        for person in entities_item['user_mentions']:
            # This is similar to the above
            my_entities_dict['tweet_mentions'] += person['id_str'] + '`'
        for links in entities_item['urls']:
            # Similar to the above
            my_entities_dict['links_mention'] += links['url'] + '`'
        return my_entities_dict

    def extract_relevant(self):
        """
        This function creates additional load-in data to send to the database. This function also does some
        work cleaning the data so that it's easier to work with.

        :return: A dictionary to be unpacked into the main load-in set for the database
        """
        item_extraction = self.data
        my_dict = {'tweeted_time': item_extraction['created_at'],
                   'tweet_id': item_extraction['id'],
                   # If the time comes when the below becomes more significant, it will be no trouble at all to make an
                   # additional column for it, but delimiting it with a ` creates less clutter in the Database
                   'in_reply_to':
                       "NAME/" + str(item_extraction['in_reply_to_screen_name']) + "`" +
                       "STATUSID/" + str(item_extraction['in_reply_to_status_id_str']) + "`" +
                       "USERID/" + str(item_extraction['in_reply_to_user_id_str']),
                   'lang': item_extraction['lang'],
                   'place': item_extraction['place'], 'source': item_extraction['source']}
        if item_extraction['place'] is not None:
            my_dict['place'] = item_extraction['place']['full_name']
        if 'retweeted_status' in item_extraction.keys():
            my_dict['original_author_id'] = item_extraction['retweeted_status']['user']['id']
            my_dict['original_author_handle'] = item_extraction['retweeted_status']['user']['screen_name']
            tester = item_extraction['retweeted_status']['text']
            cleaned = ' '.join(re.sub("(RT : )|(@[\S]+)|(&\S+)|(http\S+)", " ", tester).split())
            removed_others = " ".join(re.sub("(#\S+)", ' ', cleaned).split())
            final_text = ''.join(list(filter(lambda x: x.isalpha() or x is ' ', removed_others)))
            # This final text will make it a lot easier to run NLP
            final_text = final_text.strip().replace('   ', ' ').replace('  ', ' ')
            my_dict['plain_text'] = final_text.lower()
            my_dict['tweet'] = cleaned
        else:
            my_dict['original_author_id'] = item_extraction['user']['id']
            my_dict['original_author_handle'] = item_extraction['user']['screen_name']
            cleaned = ' '.join(re.sub("(@[\S]+)|(&\S+)|(http\S+)", " ", item_extraction['text']).split())
            removed_others = " ".join(re.sub("(#\S+)", ' ', cleaned).split())
            final_text = ''.join(list(filter(lambda x: x.isalpha() or x is ' ', removed_others)))
            final_text = final_text.strip().replace('   ', ' ').replace('  ', ' ')
            my_dict['plain_text'] = final_text.lower()
            my_dict['tweet'] = cleaned
        return my_dict

    def calculate_days(self):
        """
        This function calculates the number of days that the person has had a twitter, as well as some
        other useful information including the average number of statuses per day, followers gained per day,
        and the average number of status's per day.

        :return: A dictionary to be unpacked into the main load-in set for the database
        """
        tweet_time = self.data['created_at']
        birthday = self.data['user']['created_at']
        my_dates = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
                    "Nov": 11, "Dec": 12}
        # This could have easily been cast into one of the numerous datetime function's immediately, however
        # it was causing a major slowdown to the program and so the below was a quick fix.
        ######################################################################
        # NOTICE: IF SOMETHING BREAKS THIS IS MOST LIKELY TO BE WHAT IT IS   #
        ######################################################################
        tweet_time2 = [my_dates[tweet_time[4:7]], int(tweet_time[8:10]), int(tweet_time[26:])]
        birthday2 = [my_dates[birthday[4:7]], int(birthday[8:10]), int(birthday[26:])]
        first = date(tweet_time2[2], tweet_time2[0], tweet_time2[1])
        second = date(birthday2[2], birthday2[0], birthday2[1])
        final = first - second
        days = final.days
        follows = self.data['user']['followers_count']
        favorites = self.data['user']['favourites_count']
        statuses = self.data['user']['statuses_count']
        favpd = favorites/days
        folpd = follows/days
        statpd = statuses/days
        return {"days": final.days, "folpd": folpd, "favpd": favpd, "statpd": statpd}

    def clean_user_desc(self):
        """
        This function cleans the user description, removing all but alphabetical characters, and casting
        everything to lowercase.

        :return: A dictionary to be unpacked into the main load-in set for the database
        """
        desc = self.data['user']['description']
        if desc is not None:
            desc = ' '.join(re.sub("(RT : )|(@[\S]+)|(&\S+)|(http\S+)", " ", desc).split())
            desc = " ".join(re.sub("(#\S+)", ' ', desc).split())
            desc = ''.join(list(filter(lambda x: x.isalpha() or x is ' ',
                                       desc))).replace('   ', ' ').replace('  ', ' ').lower().strip()
        return {'plain_desc': desc}

    def store_data(self, data):
        """
        The following function stores the data into the specified database. This function is the heart of the program
        the_main_dict is an example of the power of dictionary unpacking, it also makes it very easy to modify the
        scraper. If new information is wanted to be gleaned, a new function can be created above, since the entire
        scraper is an object, all of the data is held in place currently, this is where all data comes to be cleaned.

        PROCEDURE TO ADD A NEW COLUMN TO THE DATABASE WITH CUSTOM PARAMETERS: (Change Line Numbers to match as needed)

        1. Go to line 47 and determine what the column name should be, and insert it into the position it would fall
        into alphabetically.

        2. Directly above this function, define a new function that takes no parameters, and then manipulate the data
        as needed within the function until the desired result is reached. Set the function to then return the result
        in the form of a dictionary, in which the keys match the name set in step 1. and the values are the result

        3. In the section of this function below, marked HERE, insert however many additional {} are needed to format
        into the insert SQL query

        :type data: dict
        :param data: The data passed in directly from the Scraper
        :return: An integer to inform the scraper of Success or not, used to manage the limit if neccesarry.
        """
        self.data = data
        # HERE
        the_main_dict = {**self.user_data(), **self.entities_data(), **self.extract_relevant(), **self.locate(),
                         **self.calculate_days(), **self.clean_user_desc()}
        # The below is the reason that the table creation must be written in alphabetical order. This is simpler than
        # writing the complex joins that would otherwise be needed.
        my_keys_list = sorted(the_main_dict.keys())
        my_items = list(map(lambda x: str(the_main_dict[x]).replace("'", ''), my_keys_list))
        try:
            # Unpacks the items into an insert statement for the SQLite table
            self.conn.execute("INSERT INTO {0} VALUES('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}',"
                              "'{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}',"
                              "'{21}','{22}','{23}','{24}','{25}','{26}','{27}','{28}')".format(self.table, *my_items))
            self.limiting += 1
            return 0
        except sqlite3.IntegrityError:
            return 1

    def finish(self):
        """
        Commits the changes to the database, and closes the connection.

        :return: None
        """
        self.conn.commit()
        self.conn.close()


# class DataManager(object):
#
#     def __init__(self):
#         """
#         This object is designed to allow for administration to be put in place, and also to allow for the datasets to
#         be better organized upon collection. The goal is to make it possible to run multiple scrapers at once and
#         collect information on multiple topics at once, which can later be used as data-sets
#         """
#         self.conn = None
#
#     def connect(self):
#         """
#         Creates a connection to the manager table
#         :return: None
#         """
#         self.conn = sqlite3.connect("DATABASE/CONTROL.sqlite")
#         self.conn.execute("CREATE TABLE IF NOT EXISTS {tn} (id TEXT, database TEXT,"
#                           "query TEXT, query_text TEXT,"
#                           " volume INTEGER, PRIMARY KEY (id, database))".format(tn='manager'))
#
#     def addition(self, database, table):
#         # TODO: This needs some work, a quick view of the SQL table will show that. Most parameters are filled in as
#         # None and need to be fixed
#         """
#         Attempts to add the database and table into the list of currently existing databases and tables
#         :param database:
#         :param table:
#         :return:
#         """
#         try:
#             self.conn.execute("INSERT INTO manager VALUES('{id}','{database}','{query}', '{query_text}'"
#                               ",'{volume}')".format(id=table, database=database, query="None", query_text="None",
#                                                     volume="None"))
#             self.conn.commit()
#             self.conn.close()
#             return True
#         except sqlite3.IntegrityError:
#             return False


class MyListener(StreamListener):

    def __init__(self, limits=60, limit_types="TIME"):
        """
        Extends StreamListener in the tweepy module

        :type limits: int
        :param limits: The limit of the amount of data to stream
        :type limit_types: str
        :param limit_types: Specify 'TIME' for seconds or 'COUNT' for tweet number
        """
        self.start_time = time.time()
        self.limit_type = limit_types
        self.limit = limits
        self.temp = set()
        self.database = None
        super(MyListener, self).__init__()

    def config(self, database, table_name):
        self.database = Extraction()
        self.database.connect(database, table_name)

    def on_data(self, data):
        """
        Extends the StreamListener class and routes the incoming data into the Extraction Object method store_data
        :param data: Data streamed from twitter API through tweepy
        :return: True to continue stream, False to end stream
        """
        # Try-Except used by tweepy
        try:
            # If the limit type is time, and the time passed is less than the limit, continue
            if self.limit_type == "TIME" and (time.time() - self.start_time < self.limit):
                item = json.loads(data)
                if 'created_at' in item.keys():
                    self.temp |= set(item.keys())
                    self.database.store_data(item)
                else:
                    pass
                # The below is a check to prevent entering another loop by forcing the stream to be cutoff
                if (time.time() - self.start_time) < self.limit:
                    return True
                else:
                    self.database.finish()
                    return False
            # If the limit type is count, and the number of tweets streamed in hasn't reached the limit, continue
            elif self.limit_type == "COUNT" and self.limit != 0:
                # See limit type = 'TIME' for confusion about below
                item = json.loads(data)
                if 'created_at' in item.keys():
                    good = self.database.store_data(item)
                    self.limit += good
                    self.limit -= 1
                else:
                    pass
                if self.limit > 0:
                    return True
                else:
                    self.database.finish()
                    # Call counter
                    return False
            else:
                return False
        except BaseException as e:
            print(e)
            return True

    def on_status(self, status):
        print(status.txt)

    def on_limit(self, limit_info):
        print(limit_info)
        return

    def on_connect(self):
        print('ok')

    def on_error(self, status_code):
        print(status_code)

    def on_exception(self, exception):
        print(exception)


def locate(code):
    # TODO: Add more specific search parameters, link this to a GUI that shows the map and lets you custom pick the
    # geo-coordinate box.
    """
    Used to get the geo-box coordinates of a country by it's code EX: 'US'

    :type code: str
    :param code: A :str: with a country code
    :return: A :list: of :float: with geo-box coordinates
    """
    my_dict = {}
    # Gets the specified country codes geo-box coordinates from a CVS file

    with open("CSV-Files/country-boundingboxes.csv", 'r') as tester:
        for line in tester:
            item = line.rstrip('\n').split(',')
            my_dict[item[0]] = list(map(lambda x: float(x), item[2:]))
    tester.close()
    return my_dict[code]


class Scraper(object):

    def __init__(self, search_type):
        """
        This is the Scraper object.
        :param search_type:
        """
        self.search = search_type
        self.items = None
        self.lang = None
        self.limit = None
        self.limit_type = None
        self.database = None
        self.table = None
        self.access_token = None
        self.access_token_secret = None
        self.consumer_key = None
        self.consumer_secret = None

    def set_limit(self, limit_type, limit):
        self.limit_type = limit_type
        self.limit = limit

    def database_config(self, username, table):
        self.table = table
        self.database = username

    def search_configure(self, search=list()):
        self.items = search

    def set_languages(self, languages):
        self.lang = languages

    def set_keys(self, keys):
        self.access_token = keys['access_token']
        self.access_token_secret = keys['access_token_secret']
        self.consumer_key = keys['consumer_key']
        self.consumer_secret = keys['consumer_secret']

    def scrape(self):
        scraper = MyListener(self.limit, self.limit_type)
        scraper.config(self.database, self.table)
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        stream = Stream(auth, scraper)
        if self.search == 'track' and self.lang is None:
            stream.filter(track=self.items)
        elif self.search == 'track':
            stream.filter(track=self.items, languages=self.lang)
        elif self.search == 'location' and self.lang is None:
            stream.filter(locations=self.items)
        elif self.search == 'location':
            stream.filter(locations=self.items, languages=self.lang)
