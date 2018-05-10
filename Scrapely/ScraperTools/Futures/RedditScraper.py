import praw
import requests
import json





class RedditBot():

    def __init__(self, username, password, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(username=username,
                             password=password,
                             client_id=client_id,
                             client_secret=client_secret,
                             user_agent=user_agent)
        self.subreddits = None

    def fetch_query(self, query, sort='relevance'):
        fetched = self.reddit.subreddit('all').search(query=query, sort=sort)
        my_list = []
        for item in fetched:
            my_list.append("https://www.reddit.com"+item.permalink)
            print(my_list[0])
        for item in my_list:
            x = requests.get(item, headers={'User-agent':'Classification Bot'})
            print(x.json())




# test = RedditBot(username, password, client_id, client_secret, user_agent)
# test.fetch_query('trump')
test = requests.get("https://www.reddit.com/r/politics/comments/4smg52/quinnipiac_poll_july_13_pa_trump_43_clinton_41_oh/?ref=search_posts", headers={"User-agent":"Classification Bot"})
