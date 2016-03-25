# encoding: utf-8

from twitter import *
import os

access_key=os.getenv('TWITTER_ACCESS_KEY')
access_secret=os.getenv('TWITTER_ACCESS_SECRET')
consumer_key=os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET')

t = Twitter(auth=OAuth(access_key,access_secret,consumer_key,consumer_secret))

query = t.search.tweets(q='#SomeWeirdHashtag')

for result in query["statuses"]:
    print "(%s) @%s     %s" % (result["created_at"], result["user"]["screen_name"], result["text"])

