from datetime import datetime, date, time, timedelta
import time as t
from collections import Counter
import sys
import re
import json
import networkx as nx
from networkx.readwrite import json_graph

networkCount={}
completeMap={}
fG=nx.Graph()
mG=nx.DiGraph()
hG=nx.Graph()
rG = nx.DiGraph()  #graph made for retweets of a particular user
favG = nx.DiGraph()  # represents the graph which is made for favourites

try:
    with open('followers.json', 'r') as openfile:
        json_object = json.load(openfile)
    fG=json_graph.node_link_graph(json_object)
except:
    print("")

try:
    with open('mentions.json', 'r') as openfile:
        json_object = json.load(openfile)
    mG=json_graph.node_link_graph(json_object)
except:
    print("")

try:
    with open('hashtags.json', 'r') as openfile:
        json_object = json.load(openfile)
    hG=json_graph.node_link_graph(json_object)
except:
    print("")

try:
    with open('fav.json', 'r') as openfile:
        json_object = json.load(openfile)
    favG=json_graph.node_link_graph(json_object)
except:
    print("")

try:
    with open('retweet.json', 'r') as openfile:
        json_object = json.load(openfile)
    rG=json_graph.node_link_graph(json_object)
except:
    print("")
try:
    with open('networkCount.json', 'r') as openfile:
        networkCount = json.load(openfile)
except:
    print("")
"""
#TEST CASE
networkCount["a"]=[10,30]
networkCount["b"]=[100,30]
networkCount["c"]=[1,30]
networkCount["d"]=[20,30]
networkCount["e"]=[16,30]

fG.add_edge("a","b")
fG.add_edge("a","c")
fG.add_edge("c","d")
fG.add_edge("d","e")
fG.add_edge("e","b")
fG.add_edge("e","a")


hG.add_edge("@a","af",weight=1)
hG.add_edge("@b","af",weight=-1)
hG.add_edge("@c","af",weight=0)
hG.add_edge("@d","af",weight=-1)
hG.add_edge("@e","af",weight=1)
"""

for x in list(hG.nodes):
    if "@" not in x:
        xMap={}
        users=nx.neighbors(hG, x)
        for user1 in users:
            userList=[]
            count1=networkCount[user1.replace("@","")]
            sentiment=hG.get_edge_data(x,user1)['weight']
            for user2 in users:
                count2=networkCount[user2.replace("@","")]
                if(user1!=user2):
                    if( count1[1]/count1[0] > count2[1]/count2[0] ):
                        if hG.get_edge_data(x,user2)['weight']==sentiment:
                            if (fG.has_edge(user1.replace("@",""),user2.replace("@",""))):
                                userList.append(user2.replace("@",""))
            xMap[user1.replace("@","")]=userList

        completeMap[x]=xMap
#TODO work on completeMap
print(completeMap)
