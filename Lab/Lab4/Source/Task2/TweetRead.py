# TweetRead.py
# This first python script doesn’t use Spark at all:

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json
import time

consumer_key = 'kfDc4C3WRQMixHNlrmqyVwBwB'
consumer_secret = 'cKLsUWeFZevvnXMuPrMoY2TkaOyMRibqCfmVHAv0FXv1kWdqQo'
access_token = '712180562-8teeJHgkkJEmibKimkxjKVk1nQ8XhclWk9GW1yyG'
access_secret = 'fdAMA9K4JcqoBrxN94FNLRBqNp0ytA8XNLnR1FWlucYf3'


class TweetsListener(StreamListener):

    def __init__(self, csocket):
        self.client_socket = csocket

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            print(tweet['text'].encode('utf-8'))
            self.client_socket.send(tweet['text'].encode('utf-8'))
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


def sendData(c_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track=['shooting'])


if __name__ == "__main__":
    s = socket.socket()  # Create a socket object
    host = "localhost"  # Get local machine name
    port = 5555  # Reserve a port for your service.
    s.bind((host, port))  # Bind to the port

    print("Listening on port: %s" % str(port))

    s.listen(5)  # Now wait for client connection.
    c, addr = s.accept()  # Establish connection with client.
    time.sleep(5)

    print("Received request from: " + str(addr))

    sendData(c)
