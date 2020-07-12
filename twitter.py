import json

import tweepy

# use config json file to hide security API keys
# config.json is git ignored - you can see this file template in
# config.template.json
with open('./config.json') as json_file:
    config_json = json.load(json_file)
# initial config keys from config.json file
consumer_key = config_json['twitter']['api_key']
consumer_secret = config_json['twitter']['api_key_secret']
access_token = config_json['twitter']['access_token']
access_token_secret = config_json['twitter']['access_token_secret']
# use tweepy to authorization twitter api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# get tweet by list of id
public_tweets = api.statuses_lookup([1281841440570650625, 1281969401420554241])
file = open('tweet.txt', 'w')
for tweet in public_tweets:
    file.write(tweet.text)
    file.writelines('\n')
    file.writelines('\n')
    file.writelines('\n')
    file.writelines('\n')
file.close()
