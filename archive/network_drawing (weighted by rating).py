'''
Social network of music reviews

If two users share a release, an edge is drawn

Edge weight for each edge is the average of the two reviews (applicable only if we choose reviews with score <100)

Double edges are possible (actually present the graph), but their significance is neglected for now



'''

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import math
import time


startTime = time.time()
df = pd.read_csv('all_reviews.csv')

print(df.columns)

mp = {}

posScore = df['Score'].quantile(.9)

nodes = set()

for i in range(len(df)):
    #if df['Score'][i] > posScore:#positive review is defined as 90th percentile or above
    if df['Score'][i] == 100:#only consider positive review as full score of 100
        if df['Release'][i] not in mp:
            mp[df['Release'][i]] = []
        mp[df['Release'][i]].append((df['User'][i],float(df['Score'][i])))
        #nodes.add(df['User'][i])

#print(mp)


G = nx.Graph()
#nodes = list(nodes)
#G.add_nodes_from(nodes)

maxGroupSize = 0
for item in mp:
    for i in range(len(mp[item])):#every pair of reviews of the same release
        for j in range(i+1,len(mp[item])):
            #add nodes which are connected to other nodes (i.e. eliminating lone nodes)
            if mp[item][i][0] not in nodes:
                nodes.add(mp[item][i][0])
                G.add_node(mp[item][i][0])
            if mp[item][j][0] not in nodes:
                nodes.add(mp[item][j][0])
                G.add_node(mp[item][j][0])
            G.add_edge(mp[item][i][0],mp[item][j][0], weight = float((mp[item][i][1] + mp[item][j][1])/2))#weight is the average of two ratings
    maxGroupSize = max(maxGroupSize, len(mp[item]))


print("Maximum number of users per release =",maxGroupSize)
#print(G.edges())

weights = [(G[u][v]['weight']-posScore)/5 for u,v in G.edges()]#normalised

print("Number of edges =",len(G.edges()))

pos = nx.spring_layout(G)

#nx.draw(G, node_size = 10, width = weights, pos = nx.spring_layout(G))

nx.draw(G, node_size = 10)
#nx.draw_circular(G, node_size = 10, width = weights)

endTime = time.time()

print("Program successfully executed in",endTime-startTime,"seconds.")

plt.show()
