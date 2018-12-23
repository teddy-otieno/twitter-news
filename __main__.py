import tweepy
import subprocess
import json
import socket
import threading
import sys
from credentials import *

#TODO: Filters
#FEATURE: server client protocol, to add and remove user id's in real time
#Add userIDs of the accounts you want to get news from
FOLLOW = [
        "56510427", #motherboard
        "333430027", #manjarolinux
        "50052513", #freebsd
        "300789811",
        "742143",
        "14706299",
        "2097571",
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
    
    if 'RT @' not in tweet['text'] and tweet['user']['id_str'] in FOLLOW:
        message = Message(tweet['user']['name'], tweet['text'])
    else:
        message = Message(out=False) 
    return message

def save_to_filesystem(user_id):
    file_location = "/home/teddy/Projects/Python/twitter-news/user_ids_store"

    temporary_user_ids = []

    with open(file_location, 'r') as File:
        file_output = File.read()
        for user_id in file_output.split('\n'):
            temporary_user_ids.append(user_id)

    if user_id not in temporary_user_ids:
        with open(file_location, 'a') as File:
            File.write(user_id + "\n")

        return True

    else:
        return False

def server():
    print("Server started")
    host = 'localhost'
    port = 9090
    
    #change to unix-sockets
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind((host, port))

    connection.listen(10)
    while True:
        conn, address = connection.accept()
        print("Connection received")

        user_id = str(conn.recv(1024), 'utf-8')
        if user_id not in FOLLOW and save_to_filesystem(user_id):
            FOLLOW.append(user_id)
            conn.send(b"User ID updated succesfully")
        else:
            conn.send(b"User ID already present, update failed")
        conn.close()

def main():
    print(FOLLOW)
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    stream = tweepy.Stream(auth = api.auth, listener=Listener())

    print("streaming")
    stream.filter(follow=FOLLOW)

if __name__ == '__main__':
    try:
        main_thread = threading.Thread(target=main)
        server_thread = threading.Thread(target=server)

        server_thread.start()
        main_thread.start()
    except e:
        main_thread.join()
        server_thread.join()
        print("Exeception {} occured, server stopped".format(e))
        sys.exit()

