import re
import json
from textblob import TextBlob
import html
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import words

eng_words = set(words.words())
def word_split(tweet_word, exclude_list=None):
    word_list = []
    if not tweet_word.isalpha():
        return [tweet_word]
    if not exclude_list:
        exclude_list = ()
    
    t = tweet_word
    while t:
        for i in range(len(t), 1, -1):
            segment = t[0: i]
            if (segment in eng_words) and (segment not in exclude_list):
                word_list.append(segment)
                t = t[i:]
                break
            else:
                if word_list:
                    exclude_list.add(word_list[-1])
                    return word_split(tweet_word, exclude_list)
                return [tweet_word]
    return word_list

def parse_tweet(tweet):

    # Escaping html characters
    html_parsed_tweet = html.unescape(tweet)
    print(html_parsed_tweet)

    # Removing apostrophes
    apostrophes = {"'s": "is", "'re": "are", "'l": "will", "'ll": "will", "'em": "them", "'d": "had", "'t": "not", "'m": "am", "'ve": "have"}
    apostrophe_parsed_tweet = [apostrophes[w] if w in apostrophes else w for w in html_parsed_tweet.split()]
    apostrophe_parsed_tweet = " ".join(apostrophe_parsed_tweet)

    # Removing stop words
    stop_words = set(stopwords.words('english'))
    tweet_tokens = word_tokenize(apostrophe_parsed_tweet)
    stop_words_parsed_tweet = [w for w in tweet_tokens if w not in stop_words]

    hash_tags = [w for w in stop_words_parsed_tweet if w[0] == '#']

    # Removing puntuations
    puntuations_removed_tweets = [w for w in stop_words_parsed_tweet if w.isalnum()]
    puntuations_removed_tweets.extend(hash_tags)

    # splitting attached words
    

    tweet = tweet.lower()
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

    #print(eng_words)
    #w = word_split("helloworldlisthere")
    w = word_split("blackworkstrand")
    print(w)

    '''
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
    '''

