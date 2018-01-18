import json
from kafka import SimpleProducer, KafkaClient
import tweepy
import configparser
import datetime
import numpy as np

count = 0

class TweeterStreamListener(tweepy.StreamListener):
    """ A class to read the twitter stream and push it to Kafka"""

    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        client = KafkaClient("localhost:9092")
        self.producer = SimpleProducer(client, async = True, batch_send_every_n = 1000, batch_send_every_t = 10)

    def on_status(self, status):
        """ This method is called whenever new data arrives from live stream. We asynchronously push this data to kafka queue"""
        global count

        if count == 0:
            dt = status.created_at
        tweet =  status.text.encode('utf-8')
        tc = status.created_at
        td = divmod((tc - dt).total_seconds(), 2)[0]
        if td <= 1.0:
            tw_count += 1
        else:
            msg = twitter_anomaly.online_anomaly_detector(tw_count)
            tw_count = 1
            dt = tc
            try:
                self.producer.send_messages('twitteranomaly', msg)
                return True
            except Exception as e:
                print(e)
                return False
        count += 1
        if count % 100 == 0:
            print('Saving plot and model ......')
            twitter_anomaly.plot_performance()
            twitter_anomaly.plot_loss()
            twitter_anomaly.save_anomaly_model()
        return True

    def on_error(self, status_code):
        print("Error received in kafka producer")
        return True # Don't kill the stream

    def on_timeout(self):
        return True # Don't kill the stream

if __name__ == '__main__':

    user1 = 'Mike Novogratz'
    user2 = 'Charlie Lee'

    # Read the credententials from 'twitter-app-credentials.txt' file
    config = configparser.ConfigParser()
    config.read('twitter-credentials.txt')
    consumer_key = config['DEFAULT']['consumerKey']
    consumer_secret = config['DEFAULT']['consumerSecret']
    access_key = config['DEFAULT']['accessToken']
    access_secret = config['DEFAULT']['accessTokenSecret']

    # Create Auth object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    id1 = api.get_user(screen_name=user1)
    id2 = api.get_user(screen_name=user2)

    tweets = []
    t = api.user_timeline(screen_name=user1, count=200)
    tweets.extend(t)
    t_id = tweets[-1].id - 1
    while len(t) > 0:
        t = api.user_timeline(screen_name=user1, count=200, max_id=t_id)
        tweets.extend(t)
        t_id = tweets[-1].id - 1
    print('# Tweets from ' + user1 + ': ' + len(tweets))

    t = api.user_timeline(screen_name=user2, count=200)
    tweets.extend(t)
    t_id = tweets[-1].id - 1
    while len(t) > 0:
        t = api.user_timeline(screen_name=user2, count=200, max_id=t_id)
        tweets.extend(t)
        t_id = tweets[-1].id - 1
    print('# Tweets from ' + user2 + ': ' + len(tweets))
    #tweets = [t.text.encode('utf-8') for t in tweets]

    with open('Tweets.txt', 'w') as f:
        for t in tweets:
            f.write(t + '\n')
    print('Data collection complete ...')

    # Create stream and bind the listener to it
    #stream = tweepy.Stream(auth, listener = TweeterStreamListener(api))

    #Custom Filter rules pull all traffic for those filters in real time.
    #stream.filter(locations=[-180,-90,180,90], languages = ['en'])
    #stream.filter(track = ['gujarat', 'modi', 'polls', 'bjp'], languages = ['en'])
    #stream.filter(track = ['football'], languages = ['en'])

