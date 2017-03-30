"""
Opens a Twitter Stream and filters on arguement keyword then stores to mongodb.
Start MongoDB, open mongo console, then type  "use twit_db" command at mongodb console.
    Usage: python twitter_stream.py -q <keyword>
    if no keyword is supplied, the default is all of the stream
    To stop use CTRL C
    caution: file size can grow rapidly if no keyword arguement is supplied

Author: Al Sabay
Credits to: Ruben Cuevas Menendez https://coolprof.wordpress.com/2014/10/19/tweepy-and-pymongo-retrieving-and-storing-tweets-in-mongodb/
            Marco Bonzanini https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/            
"""

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json
from pymongo import MongoClient

#parser for command line
def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    return parser

#subclass StreamListener to store tweets to mongodb
class MyListener(StreamListener):
    def on_data(self, data):
        client = MongoClient('localhost', 27017)

        # Use twit_db database
        db = client.twit_db

        # Decode JSON
        datajson = json.loads(data)
        # insert data to mongodb
        db.tweet.insert(datajson)
        return True
    def on_error(self, status):
        print(status)
        return True


def convert_valid(one_char):

    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    twitter_stream = Stream(auth, MyListener(args.query))

    twitter_stream.filter(track=[args.query])
