import tweepy
import time
import os
import sys
import json
import argparse

FOLLOWING_DIR = 'following'
MAX_FRIENDS = 1000
FRIENDS_OF_FRIENDS_LIMIT = 1000
RESULTS_DIR = "results"

if not os.path.exists(FOLLOWING_DIR):
    os.makedir(FOLLOWING_DIR)

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

api = tweepy.API(auth)

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse

# User is the data model for a user profile
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse

# Process a single status
def search_twitter_to_json(query, count=100, maxtweets=1000):

    d = {}
    tweetcount = 0
    max_id = -1
    sinceId = None
    fname = "search_" + query + ".json"
    query = "#" + query

    with open(os.path.join(RESULTS_DIR, fname), 'w') as f:

        while tweetcount < maxtweets:
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = api.search(q=query, count=count)
                    else:
                        new_tweets = api.search(q=query, count=count,
                            since_id=sinceId)
                else:
                    if not(sinceId):
                        new_tweets = api.search(q=query, count=count,
                            max_id=str(max_id - 1))
                    else:
                        new_tweets = api.search(q=query, count=count,
                            max_id=str(max_id - 1), since_id=sinceId)

                if not new_tweets:
                    print("No more tweets found.")
                    break


                for result in new_tweets:

                    for result in new_tweets:
                        print (result.text)
                        print (result.created_at)
                        print (result.retweet_count)
                        print("")

                        id_str = result.id_str

                        d[id_str] = {
                        'id_str': result.id_str,
                        'date': str(result.created_at),
                        'text': result.text,
                        'retweet_count': result.retweet_count,
                        'favorite_count': result.favorite_count,
                        'reply_to': result.in_reply_to_screen_name,
                        'coordinates': result.coordinates,
                        'reply_to_tweet': result.in_reply_to_status_id,
                        'user_screen_name': result.user.screen_name,
                        'quoted_status': result.is_quote_status,
                        'lang': result.lang,
                        'entities': result.entities,
                        'urls': result.entities['urls'],
                        'hashtags': result.entities['hashtags'],
                        'user_mentions': result.entities['user_mentions'],
                        'user': result.user._json,
                        }

                        try:
                            d[id_str]['quoted_status_id_str'] = result.quoted_status_id_str
                        except AttributeError:
                            d[id_str]['quoted_status_id_str'] = None

                tweetcount += len(new_tweets)
                print("Downloaded {} tweets".format(tweetcount))
                max_id = new_tweets[-1].id

            except tweepy.TweepError as e:
                print("some error :" +str(e))
                break

        f.write(json.dumps(d, indent=1))

    print("Downloaded {} tweets, saved to {}".format(tweetcount, fname))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-q", "--query", required=True, help="Text to query")
    ap.add_argument("-c", "--count", required=True, type=int, help="Number of tweets per page")
    ap.add_argument("-m", "--max", required=True, type=int, help="Maximum number of tweets")
    args = vars(ap.parse_args())

    query = args['query']
    count = int(args['count'])
    maxtweets = int(args['max'])

    search_twitter_to_json(query, count=count, maxtweets=maxtweets)
