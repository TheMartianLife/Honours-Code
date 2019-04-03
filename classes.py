import json
import math

class Tweet:

    #################################
    #          INITIALISER          #
    #################################
    def __init__(self, tweet_object):
        # store original json (for debugging/cleaning/verification)
        self.original_data = tweet_object

        # convert object string representation to JSON dict
        tweet_json = json.loads(tweet_object)

        self.id = int(tweet_json["id_str"]) if "id_str" in tweet_json else None
        self.retweets = int(tweet_json["retweet_count"]) if "retweet_count" in tweet_json else None
        self.timestamp = tweet_json["created_at"]

        # RETWEET
        if "retweeted_status" in tweet_json:
            self.text = self.get_full_text(tweet_json["retweeted_status"])
            self.likes = int(tweet_json["retweeted_status"]["favorite_count"]) if "favorite_count" in tweet_json["retweeted_status"] else None

        # NORMAL TWEET
        else:
            self.text = self.get_full_text(tweet_json)
            self.likes = int(tweet_json["favorite_count"]) if "favorite_count" in tweet_json else None

        # QUOTE TWEET
        if "quoted_status" in tweet_json:
            self.text += "\n\nQUOTED TWEET: " + self.get_full_text(tweet_json["quoted_status"])
            self.quote_tweet = True

        self.temperature = self.calculate_temperature()
        self.volume = self.calculate_volume()

    #################################
    #        HELPER FUNCTION        #
    #################################
    def get_full_text(self, tweet_json):
        if "extended_tweet" in tweet_json and "full_text" in tweet_json["extended_tweet"]:
            return tweet_json["extended_tweet"]["full_text"]
        return tweet_json["full_text"] if "full_text" in tweet_json else None

    #################################
    #      TEMPERATURE METRIC       #
    #################################
    def calculate_temperature(self):
        # TODO: replace metric
        if self.likes is None or self.retweets is None:
            return None
        return float(self.likes) / float(self.retweets)

	#################################
    #         VOLUME METRIC         #
    #################################
    def calculate_volume(self):
        # TODO: replace metric
        if self.retweets is None:
            return None
        return self.retweets


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
        return [str(self.id), self.text, str(self.likes), str(self.retweets), str(self.temperature), str(self.volume), self.timestamp]