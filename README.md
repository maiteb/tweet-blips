# tweet-blips

This repo contains a simple script to query Twitter's feed for some
hashtag.
After that we will create blips for Technology Radar
(https://www.thoughtworks.com/radar) from the consumed tweets.
To achieve that, the script expects that tweet which was found has the
following structure:

```
Quadrant - Cycle - Blip
```

Where ```Quadrant``` can be Techniques, Platforms, Tools or Languages
& Frameworks; while ```Cycle``` can be Hold, Access, Trial or Adopt.
For both of them, the script accepts the terms in Brazilian Portuguese.

```Blip``` will be a text-free section to describe what you're
suggesting.

### Example

```
Tools - Trial - Docker Toolbox #HashtagToBeSearched
```

```
Techniques - Access - BFF (Backend for Frontend) #HashtagToBeSearched
```

```
Linguagens e Frameworks - Adote - ES6 #HashtagToBeSearched
```

All the filtered tweets will be saved into a Google Spreadsheet to feed
(https://github.com/ThoughtWorksInc/tech-radar)

## Getting Started

- Go to ```https://apps.twitter.com/``` and create your own application in
order to get both consumer and access keys/secrets

Export them as environment variables like:

```
$ export TWITTER_ACCESS_KEY=<APP_ACCESS_KEY>
$ export TWITTER_ACCESS_SECRET=<APP_ACCESS_SECRET>
$ export TWITTER_CONSUMER_KEY=<APP_CONSUMER_KEY>
$ export TWITTER_CONSUMER_SECRET=<APP_CONSUMER_SECRET>
```
- Go to ```https://console.developers.google.com/```, create a project
and then create a service account credential.

Export them as environment variables like:

```
export GSPREAD_CLIENT_EMAIL=<GOOGLE_CLIENT_EMAIL>
export GSPREAD_PRIVATE_KEY_ID=<GOOGLE_PRIVATE_KEY_ID>
export GSPREAD_PRIVATE_KEY=<GOOGLE_PRIVATE_KEY>
```

- Create a Google Spreadsheet and share it with the GOOGLE_CLIENT_EMAIL
generated in the step above.
Export the spreadsheet name as environment variable like:

```
export GSPREAD_SHEET_NAME=<GOOGLE_SPREADSHEET_NAME>
```
- You'll need to have a sheet, at the same spreadsheet, with the latest version of radar's blips, in order to identify if some blip is new or not.
Export the sheet name as environment variable like:

```
export GSPREAD_PREVIOUS_RADAR_NAME=<SHEET_NAME_WITH_AN_OLDER_VERSION_OF_RADAR>
```

- Install requirements

```
pip install -r requirements.txt
```

## Run
```
python consumer.py --hashtag <hashtag>
```

Where ```--hashtag ``` will be the one to be searched, but you don't
need to add the # signal when executing this script
