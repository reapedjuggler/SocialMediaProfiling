from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
import re
from textblob import TextBlob

consumer_key="ypMrlvPrwKt1jHRnnaJEC3y44"
consumer_secret="YtghWkKZiRDdPLWUUNu8Jdd6vqAMF3acC7LpAQrzyCMrXNhXvy"
access_token="2900093502-AOOl23W2HDvpmI94QAg7GWA3ChlsvkTQcV97Cm7"
"AAAAAAAAAAAAAAAAAAAAADAdHwEAAAAAhVRThB0Bmzwld60okSq0jjoQyew%3D4V9NfEMx8VoSlwGfciWd3WQo4fVQD6QOcCBu0NojKmmJeTxAK4"
access_token_secret="szKpFyy4mYflH49v4uQGWJ6zw62bYKF55rj15mfioKHIn"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth,wait_on_rate_limit=True)

account_list = ["@Reapedj"]

if len(account_list) > 0:
  for target in account_list:
    print("Getting data for " + target)
    item = auth_api.get_user(target)
    print("name: " + item.name)
    print("screen_name: " + item.screen_name)
    print("description: " + item.description)
    print("statuses_count: " + str(item.statuses_count))
    print("friends_count: " + str(item.friends_count))
    print("followers_count: " + str(item.followers_count))
    tweets = item.statuses_count
    account_created_date = item.created_at
    delta = datetime.utcnow() - account_created_date
    account_age_days = delta.days
    print("Account age (in days): " + str(account_age_days))
    if account_age_days > 0:
      print("Average tweets per day: " + "%.2f"%(float(tweets)/float(account_age_days)))
    hashtags = []
    mentions = []
    tweet_count = 0
    end_date = datetime.utcnow() - timedelta(days=30)
    for status in Cursor(auth_api.user_timeline, id=target).items():
      tweet_count += 1

      if hasattr(status, "entities"):
        entities = status.entities
        if "hashtags" in entities:
          for ent in entities["hashtags"]:
            if ent is not None:
              if "text" in ent:
                hashtag = ent["text"]
                if hashtag is not None:
                  hashtags.append(hashtag)
        if "user_mentions" in entities:
          for ent in entities["user_mentions"]:
            if ent is not None:
              if "screen_name" in ent:
                name = ent["screen_name"]
                if name is not None:
                  mentions.append(name)
      if status.created_at < end_date:
        break
    print
    print("Most mentioned Twitter users:")
    for item in mentions:
      print(item )

    print
    print("Most used hashtags:")
    for item in hashtags:
      print(item )

    print
    print ("All done. Processed " + str(tweet_count) + " tweets.")
    print

    for x in auth_api.user_timeline(target):
        print(x.text)
        print("---------------------------------")
    '''
    print("*******************************")
    for user in Cursor(auth_api.friends, screen_name=target).items():
        print('friend: ' + user.screen_name)
    print("*******************************")

    for user in Cursor(auth_api.followers, screen_name=target).items():
        print('follower: ' + user.screen_name)
    print("*******************************")

    for status in auth_api.favorites(target):
        print(status.user.screen_name)
        print("--------------------")
        print(status)
        print("--------------------")

    '''
