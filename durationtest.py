import os
import json
from pprint import pprint
import networkx as nx 
import matplotlib.pyplot as plt
import codecs
import time
import datetime
import random
import time
import sys
import io
from networkx.algorithms.community import greedy_modularity_communities

# (# groups, # vertices in each group, probability of connecting within group, probability of connecting between groups, seed for random number generator)
G = nx.random_partition_graph([700,300],.1,.0125)
adjacencydict = nx.to_dict_of_dicts(G, nodelist=None, edge_data = None)
communities = list(greedy_modularity_communities(G))
# print(communities)

# export graph so can be visualized
# outputdir = "/Users/brookeistvan/Documents/Thesis/seniorthesis"
# nx.write_gexf(G, outputdir+"SIZSRgraph.gexf")

infectedstates = {}
for n in range(len(adjacencydict)):
    infectedstates.update({n:"S"})

infectedcount_by_iteration = []
skepticcount_by_iteration = []
startnode = random.randint(0,len(adjacencydict))
if startnode in communities[0]:
    infectedstates.update({startnode:"I"})
    infectedcount = 1
    skepticcount = 0 
    infectedcount_by_iteration.append(1)
    skepticcount_by_iteration.append(0)
elif startnode in communities[1]:
    infectedstates.update({startnode:"Z"})
    skepticcount = 1
    infectedcount = 0
    skepticcount_by_iteration.append(1)
    infectedcount_by_iteration.append(0)

def flipstateI(node): 
    num = random.randint(0,99)  # random number 0-9
    if num < 10: 
        return True
    return False 

def flipstateZ(node): 
    num = random.randint(0,99)  # random number 0-9
    if num < 20: 
        return True
    return False 

def flipstateR(states):
    num2 = random.randint(0,99)
    if num2 < 5:
        return True
    return False


def flipstateS(states):
    num3 = random.randint(0,99)
    if num3 < 80:
        return True
    return False

reinject = [25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425]
recoveredcount_by_iteration = [0]
susceptiblecount_by_iteration = [len(infectedstates)]
recoveredcount = 0
susceptiblecount = len(infectedstates) - 1
useractivedays = {}
for i in range(426): #426
    for node, state in infectedstates.items():
        if state == "I": 
            if node in useractivedays.keys():
                useractivedays[node].append(i)
            else:  
                useractivedays.update({node:[i]})
            for key, neighbors in adjacencydict.items():
                if key == node: 
                    for neighbor in neighbors:
                        if infectedstates[neighbor] == "S":
                            if neighbor in communities[0]:
                                if flipstateI(neighbor) is True: 
                                    infectedstates[neighbor] = "I"
                                    infectedcount += 1 
                                    susceptiblecount -= 1
                            elif neighbor in communities[1]:
                                if flipstateZ(neighbor) is True:
                                    infectedstates[neighbor] = "Z"
                                    skepticcount += 1
                                    susceptiblecount -= 1

            if flipstateS(node) is True: 
                infectedstates[node] = "S"
                susceptiblecount += 1
                infectedcount -= 1
            elif flipstateR(node) is True:
                infectedstates[node] = "R"
                recoveredcount += 1
                infectedcount -= 1
        elif state == "Z": 
            if node in useractivedays.keys():
                useractivedays[node].append(i)
            else:  
                useractivedays.update({node:[i]})
            for keyz, neighborsz in adjacencydict.items():
                if keyz == node:
                    for neighborz in neighborsz:
                        if infectedstates[neighborz] == "S":
                            if neighborz in communities[1]:
                                if flipstateZ(neighborz) is True:
                                    infectedstates[neighborz] = "Z"
                                    skepticcount += 1
                                    susceptiblecount -= 1
                            elif neighborz in communities[0]:
                                if flipstateI(neighborz) is True:
                                    infectedstates[neighborz] = "I"
                                    infectedcount += 1 
                                    susceptiblecount -= 1
            if flipstateS(node) is True: 
                infectedstates[node] = "S"
                susceptiblecount += 1
                skepticcount -= 1
            elif flipstateR(node) is True:
                infectedstates[node] = "R"
                recoveredcount += 1
                skepticcount -= 1

    infectedcount_by_iteration.append(infectedcount)
    skepticcount_by_iteration.append(skepticcount)
    recoveredcount_by_iteration.append(recoveredcount)
    susceptiblecount_by_iteration.append(susceptiblecount)


# print(useractivedays)
    
durations = []
durationdict = {}
for user, activedays in useractivedays.items():
    duration = 0
    duration += (activedays[-1] - activedays[0])
    durations.append(duration)
    if duration in durationdict:
        durationdict[duration] += 1
    else:
        durationdict.update({duration:1})

print(durationdict)
# # Remove people who only appear on one day
# onedaypeople = 0
# greatthanhundredpeople = 0
# for k,v in durationdict.items():
#     if k == 0:
#         onedaypeople = v
#         del durationdict[k]

#     if k > 50:
#         greatthanhundredpeople += v 
#         del durationdict[k]


# print(durationdict)
# print(onedaypeople)
# print(greatthanhundredpeople)
# print(np.mean(durations))

# # graph key as x and value as y
# plt.bar(range(len(durationdict)), list(durationdict.values()), align='center')
# plt.xticks(range(len(durationdict)), list(durationdict.keys()))
# plt.xlabel("number of days infected")
# plt.ylabel("number of nodes infected x days")
# plt.show()

alldurations = list(durationdict.keys())
bins = list(range(max(alldurations)))
print(bins)
print(max(alldurations))

plt.hist(durations)
plt.xlabel("number of days infected")
plt.ylabel("number of nodes infected x days")
plt.show()

