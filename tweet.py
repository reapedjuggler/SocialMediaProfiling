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

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


account_list=[]
account_list_temp=[]
alreadyProcessed = []
networkCount={}
#fG=nx.DiGraph()
fG=nx.Graph()
mG=nx.DiGraph()
#hG=nx.DiGraph()
hG=nx.DiGraph()
rG = nx.DiGraph()  #graph made for retweets of a particular user
favG = nx.DiGraph()  # represents the graph which is made for favourites

with open('accountList.txt', 'r') as filehandle:
    for line in filehandle:
        user = line[:-1]
        account_list_temp.append(user)

try:
    with open('alreadyProcessed.txt', 'r') as filehandle:
        for line in filehandle:
            user = line[:-1]
            alreadyProcessed.append(user)
    with open('followers.json', 'r') as openfile:
        json_object = json.load(openfile)
    fG=json_graph.node_link_graph(json_object)

    with open('mentions.json', 'r') as openfile:
        json_object = json.load(openfile)
    mG=json_graph.node_link_graph(json_object)

    with open('hashtags.json', 'r') as openfile:
        json_object = json.load(openfile)
    hG=json_graph.node_link_graph(json_object)

    with open('fav.json', 'r') as openfile:
        json_object = json.load(openfile)
    favG=json_graph.node_link_graph(json_object)

    with open('retweet.json', 'r') as openfile:
        json_object = json.load(openfile)
    rG=json_graph.node_link_graph(json_object)

    with open('networkCount.json', 'r') as openfile:
        networkCount = json.load(openfile)




except:
    print("Run")

account_list = [x for x in account_list_temp if x not in alreadyProcessed]



def makeIt(target , following ,mentions, mentionSentiment, followers , hashtags ,hashtagSentiment, fav , retweet):

    for hashtag,sentiment in zip(hashtags,hashtagSentiment):
        hG.add_edge(hashtag,target,weight=sentiment)

    target=target.replace("@","")
    for user in following:
        fG.add_edge(target,user)
        if user not in account_list:
            account_list.append(user)
    #adding same edge again doesn't effect the graph
    for user in followers:
        fG.add_edge(target,user)
        if user not in account_list:
            account_list.append(user)

    for user,sentiment in zip(mentions,mentionSentiment):
        mG.add_edge(target,user,weight=sentiment)
        if user not in account_list:
            account_list.append(user)

    for user in fav:
        favG.add_edge(user , target)
        if user not in account_list:
            account_list.append(user)

    #this one is a dictionary retweet

    # {"1" : ["acdfac" , "aczzac" , "acbs" , "acadsc"] , .........}

    for user in retweet:
        rG.add_edge(user , target)
        if user not in account_list:
            account_list.append(user)



    temp_list=list(dict.fromkeys(account_list))
    temp_list.remove(target)
    alreadyProcessed.append(target)

    data = json_graph.node_link_data(fG)
    with open("followers.json", "w") as outfile:
        json.dump(data, outfile)
    data = json_graph.node_link_data(mG)
    with open("mentions.json", "w") as outfile:
        json.dump(data, outfile)
    data = json_graph.node_link_data(hG)
    with open("hashtags.json", "w") as outfile:
        json.dump(data, outfile)
    data = json_graph.node_link_data(favG)
    with open("fav.json", "w") as outfile:
        json.dump(data, outfile)
    data = json_graph.node_link_data(rG)
    with open("retweet.json", "w") as outfile:
        json.dump(data, outfile)
    with open('networkCount.json', 'w') as outfile:
        json.dump(networkCount, outfile)

    with open('accountList.txt', 'w') as filehandle:
        for listitem in temp_list:
            filehandle.write('%s\n' % listitem)

    with open('alreadyProcessed.txt', 'w') as filehandle:
        for listitem in alreadyProcessed:
            filehandle.write('%s\n' % listitem)



def clean_tweet(tweet):

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment( tweet):

    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

if len(account_list) > 0:
    for target in account_list:

        target="@"+target

        hashtags = []
        hashtagSentiment = []
        mentions = []
        mentionSentiment = []
        following = []
        myfollower = []
        retweet = []
        fav = []
        tweet_count = 0
        sentiment = []

        print("Getting data for " + target)
        item = auth_api.get_user(target)
        # print("name: " + item.name)
        # print("screen_name: " + item.screen_name)
        # print("description: " + item.description)
        # print("statuses_count: " + str(item.statuses_count))
        fcount=[]
        fcount.append(item.friends_count)
        fcount.append(item.followers_count)
        networkCount[target]=fcount
        #print("followers_count: " + str(item.followers_count))
        #print("followers_count: " + str(item.friends_count))

        tweets = item.statuses_count
        account_created_date = item.created_at
        delta = datetime.utcnow() - account_created_date
        account_age_days = delta.days
        print("Account age (in days): " + str(account_age_days))

        if account_age_days > 0:
          print("Average tweets per day: " + "%.2f"%(float(tweets)/float(account_age_days)))

        end_date = datetime.utcnow() - timedelta(days=30)
        cur = Cursor(auth_api.user_timeline, id=target).items()

        while True:
            try:

                status =cur.next()
                #print(status)
                tweet_count += 1
                if hasattr(status,"text"):
                    print(status.text)
                    sentiment=get_tweet_sentiment(status.text)

                if hasattr(status,"id"):
                    print(status.id)
                    retweets_list = auth_api.retweets(status.id)

                    # {id : vector<string>}

                    for x in retweets_list:
                        retweet.append(x.user.screen_name)
                        # print(retweet.user.screen_name)

                if hasattr(status, "entities"):
                    entities = status.entities
                    if "hashtags" in entities:
                        for ent in entities["hashtags"]:
                            if ent is not None:
                                if "text" in ent:
                                    hashtag = ent["text"]
                                    if hashtag is not None:
                                        print(hashtag)
                                        hashtags.append(hashtag)
                                        hashtagSentiment.append(sentiment)
                    if "user_mentions" in entities:
                        for ent in entities["user_mentions"]:
                            if ent is not None:
                                if "screen_name" in ent:
                                    name = ent["screen_name"]
                                    if name is not None:
                                        print(name)
                                        mentions.append(name)
                                        mentionSentiment.append(sentiment)
                #if status.created_at < end_date:
                    #break
            except tweepy.TweepError:
                print("wait")
                t.sleep(61)
		if(tweet_count>500):
			break
                else:
			continue
            except StopIteration:
                break
            except Exception as e:
                print(e)


        val=0
        cur=Cursor(auth_api.friends, screen_name=target).items()
        while True:
            try:
                user=cur.next()
                val+=1
                print('friend: ' + user.screen_name)
                following.append(user.screen_name)
            except tweepy.TweepError:
                print("wait")
                t.sleep(61)
                if(val>300):
                    break
                continue
            except StopIteration:
                break
            except Exception as e:
                print(e)
        val=0
        cur= Cursor(auth_api.followers, screen_name=target).items()
        while True:
            try:
                user=cur.next()
                val+=1
                # print('follower: ' + user.screen_name)
                myfollower.append(user.screen_name)
            except tweepy.TweepError:
                print("wait")
                t.sleep(61)
                if(val>300):
                    break
                continue
            except StopIteration:
                break
            except Exception as e:
                print(e)


        cur1 = Cursor(auth_api.favorites, id='@ReapedJ').items(20)

        while 1:
            try:
                favorite = cur1.next()
                fav.append(favorite.user.screen_name)
                 # print(favorite.user.screen_name)
            except tweepy.TweepError:
                print("wait")
                t.sleep(61)
                continue
            except StopIteration:
                break
            except Exception as e:
                print(e)

        makeIt(target ,following , mentions,mentionSentiment , myfollower , hashtags,hashtagSentiment , fav , retweet)
        print("__________________________________________")

        # print
        # print("Most mentioned Twitter users:")
        # for item in mentions:
        #   print(item)

        # print
        # print("Most used hashtags:")
        # for item in hashtags:
        #   print(item )

        # print
        # print ("All done. Processed " + str(tweet_count) + " tweets.")
        # print

        # for x in auth_api.user_timeline(target):
        #     print(x.text)
        #     print("---------------------------------")

        # print("*******************************")

        # print("*******************************")


        # print("*******************************")
        # for status in auth_api.favorites(target):
        #     print(status.user.screen_name)
        #     print("--------------------")
        #     print(status)
        #     print("--------------------")
        #


        # Making the Graph





            # this will be an infinite loop so maintaining a count signifying when to stop
            # for i in range(count):
            #     for x in myfollower
