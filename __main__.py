import tweepy
import subprocess
import json
from credentials import *

FOLLOW = [  
        "70394965",
        "11348282",
        "53037279",
        "115141256",
        "25985333",
            ]

class Listener(tweepy.StreamListener):
    def on_data(self, data):
        #jprint(data)
        output(parse(data))
        return True

    def on_error(self, error):
        return False

class Message:
    def __init__(self, title=None, body=None, out=True):
        self.title = title
        self.body = body
        self.out = out

    def __str__(self):
        return "{} {}".format(self.title, self.body)

def output(message):
    #output
    #twitter_name: text
    #try find how to load the image
    if message.out == True:
        subprocess.run(['notify-send', '--urgency=normal', message.title, message.body])

def parse(json_string):
    tweet = json.loads(json_string)

    if 'RT @' not in tweet['text'] and tweet['user']['id'] in FOLLOW:
        message = Message(tweet['user']['name'], tweet['text'])
    else:
        message = Message(out=False) 
    return message

def main():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    stream = tweepy.Stream(auth = api.auth, listener=Listener())

    print("streaming")
    stream.filter(follow=FOLLOW)

if __name__ == '__main__':
    main()
