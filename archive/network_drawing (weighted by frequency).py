'''
Social network of music reviews

If two users share a release, an edge is drawn

For now, only reviews with full score(100) are selected.

Edge weight is the number of reviews two users share. (Can be seen from graph, not really significant)


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

nodes = set()

for i in range(len(df)):
    #if df['Score'][i] > df['Score'].quantile(.9):#positive review is defined as 90th percentile or above
    if df['Score'][i] == 100:#only consider positive review as full score of 100
        if df['Release'][i] not in mp:
            mp[df['Release'][i]] = []
        mp[df['Release'][i]].append((df['User'][i],float(df['Score'][i])))


G = nx.Graph()

edges = {}
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
            #G.add_edge(mp[item][i][0],mp[item][j][0], weight = 1)#weight is the average of two ratings
            if (mp[item][i][0],mp[item][j][0]) in edges:
                edges[(mp[item][i][0],mp[item][j][0])] += 1
            elif (mp[item][j][0],mp[item][i][0]) in edges:
                edges[(mp[item][j][0],mp[item][i][0])] += 1
            else:
                edges[(mp[item][j][0],mp[item][i][0])] = 1
    maxGroupSize = max(maxGroupSize, len(mp[item]))

for edge in edges:
    G.add_edge(edge[0], edge[1], weight = edges[edge])

print("Maximum number of users per release =",maxGroupSize)
#print(G.edges())

weights = [G[u][v]['weight'] for u,v in G.edges()]

print("Number of edges =",len(weights))

pos = nx.spring_layout(G)


nx.draw(G, node_size = 10, width = weights)

endTime = time.time()

print("Program successfully executed in",endTime-startTime,"seconds.")

plt.show()


#Splitting the graph into connected subgraphs

graphs = list(nx.connected_components(G))

for subgraph in graphs:
    if len(subgraph) < 3:#only consider subgraphs with size > 3
        continue
    graph = G.subgraph(subgraph)
    weights1 = [graph[u][v]['weight'] for u,v in graph.edges()]
    nx.draw(graph, node_size = 10, width = weights1)
    plt.show()



