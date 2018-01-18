import tweepy
import configparser
import time

if __name__ == '__main__':

    #users = ['novogratz', 'SatoshiLite', 'aantonop', 'vitalikbuterin', 'gavinandresen', 'jgarzik']
    user_names = ['novogratz', 'SatoshiLite', 'aantonop', 'vitalikbuterin', 'gavinandresen', 'jgarzik', 'erikvoorhees', 'barrysilbert', 'JihanWu', 'rogerkver', 'nickszabo4', 'VinnyLingham', 'el33th4xor', 'avsa', 
    'jonmatonis', 'petertoddbtc', 'tuurdemeester', 'adam3us', 'balajis', 'charlieshrem', 'naval', 'stephantual', 'RandyHilarski', 'f2pool_wangchun', 'coindesk', 'laurashin',
    'cryptospacesuit', 'WhalePanda', 'BitcoinMagazine', 'bcn', 'dan', 'kingscrown', 'jerrybanfield', 'jeffberwick', 'jrcornel', 'hilarski', 'heiditravels', 'tradealert', 'boxmining',
    'furion', 'someguy123', 'tech-trends', 'bitcoinflood', 'penguinpablo', 'craig-grant', 'trevonjb', 'modprobe', 'barrydutton', 'secret-guru', 'joseph', 'andreolf', 'cryptogee',
    'cryptofreedom', 'krnel', 'me-tarzen', 'zer0hedge', 'adsactly', 'acronym']
    user_names = ['novogratz']

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

    #id1 = api.get_user(screen_name=user1)
    #id2 = api.get_user(screen_name=user2)

    for user in user_names:
        print(user)
        tweets = []
        time.sleep(10)
        t = api.user_timeline(screen_name=user, count=200)
        tweets.extend(t)
        t_id = tweets[-1].id - 1
        while len(t) > 0:
            t = api.user_timeline(screen_name=user, count=200, max_id=t_id)
            tweets.extend(t)
            t_id = tweets[-1].id - 1
        print('# Tweets collected: ' + str(len(tweets)))
        tweets = [t.text for t in tweets]
        with open(user + '.txt', 'w', encoding="utf-8") as f:
            for t in tweets:
                f.write(t + '\n')

    #with open('Tweets.txt', 'w') as f:
    #    for t in tweets:
    #        a = str(t)[2:-1]
    #        f.write(a + '\n')
    print('Data collection complete ...')

