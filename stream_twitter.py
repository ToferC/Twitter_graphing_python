# Code modified from:
# http://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/

import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import csv

import os
import argparse


RESULTS_DIR = "streaming_results"

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
CONSUMER_KEY = os.environ['APP_KEY']
CONSUMER_SECRET = os.environ['APP_SECRET']

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
ACCESS_TOKEN = os.environ['OAUTH_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['OAUTH_TOKEN_SECRET']

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


class MyListener(StreamListener):

    def on_data(self, data):

        try:
            with open(os.path.join(RESULTS_DIR, '{}_stream.json'.format(query)), 'a') as f:
                f.write(data)

                result = json.loads(data)

                print(result['text'].encode('ascii', 'ignore'), result['user']['screen_name'])
                print("*****\n")
                return True

        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-q", "--query", required=True, help="Text to query for twitter stream")
    args = vars(ap.parse_args())

    query = args['query']

    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(track=[query])
