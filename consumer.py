# encoding: utf-8

from twitter import *
import os
import argparse

class Tweet:

    def __init__(self, date, username, name, content):
        self.date = date
        self.username = username.encode('ascii', 'ignore')
        self.name = name.encode('ascii', 'ignore')
        self.content = content.encode('ascii', 'ignore')

    def __str__(self):
        return "[%s] %s (@%s): %s" % (self.date, self.name, self.username, self.content)

def _parse_args():
    parser = argparse.ArgumentParser("Twitter's Feed Consumer")
    parser.add_argument('--hashtag',
                        help='hashtag to be searched WITHOUT the # signal')
    args = parser.parse_args()
    return args

def _parse_tweets(statuses,max_id):
    tweets = []
    for result in statuses:
        current_id = long(result['id_str'])
        if max_id < current_id:
            max_id = current_id
        tweets.append(Tweet(result['created_at'], result['user']['screen_name'], result['user']['name'],result['text']))
    return max_id, tweets

def _find_last_id_found():
    if os.path.exists('last_id_found'):
        file_last_id = open('last_id_found', 'r')
        last_id = file_last_id.read()
        file_last_id.close()
        return last_id

    return '0'

def _update_max_id(max_id):
    file_last_id = open('last_id_found', 'w+')
    file_last_id.write(str(max_id))
    file_last_id.close()

if __name__ == '__main__':
    access_key=os.getenv('TWITTER_ACCESS_KEY')
    access_secret=os.getenv('TWITTER_ACCESS_SECRET')
    consumer_key=os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET')

    args = _parse_args()

    t = Twitter(auth=OAuth(access_key,access_secret,consumer_key,consumer_secret))

    last_id_found = long(_find_last_id_found())
    query = t.search.tweets(q='#' + args.hashtag,count=50, since_id=last_id_found)

    max_id, tweets =_parse_tweets(query["statuses"], last_id_found)
    _update_max_id(max_id)

    for tweet in tweets:
        print tweet
