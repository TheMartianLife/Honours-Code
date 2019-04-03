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
        self.retweets = int(tweet_json["retweet_count"]) if "retweet_count" in tweet_json else None
        self.timestamp = self.process_datetime(tweet_json["created_at"])

        # RETWEET
        if self.is_retweet:
            self.text = self.get_full_text(tweet_json["retweeted_status"])
            self.likes = int(tweet_json["retweeted_status"]["favorite_count"]) if "favorite_count" in tweet_json["retweeted_status"] else None
            self.retweeted_id = int(tweet_json["retweeted_status"]["id_str"]) if "id_str" in tweet_json["retweeted_status"] else None
            self.is_retweet = True

        # NORMAL TWEET
        else:
            self.text = self.get_full_text(tweet_json)
            self.likes = int(tweet_json["favorite_count"]) if "favorite_count" in tweet_json else None

        # QUOTE TWEET
        if self.is_quote_tweet:
            self.text += "\n\nQUOTED TWEET: " + self.get_full_text(tweet_json["quoted_status"])
            self.quoted_id = int(tweet_json["quoted_status_id"]) if "quoted_status_id" in tweet_json else None

        self.temperature = self.calculate_temperature()
        self.volume = self.calculate_volume()

    #################################
    #        HELPER FUNCTIONS       #
    #################################
    def get_full_text(self, tweet_json):
        if "extended_tweet" in tweet_json and "full_text" in tweet_json["extended_tweet"]:
            return tweet_json["extended_tweet"]["full_text"]
        return tweet_json["full_text"] if "full_text" in tweet_json else None

    def process_datetime(self, date_string):
        time_tuple = parsedate_tz(date_string.strip())
        dt = datetime(*time_tuple[:6])
        return str(dt - timedelta(seconds=time_tuple[-1]))

    #################################
    #      TEMPERATURE METRIC       #
    #################################
    def calculate_temperature(self):
        # TODO: replace metric
        if self.likes is None or self.retweets is None:
            return None
        return self.likes

    #################################
    #         VOLUME METRIC         #
    #################################
    def calculate_volume(self):
        # TODO: replace metric
        if self.retweets is None:
            return 1
        return self.retweets + 1


    #################################
    #     STRING REPRESENTATION     #
    #################################
    def __str__(self):
        header_text = "TWEET (ID: " + str(self.id) + ")\ntimestamp: " + self.timestamp + "\n\n"
        engagement_text = "\n\nlikes: " + str(self.likes) + " retweets: " + str(self.retweets) + "\n"
        metrics_text = " temperature: " + str(self.temperature) + "volume: " + str(self.volume) + "\n"
        return header_text + self.text + engagement_text + metrics_text


    #################################
    #        CSV LINE VALUES        #
    #################################
    def values(self):
        return [str(self.id), self.text.encode('utf-8'), str(self.likes), str(self.retweets), str(self.temperature), str(self.volume), str(self.is_retweet), str(self.retweeted_id), str(self.is_quote_tweet), str(self.quoted_id), self.timestamp]