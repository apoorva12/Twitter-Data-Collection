import json
# import sys
import time
# import os
from pymongo import MongoClient
from twython import Twython
from pprint import pprint
import pandas as pd
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


api_key = {
	'api_key': 'OnmbHzqFV94DmaIMVAL03v8Yd',
	'api_secret': '9A0aiIIeW3PpHAamXSkUyHhVH16QNIEyHwGrNMeYI8fStxRoIB',
	'access_token': '4643578124-0x6k9vCvXHZhHNhDHjJht5QyaDLvLpSS9Dktq4G',
	'access_token_secret': 'W5loeOCrk1xIo9Im8tgkRQDZtrB4clSHoEvBypVp5jhvB'
}

twitter= Twython(api_key['api_key'],
				api_key['api_secret'],
				api_key['access_token'],
				api_key['access_token_secret']
				)

# # Insert data in a MongoDB database
def insert_data(post):

	client = MongoClient('localhost', 27017) #connect to the mongo instance running on the system

	db = client['surgical']	#connect to the required data base
	collection = db['strike']	
 	#post['_id'] = post['id']
 	db.strike.insert(post)
 	#df=pd.DataFrame(list(collection.find()))
 	#print(pd.DataFrame(df))


list_of_tweets = []

def search_tweets(search_phrase, maxTweets):
	# ID of the earliest tweet
	id_of_earliest_tweet = -1
	print maxTweets
	count = 0
	tweetCount = 0


	while tweetCount < maxTweets:
		

		if id_of_earliest_tweet <= 0:
			new_statuses = twitter.search(q=search_phrase, count="100", include_entities= True)

		else:
			new_statuses = twitter.search(q=search_phrase, count="100", include_entities = True, max_id=id_of_earliest_tweet - 1)

		tweetCount += len(new_statuses['statuses'])
		#tweetCount=tweetCount+1
		#print len(new_statuses['statuses'])

		for tweet in new_statuses['statuses']:
			count = count+1
			post = tweet
			list_of_tweets.append(post['id'])

			# # Saving data in a MongoDB collection
			insert_data(post)

			# Saving data in files

			#with open('/home/apoorva/Desktop/surgical/'+str(count)+'.json', 'w') as outfile:
			#		json.dump(post,outfile)

		id_of_earliest_tweet = sorted(list_of_tweets)[0]


		# print tc

	print "Total tweets: ", tweetCount

def clean_tweet(tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        val=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])||(\w+:\/\/\S+)", " ", tweet).split())
        #print val
        return val

def get_sentiment(tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1



def collectText():
	client = MongoClient('localhost', 27017) #connect to the mongo instance running on the system

	db = client['surgical']	#connect to the required data base
	collection = db['strike']	
	cursor = collection.find({},{"text":1,"_id":1})

	ptweets=0
	ntweets=0
	tweetsn=0
	Ptw=[]
	Ntw=[]
	twN=[]
	
	for doc in cursor:
		t=get_sentiment(doc['text'])

		if(t==1):
			ptweets=ptweets+1
			Ptw.append(doc['_id'])
		elif(t==0):
			tweetsn=tweetsn+1
			Ntw.append(doc['_id'])
		else:
			ntweets=ntweets+1
			twN.append(doc['_id'])

	return ptweets,ntweets,tweetsn

		
	





# First parameter: The keyword we wish to search for
# Second parameter: Total tweets you wish to collect
var = raw_input()
search_tweets(var,50)

pp,nn,net=collectText()
print pp,nn,net
