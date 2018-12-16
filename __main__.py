import tweepy

from credentials import *
class Listener(tweepy.StreamListener):
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, error):
        print(error)
        return False

def output(tweet):
    #output
    #twitter_name: text
    #try find how to load the image
    pass

def parse(json_string):
    pass

def main():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    stream = tweepy.Stream(auth = api.auth, listener=Listener())

    #follow citizen_tv, nasa, iss, 
    print("streaming")
    stream.filter(follow=["70394965", "11348282"])

if __name__ == '__main__':
    main()
