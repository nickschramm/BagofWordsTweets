import tweepy
import pandas as pd
import time
import re
import numpy as np
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import sys
import operator
import itertools

consumer_key = "XTVHb8OVmWDh6Me0J1P2ngHkS"
consumer_secret = "ZQKjd0jglZhUIvLHt2ByPEp5kXf9DQJm0Atmmqz4MQYOF0Ui9U"
access_token = "1438000553380962307-XlGvVGQpxgqKlONv4C9NbG5FKsin6J"
access_token_secret = "rp2sDzFrhQqEfq538EnhLtj3SegEkEeP8SPVVGe6xtwBP"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

tweets = []

def username_tweets_to_csv(username,count):
    try:      
        tweets = api.user_timeline(screen_name = username, count = count, include_rts = False)
        tweets_list = [[tweet.text] for tweet in tweets]
        tweets_df = pd.DataFrame(tweets_list,columns=['Text'])
        tweets_df = tweets_df.iloc[20:, :]
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
                     "now", "im", "us"]
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
          


# Input username and count to return x most recent tweets from user
users = ['SimuLiu', 'KenJennings', 'KDTrey5', 'jack', 'GTMBB',
         'KevinHart4real', 'CaucasianJames', 'tylerthecreator',
         'nytimes', 'BarackObama']

count = 10000
usertweets = []
for user in users:
    usertw = username_tweets_to_csv(user, count)
    usertweets.append(usertw)

data1, data2, data3, data4, data5, data6, data7, data8, data9, data10 = usertweets
alldata = [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10]

mostcomlist = []
mostcomfreqlist = []
dictlist = []
for data in alldata:
    diction = {}
    for word in data:
        if word in diction.keys():
            diction[word] = 1 + diction[word]
        else:
            diction[word] = 1

    diction = {k: v for k, v in sorted(diction.items(), reverse = True, key=lambda item: item[1])}
    dictlist.append(diction)
    mostcom = dict(list(diction.items())[0:500])
    mostcomfreq = mostcom.values()
    mostcom = mostcom.keys()
    mostcomlist.append(mostcom)
    mostcomfreqlist.append(mostcomfreq)
    
mostcom1, mostcom2, mostcom3, mostcom4, mostcom5, mostcom6, mostcom7, mostcom8, mostcom9, mostcom10 = mostcomlist
allmostcom = [mostcom1, mostcom2, mostcom3, mostcom4, mostcom5, mostcom6, mostcom7, mostcom8, mostcom9, mostcom10]

dict1, dict2, dict3, dict4, dict5, dict6, dict7, dict8, dict9, dict10 = dictlist
alldict = [dict1, dict2, dict3, dict4, dict5, dict6, dict7, dict8, dict9, dict10]

print("Input the tweet you want to classify by typing it out, copy/pasting, or any other method. Don't worry about punctuation and capitalization.")
test = input("Type Tweet to Analyze: ")
contest = test

test = re.sub(r"[@]([^\s]+)", '', test)
test = re.sub("[']", '', test)
#test = re.sub("[\n, \t, [-], (, ), /, :, ;]", ' ', test)
test = test.replace("…", '')
test = test.replace("-", " ")
test = test.replace(",", " ")
test = test.replace("?", " ")
test = test.replace("!", " ")
test = test.replace("/", " ")
test = test.replace(":", " ")
test = test.replace(";", " ")
test = test.replace("~", " ")
test = test.replace("`", " ")
test = test.replace("&", " ")
test = test.replace("^", " ")
test = test.replace("%", " ")
test = test.replace("$", " ")
test = test.replace("#", " ")
test = test.replace("*", " ")
test = test.replace("(", " ")
test = test.replace(")", " ")
test = test.replace("[", " ")
test = test.replace("]", " ")
test = test.replace("{", " ")
test = test.replace("}", " ")
test = test.replace("|", " ")
test = test.replace("<", " ")
test = test.replace("=", " ")
test = test.replace("+", " ")
test = test.replace("_", " ")
test = test.replace(">", " ")
test = test.replace(".", " ")
test = test.replace('"', " ")
test = test.lower()
    
testsplit = test.split()

inputlist = []
for word in testsplit:
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

rates = []
for (mostcom, diction) in zip(allmostcom, alldict):
    sentence_vector = []
    for (key, word) in zip(diction, inputlist):
        if word in mostcom:
            sentence_vector.append(diction[key])
        else:
            sentence_vector.append(0)
    yes = 0
    total = 0
    for entry in sentence_vector:
        if entry > 1:
            val = entry
            yes += val
            total += 1
        elif entry == 1:
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

resultdict = dict(zip(users, rates))
resultlist = sorted(resultdict.items(), key=operator.itemgetter(1))
mostlik = resultlist[-1][0]
prob = resultlist[-1][1]
prob = prob * 100
prob = round(prob, 2)

print("")
print("Tweet being tested: " + str(contest))
print("")
print("This tweet was most likely tweeted by " + str(mostlik) + " with a similarity of " + str(prob) + "% to their other tweets.")
print("")
print("The similarity of the rest of the users given is as follows:")

p = 2
for user in resultlist:
    try:
        mostlike = resultlist[-p][0]
        prob = resultlist[-p][1]
        prob = prob * 100
        prob = round(prob, 2)
        print(str(mostlike) + ": " + str(prob) + "%")
        p += 1
    except:
        pass

