import time
import os
import sys
import json
import argparse
import preprocessor as p
import csv

RESULTS_DIR = os.path.join(os.path.curdir, "results/")
DATA_DIR = "/home/chris/data"

# Process a csv single status
def csv_to_json(filename, output_file):

    d = {}

    with open(os.path.join(DATA_DIR, filename), encoding="utf-8") as r:
        reader = csv.reader(r, delimiter=",", quotechar='"')

        next(reader, None)
        for row in reader:
            link, date, time, author_id, followers, following, *content_rows= row

            content = ""

            for row in content_rows:
                content += f" {row}"

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
                print(f"{author_id}: {content}")

            try:
                for url_string in parsed_tweet.urls:
                    url_strings.append(url_string.match)
            except TypeError:
                pass

                d[id_str] = {
                'id_str': id_str,
                'date': date,
                'text': content,

                # To do: tokenize tweet to get retweets

                'retweet_count': 0,
                'favorite_count': 0,
                'reply_to': 0,
                'coordinates': 0,
                'reply_to_tweet': 0,
                'user_screen_name': f"@{author_id}",
                'quoted_status': 0,
                'lang': 0,
                'entities': 0,
                'urls': url_strings,
                'hashtags': hashtags,
                'user_mentions': mentions,
                'user': author_id,
                }

    with open(os.path.join(RESULTS_DIR, "converted_"+output_file+".json"), 'w') as f:  
        f.write(json.dumps(d, indent=1))

    print("Success")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filename", required=True, help="Enter file name")
    ap.add_argument("-o", "--output", required=True, help="Enter output file name")
    args = vars(ap.parse_args())

    filename = args['filename']
    output_file = args['output']

    csv_to_json(filename, output_file)
