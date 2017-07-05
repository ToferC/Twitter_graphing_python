import time
import os
import sys
import json
import argparse
import csv
import preprocessor as p

RESULTS_DIR = os.path.join(os.path.curdir, "results/")
DATA_DIR = "/home/chris/data"

# Process a csv single status



with open(os.path.join(DATA_DIR, "gc2020_innovation_fair_2017.csv")) as r:
    reader = csv.reader(r, delimiter=",", quotechar='"')
    next(reader, None)
    for row in reader:
        link, date, time, author_id, followers, following, content, *extra = row

        url, id_str = link.split("statuses/")

        hashtags = []
        mentions = []
        url_strings = []

        parsed_tweet = p.parse(content)

        try:
            for hashtag in parsed_tweet.hashtags:
                hashtags.append(hashtag.match)
        except TypeError:
            pass

        try:
            for mention in parsed_tweet.mentions:
                mentions.append(mention.match)
        except TypeError:
            pass

        try:
            for url_string in parsed_tweet.urls:
                url_strings.append(url_string.match)
        except TypeError:
            pass


        print(f'''ID:{id_str}\n
                Hashtags:{hashtags}\n
                Mentions: {mentions}\n''')