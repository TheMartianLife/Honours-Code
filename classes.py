import os
import json
import math
from datetime import datetime, timedelta
from email.utils import parsedate_tz

class FileComponents:

    def __init__(self, filepath):
        absolute_path = os.path.abspath(filepath) if filepath is not None else None
        path,file = os.path.split(absolute_path) if filepath is not None else None
        name = os.path.splitext(file)[0] if filepath is not None else None
        extension = os.path.splitext(file)[1] if filepath is not None else None

        self.absolute_path = absolute_path
        self.path = path + '/'
        self.name = name
        self.extension = extension

class Tweet:

    #################################
    #          INITIALISER          #
    #################################
    def __init__(self, tweet_object):
        # store original json (for debugging/cleaning/verification)
        self.original_data = tweet_object

        # convert object string representation to JSON dict
        tweet_json = json.loads(tweet_object)

        self.is_retweet = ("retweeted_status" in tweet_json)
        self.is_quote_tweet = ("quoted_status" in tweet_json)
        self.retweeted_id = None
        self.quoted_id = None

        self.id = int(tweet_json["id_str"]) if "id_str" in tweet_json else None
        self.likes = int(tweet_json["favorite_count"]) if "favorite_count" in tweet_json else None
        self.retweets = int(tweet_json["retweet_count"]) if "retweet_count" in tweet_json else None
        self.timestamp = self.process_datetime(tweet_json["created_at"])

        # RETWEET
        if self.is_retweet:
            self.retweeted_id = int(tweet_json["retweeted_status"]["id_str"]) if "id_str" in tweet_json["retweeted_status"] else None
            retweet_likes = int(tweet_json["retweeted_status"]["favorite_count"]) if "favorite_count" in tweet_json["retweeted_status"] else None
            self.likes = max(self.likes, retweet_likes)

        # QUOTE TWEET
        if self.is_quote_tweet:
            self.quoted_id = int(tweet_json["quoted_status_id"]) if "quoted_status_id" in tweet_json else None

    #################################
    #        HELPER FUNCTIONS       #
    #################################
    def process_datetime(self, date_string):
        time_tuple = parsedate_tz(date_string.strip())
        dt = datetime(*time_tuple[:6])
        return str(dt - timedelta(seconds=time_tuple[-1]))

    #################################
    #        CSV LINE VALUES        #
    #################################
    def values(self):
        return [str(self.id), str(self.likes), str(self.retweets), str(self.retweeted_id), str(self.quoted_id), self.timestamp]
