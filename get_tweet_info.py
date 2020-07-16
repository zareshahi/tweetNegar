import json
import re

import tweepy
from requests_oauthlib import OAuth1Session


class GetTweetInfo():
    __api = ''
    __status = {
        'id': ''
    }

    def __init__(self):
        self.__authorization()

    def __authorization(self):
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

        self.__api = tweepy.API(auth)

    def get_text(self, tweet_id):
        ''' get tweet long text by tweet id
        '''
        status = self.__get_status(id=tweet_id, tweet_mode="extended")
        try:
            return re.sub(r"http\S+$", "", status.retweeted_status.full_text)
        except AttributeError:  # Not a Retweet
            try:
                return re.sub(r"http\S+$", "", status.full_text)
            except:
                return 'Not Found!'

    def get_author(self, tweet_id):
        ''' get tweet author profile detail
        '''
        status = self.__get_status(id=tweet_id, tweet_mode="extended")
        try:
            author = status.author
            author_detail = {
                'id': author.id,
                'name': author.name,
                'username': author.screen_name,
                'profile_image': author.profile_image_url
            }
            return author_detail
        except AttributeError:  # Not a Retweet
            return 'AttributeError'

    def __get_status(self, id, tweet_mode='extended'):
        ''' get tweet id and return tweet status if exist
        '''
        if (self.__status['id'] == id):
            return self.__status
        else:
            try:
                self.__status = self.__api.get_status(
                    id=id, tweet_mode=tweet_mode)._json
                return self.__status
            except:
                return ''

    def get_tweet(self, id):
        ''' get tweet id and return tweet text and user in json format
        '''
        tweet_text = self.get_text(id)
        tweet_author = self.get_author(id)
        return {
            'tweet': tweet_text,
            'author': tweet_author
        }


samples = {
    'with_photo': {
        'id': 1282931844716126208,
        'url': 'https://twitter.com/m_mkia8/status/1282931844716126208?s=20'
    },
    'normal': {
        'id': 1282932074584973313,
        'url': 'https://twitter.com/zohreyezahra/status/1282932074584973313?s=20'
    },
    'qute': {
        'id': 1282821340043542529,
        'url': 'https://twitter.com/syjebraily/status/1282821340043542529?s=20'
    },
    'reply': {
        'id': 1282931657121468417,
        'url': 'https://twitter.com/mohammad_amin23/status/1282931657121468417?s=20'
    },
    'retweet': {
        'id': 1282732786688958464,
        'url': 'https://twitter.com/pariis_tar/status/1282732786688958464?s=20'
    },
    'removed': {
        'id': 1283001644892909568,
        'url': 'https://twitter.com/moeb_ir/status/1282927709795090432'
    },
    'video': {
        'id': 1233848803914059781,
        'url': 'https://twitter.com/Alireza_gh_97_4/status/1233848803914059781?s=20'
    },
    'rashto': {
        'id': 1279989094349750272,
        'url': 'https://twitter.com/MortezaJaliliIR/status/1279989094349750272?s=20'
    }
}

twitter = GetTweetInfo()
json_data = []

for tweet in samples:
    tid = samples[tweet]['id']
    json_data.append(twitter.get_tweet(tid))
with open('tmp/tweet.json', 'w', encoding='utf8') as outjson:
    json.dump(json_data, outjson, ensure_ascii=False)
