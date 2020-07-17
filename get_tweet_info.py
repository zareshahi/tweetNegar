import json
import re
import jdatetime
import tweepy
from requests_oauthlib import OAuth1Session


class GetTweetInfo():
    __api = ''
    __status = ''

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

    def get_user(self, tweet_id):
        ''' get tweet user profile detail
        '''
        status = self.__get_status(id=tweet_id, tweet_mode="extended")
        try:
            user = status.user
            user_detail = {
                'id': user.id,
                'name': user.name,
                'screen_name': user.screen_name,
                'profile_image_url': user.profile_image_url
            }
            return user_detail
        except AttributeError:  # Not a Retweet
            return 'AttributeError'

    def get_date(self, id, lang=''):
        ''' return tweet post date time
        '''
        try:
            status = self.__get_status(id)
            status_date = status.created_at
            date = jdatetime.GregorianToJalali(
                status_date.year, status_date.month, status_date.day)
            if status.lang == 'fa' or lang == 'fa':
                return {
                    'code': '1',
                    'data': {
                        'year': date.jyear,
                        'month': date.jmonth,
                        'day': date.jday,
                        'time': status_date.strftime('%H:%M')
                    },
                    'message': None
                }
            else:
                return {
                    'code': '1',
                    'data': {
                        'year': date.gyear,
                        'month': date.gmonth,
                        'day': date.gday,
                        'time': status_date.strftime('%H:%M')
                    },
                    'message': None
                }
        except AttributeError:
            return {
                'code': '2',
                'data': None,
                'message': "Not Found! - Attribute Error!"
            }

    def __get_status(self, id, tweet_mode='extended'):
        ''' get tweet id and return tweet status if exist
        '''
        if (self.__status and self.__status.id == id):
            return self.__status
        else:
            try:
                self.__status = self.__api.get_status(
                    id=id, tweet_mode=tweet_mode)
                return self.__status
            except:
                return ''

    def get_tweet(self, id):
        ''' get tweet id and return tweet text and user in json format
        '''
        tweet_text = self.get_text(id)
        tweet_user = self.get_user(id)
        tweet_date = self.get_date(id)
        return {
            'tweet': {
                'full_text': tweet_text,
                'created_at': tweet_date['data']
            },
            'user': tweet_user
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
    },
    'english': {
        'id': 1282389642470457345,
        'url': 'https://twitter.com/khamenei_ir/status/1282389642470457345?s=20'
    }
}

twitter = GetTweetInfo()
json_data = []

for tweet in samples:
    tid = samples[tweet]['id']
    json_data.append(twitter.get_tweet(tid))
with open('tmp/tweet.json', 'w', encoding='utf8') as outjson:
    json.dump(json_data, outjson, ensure_ascii=False)
