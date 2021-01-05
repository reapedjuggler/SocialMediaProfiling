import tweepy
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
import time as t
from collections import Counter
import sys
import re
import json
from textblob import TextBlob
import networkx as nx
from networkx.readwrite import json_graph
import config

consumer_key=config.consumer_key
consumer_secret=config.consumer_secret
access_token=config.access_token
access_token_secret=config.access_token_secret
tweet_count = 0

auth = OAuthHandler(consumer_key, consumer_secret) 
  
# set access to user's access key and access secret  
auth.set_access_token(access_token, access_token_secret) 
  
# calling the api  
auth_api = API(auth) 
auth_api.favorites()
end_date = datetime.utcnow() - timedelta(days=30)
cur = Cursor(auth_api.user_timeline, id='@ReapedJ').items()
# for status in cur:
#     tweet_count+=1
#     if hasattr(status,"id"):
#         print(status.id)
#         #geeting the retweeters
#         retweets_list = auth_api.retweets(status.id)
#         for retweet in retweets_list: 
#             print(retweet.user.screen_name) 
#     #print(status)
#     if tweet_count==10:
#         break
cur1 = Cursor(auth_api.favorites, id='@ReapedJ').items(20)
for favorite in cur1:
    print(favorite.user.screen_name)


  


  

