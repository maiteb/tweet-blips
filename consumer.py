# encoding: utf-8

from twitter import *
import os
import argparse
from tweet import Tweet
from export_google_sheet import export_all

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
        tweet = Tweet(result['created_at'], result['user']['screen_name'], result['user']['name'],result['text'])
        if tweet.blip is not None:
            tweets.append(tweet)
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

    if not query['statuses']:
        print "No new tweet was found with the hashtag #" + args.hashtag
    else:
        max_id, tweets =_parse_tweets(query["statuses"], last_id_found)
        _update_max_id(max_id)
        export_all(tweets)
        print "We exported " + str(len(tweets)) + " new tweets with the hashtag #" + args.hashtag + " to the Google Sheet"
