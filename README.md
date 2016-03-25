# twitter-feed-consumer

This repo contains a simple script to query Twitter's feed for some
hashtag.

## Getting Started

1. Go to ```https://apps.twitter.com/``` and create your own application in
order to get both consumer and access keys/secrets

Export them as environment variables like:

```
$ export TWITTER_ACCESS_KEY=<APP_ACCESS_KEY>
$ export TWITTER_ACCESS_SECRET=<APP_ACCESS_SECRET>
$ export TWITTER_CONSUMER_KEY=<APP_CONSUMER_KEY>
$ export TWITTER_CONSUMER_SECRET=<APP_CONSUMER_SECRET>
```

2. Install requirements

```
pip install -r requirements.txt
```


## Use
```
python consumer.py --hashtag <hashtag>
```

P.S.: Hashtag needs to have a # signal before the text
