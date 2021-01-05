from datetime import datetime, date, time, timedelta
import time as t
from collections import Counter
import sys
import re
import json
import networkx as nx
from networkx.readwrite import json_graph

networkCount={}
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
