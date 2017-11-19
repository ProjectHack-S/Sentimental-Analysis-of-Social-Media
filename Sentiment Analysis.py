import re
import quandl
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

import datetime


df=quandl.get("NSE/WIPRO", authtoken="f6EtYx5cGerm4iysqayn")

t=df[len(df)-10:]
t=t[['High']]
import numpy as np
price=np.array(t)
avg=0

for i in price:
	avg=avg+i
avg=avg/10
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'PekUJeEJHeNi2D9qxfYXPQ9Lo'
        consumer_secret = 'kyVERjh8hiSIAyTIQDWXit7PPK2wpXtA41VQX2aV163gC5KE8F'
        access_token = '563410681-Jsxm8OmpKQNvZA3WbT7WTvTzcPEwwnmGMpB09ism'
        access_token_secret = 'Ok9ym5RS8y5Jpn1pu2PdPAUwtS6Ed4FFdELaOH47JIpUJ'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        
   
        analysis = TextBlob(self.clean_tweet(tweet))
       
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        
        tweets = []

        try:
            
            fetched_tweets = self.api.search(q = query, count = count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query = 'WIPRO', count = 200)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    t=len(ptweets)
    
    l=np.correlate([t],avg)
    print(l/10000)
 

    
    

if __name__ == "__main__":
    # calling main function
    main()
    

