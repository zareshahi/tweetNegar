import json

import tweepy


class Twitter():
    def init(self, id):
        # tweet = [{
        #     text: self.get_text(id),
        #     author: self.get_author
        # }]
        pass

    def get_text(self, tweet_id):
        ''' get tweet long text by tweet id
        '''
        status = self.get_status(id=tweet_id, tweet_mode="extended")
        try:
            return status.retweeted_status.full_text
        except AttributeError:  # Not a Retweet
            try:
                return status.full_text
            except:
                return 'Not Found!'

    def get_author(self, tweet_id):
        ''' get tweet author profile detail
        '''
        status = self.get_status(id=tweet_id, tweet_mode="extended")
        try:
            author = status.author
            author_detail = {
                'id': author.id,
                'name': author.name,
                'user_name': author.secret_name,
                'profile_image': author.profile_image_url
            }
            return author_detail
        except AttributeError:  # Not a Retweet
            return 'AttributeError'

    def get_status(self, id, tweet_mode='extended'):
        try:
            return api.get_status(id=id, tweet_mode="extended")
        except:
            return ''


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

twitter = Twitter()

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
        'id': 1282927709795090432,
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

# get tweet by list of id
public_tweets = api.statuses_lookup([1281841440570650625, 1281969401420554241])
file = open('tweet.txt', 'w')
for tweet in samples:
    tid = samples[tweet]['id']
    file.write(twitter.get_text(tid))
    file.writelines('\n')
    file.writelines('\n')
    file.write(twitter.get_author(tid))
    file.writelines('\n')
    file.write('==========================================================')
    file.writelines('\n')
file.close()
