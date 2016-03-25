# encoding: utf-8

from twitter import *
import os
import argparse

def _parse_args():
    parser = argparse.ArgumentParser("Twitter's Feed Consumer")
    parser.add_argument('--hashtag',
                        help='hashtag to be searched WITHOUT the # signal')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    access_key=os.getenv('TWITTER_ACCESS_KEY')
    access_secret=os.getenv('TWITTER_ACCESS_SECRET')
    consumer_key=os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET')

    args = _parse_args()

    t = Twitter(auth=OAuth(access_key,access_secret,consumer_key,consumer_secret))

    query = t.search.tweets(q='#' + args.hashtag)

    for result in query["statuses"]:
        print "(%s) @%s     %s" % (result["created_at"], result["user"]["screen_name"], result["text"])

