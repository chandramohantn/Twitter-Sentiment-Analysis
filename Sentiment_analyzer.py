import re
import json
import numpy as np
from textblob import TextBlob
from unidecode import unidecode

def parse_tweet(tweet):
    tweet = ' '.join([unidecode(i.decode('utf-8')) for i in tweet.split()])
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_sentiment(tweet):
    parsed_tweet = parse_tweet(tweet)
    tb = TextBlob(parsed_tweet)
    if tb.sentiment.polarity > 0:
        return parsed_tweet, 'Positive'
    elif tb.sentiment.polarity == 0:
        return parsed_tweet, 'Neutral'
    else:
        return parsed_tweet, 'Negative'

if __name__ == '__main__':

    data = []
    #with open('Tweets.txt', 'r') as f:
    with open('novogratz.txt', 'r', encoding="utf-8") as f:
        for line in f:
            data.append(line[0:-1])

    p_c = 0
    n_c = 0
    sentiment_dataset = []
    for d in data:
        data = {}
        t, s = get_sentiment(d)
        data[t] = s
        sentiment_dataset.append(data)
        if s == 'Positive':
            p_c += 1
        elif s == 'Negative':
            n_c += 1

    print('# Tweets with postive sentiment: ' + str(p_c))
    print('# Tweets with negative sentiment: ' + str(n_c))
    print('# Tweets with neutral sentiment: ' + str(len(sentiment_dataset)-p_c-n_c))
    with open('Twitter_sentiment_dataset.json', 'w') as f:
        for data in sentiment_dataset:
            json.dump(data, f)
            f.write('\n')
    print('Dataset created .....')

