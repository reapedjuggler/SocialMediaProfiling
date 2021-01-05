from datetime import datetime, date, time, timedelta
import time as t
import math
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

values = [10, 10, 10]

connections = {}

#bondTotal = {(Reaped, xyz): 26.5, ......., (xyz: Reaped): 34.5}

# connections = {(user , friend): [10, 10, 0,]}



def dfsUtil(graph1, node, visited, ref):
    
    if node not in visited:
        visited.append(node)
        for k in graph1[node]:
            print(k)
            if (ref, k) not in connections:
                connections[(ref, k)].append(values[0])                 # Can be changed after wards now for sample
            dfsUtil(graph1,k, ref, visited)


def dfs(graph1,node):
    visited = []
    ref = node
    dfsUtil(graph1, node, visited,ref)
    
def bondStrength():
    
    temp=[]
    # Ratio = follower / following but for now let Ratio be == 1

    Ratio = 0.5

    for temp in connections:
        total = 0
        for j in connections[temp]:                                   # Connection List which values it contains
            total = total + j

        total = math.exp(total * Ratio)
        temp.append(total)                               # Using Exp so that value is always non negative


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

dfs(favG,"ReapedJ")
dfs(mG,"@ReapedJ")
dfs(rG,"@ReapedJ")

bondTotal=[]
bondTotal=bondStrength()
print(bondTotal)
