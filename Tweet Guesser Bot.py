import tweepy
import time
import pandas as pd
import time
import re
import numpy as np
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import sys
import operator
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime, timedelta
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime, timedelta

consumer_key = "XTVHb8OVmWDh6Me0J1P2ngHkS"
consumer_secret = "ZQKjd0jglZhUIvLHt2ByPEp5kXf9DQJm0Atmmqz4MQYOF0Ui9U"
access_token = "1438000553380962307-XlGvVGQpxgqKlONv4C9NbG5FKsin6J"
access_token_secret = "rp2sDzFrhQqEfq538EnhLtj3SegEkEeP8SPVVGe6xtwBP"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

user1 = 'KDTrey5'
user2 = 'BarackObama'
user3 = 'jack'
userslist = [user1, user2, user3]
count = 25

def username_tweets_to_csv(username,count):
    try:      
        tweets = api.user_timeline(screen_name = username, count = count, include_rts = False)
        tweets_list = [[tweet.text] for tweet in tweets]
        tweets_df = pd.DataFrame(tweets_list,columns=['Text'])
        
        tweets_df.to_csv('{}-tweets.csv'.format(username), sep=',', index = False)
        
        pd.options.display.max_colwidth = 250
        
        tweets_df['Text'] = tweets_df['Text'].apply(lambda x: re.split('https:\/\/.*', str(x))[0])
        tweets_df['Text'] = tweets_df['Text'].str.replace(r"[@]([^\s]+)", '', regex = True)
        tweets_df['Text'] = tweets_df['Text'].str.replace("[']", '', regex = True)
        tweets_df['Text'] = tweets_df['Text'].str.replace("[\n, \t, -, (, ), /, :, ;, !, ?]", ' ', regex = True)
        tweets_df['Text'] = tweets_df['Text'].str.replace("[…]", '', regex = True)
        tweets_df['Text'] = tweets_df['Text'].str.replace(r'[^\w\s]','', regex = True)
        tweets_df['Text'] = tweets_df['Text'].str.lower()
        
        tweets_list = tweets_df['Text'].values.tolist()
        newlist = []
        for tweet in tweets_list:
            newtweet = tweet.split()
            newlist.append(newtweet)

        flatlist = []
        for tweet in newlist:
            for word in tweet:
                flatlist.append(word)

        stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                     "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
                     "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
                     "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
                     "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as",
                     "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through",
                     "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
                     "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how",
                     "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
                     "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should",
                     "now"]
        for word in list(flatlist):
            if word in stopwords:
                flatlist.remove(word)

        for word in list(flatlist):
            if word[:-3] == 'ing':
                word = word[:-3]

        return flatlist
        
    except BaseException as e:
          print('failed on_status,',str(e))
          time.sleep(3)
          
user1tw = username_tweets_to_csv(user1, count)
user2tw = username_tweets_to_csv(user2, count)
user3tw = username_tweets_to_csv(user3, count)

mostcomlist = []
for data in userslist:
    diction = {}
    for word in data:
        if word in diction.keys():
            diction[word] = 1 + diction[word]
        else:
            diction[word] = 1

    diction = {k: v for k, v in sorted(diction.items(), reverse = True, key=lambda item: item[1])}

    mostcom = dict(list(diction.items())[0:250])
    mostcom = mostcom.keys()
    mostcomlist.append(mostcom)

mostcom1, mostcom2, mostcom3 = mostcomlist
allmostcom = [mostcom1, mostcom2, mostcom3]

def tweet_clean(tweet):
    tweet = re.sub(r"[@]([^\s]+)", '', tweet)
    tweet = re.sub("[']", '', tweet)
    tweet = tweet.replace("…", '')
    tweet = tweet.replace("-", " ")
    tweet = tweet.replace(",", " ")
    tweet = tweet.replace("?", " ")
    tweet = tweet.replace("!", " ")
    tweet = tweet.replace("/", " ")
    tweet = tweet.replace(":", " ")
    tweet = tweet.replace(";", " ")
    tweet = tweet.replace("~", " ")
    tweet = tweet.replace("`", " ")
    tweet = tweet.replace("&", " ")
    tweet = tweet.replace("^", " ")
    tweet = tweet.replace("%", " ")
    tweet = tweet.replace("$", " ")
    tweet = tweet.replace("#", " ")
    tweet = tweet.replace("*", " ")
    tweet = tweet.replace("(", " ")
    tweet = tweet.replace(")", " ")
    tweet = tweet.replace("[", " ")
    tweet = tweet.replace("]", " ")
    tweet = tweet.replace("{", " ")
    tweet = tweet.replace("}", " ")
    tweet = tweet.replace("|", " ")
    tweet = tweet.replace("<", " ")
    tweet = tweet.replace("=", " ")
    tweet = tweet.replace("+", " ")
    tweet = tweet.replace("_", " ")
    tweet = tweet.replace(">", " ")
    tweet = tweet.replace(".", " ")
    tweet = tweet.replace('"', " ")
    tweet = tweet.lower()
    
    tweetsplit = tweet.split()

    inputlist = []
    for word in tweetsplit:
        inputlist.append(word)

    stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                 "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
                 "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
                 "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
                 "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as",
                 "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through",
                 "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
                 "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how",
                 "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
                 "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should",
                 "now"]

    for word in list(inputlist):
        if word in stopwords:
            inputlist.remove(word)

    for word in list(inputlist):
        if word[:-3] == 'ing':
            word = word[:-3]

    return inputlist

def tweet_class(inputlist):
    rates = []
    for mostcom in allmostcom:
        sentence_vector = []
        for word in inputlist:
            if word in mostcom:
                sentence_vector.append(1)
            else:
                sentence_vector.append(0)

        yes = 0
        total = 0
        for entry in sentence_vector:
            if entry == 1:
                yes += 1
                total += 1
            else:
                total += 1
        try:
            yesrate = yes / total
            rates.append(yesrate)
        except:
            print("Tweet Not Unique Enough! Please Try Again!")
            sys.exit()
                 
    return rates

print(userslist) 
def tweet_output(rates):
    resultdict = dict(zip(userslist, rates))
    resultlist = sorted(resultdict.items(), key=operator.itemgetter(1))
    mostlik = resultlist[-1][0]
    prob = resultlist[-1][1]
    prob = prob * 100
    prob = round(prob, 2)

    output = "This tweet was most likely tweeted by " + str(mostlik) + " with a similarity of " + str(prob) + "% to their other tweets."

def get_tweets1(username):
    try:
        m = tweet
        tweet = api.user_timeline(screen_name = username, count = 1)
        tweet = tweet[0]._json['text']
        twid = tweet[0]._json['id']
        url = "https://twitter.com/twitter/statuses/" + str(twid)
        if m == tweet:
            pass
        else:
            inputlist = tweet_clean(tweet)
            rates = tweet_class(inputlist)
            output = tweet_output(rates)
            api.update_status(status = output, attachment_url = url)
    except:
        tweet = api.user_timeline(screen_name = username, count = 1)
        twid = (tweet[0]._json['id'])
        tweet = tweet[0]._json['text']
        url = "https://twitter.com/twitter/statuses/" + str(twid)
        inputlist = tweet_clean(tweet)
        rates = tweet_class(inputlist)
        output = tweet_output(rates)
        api.update_status(status = output, attachment_url = url)

        

def periodic_work(interval):
    while True:
        get_tweets1(user1)
        time.sleep(interval)

periodic_work(60 * 0.1)




