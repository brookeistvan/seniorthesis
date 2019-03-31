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
import math
from itertools import groupby
from operator import itemgetter

# (# groups, # vertices in each group, probability of connecting within group, probability of connecting between groups, seed for random number generator)
G = nx.random_partition_graph([800,200],.1,.0125)
adjacencydict = nx.to_dict_of_dicts(G, nodelist=None, edge_data = None)

# G = nx.planted_partition_graph(2, 100, 0.5, 0.1,seed=42)
# adjacencydict = nx.to_dict_of_dicts(G, nodelist=None, edge_data = None)

# create dict for states and one infected
infectedstates = {}
for n in range(len(adjacencydict)):
	infectedstates.update({n:"S"})

startnode = random.randint(0,len(adjacencydict)) 
infectedstates.update({startnode:"I"})

def flipstateI(node): 
    num = random.randint(0,99)  # random number 0-9
    if num < 14: 
        return True
    return False 


def flipstateR(states):
    num2 = random.randint(0,99)
    if num2 < 9:
        return True
    return False


# def flipstateS(states):
#     num3 = random.randint(0,99)
#     if num3 < 2:
#         return True
#     return False

reinject = [5, 10, 15, 20, 25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425]
infectedcount_by_iteration = [1]
recoveredcount_by_iteration = [0]
susceptiblecount_by_iteration = [len(infectedstates)]
infectedcount = 1
recoveredcount = 0
susceptiblecount = len(infectedstates) - 1
useractivedays = {}
# for i in range(426):
#     for node, state in infectedstates.items():
#         if state == "I": 
#             if node in useractivedays.keys():
#                 useractivedays[node].append(i)
#             else:  
#                 useractivedays.update({node:[i]})
#             for key, neighbors in adjacencydict.items():
#                 if key == node: 
#                     for neighbor in neighbors:
#                         if infectedstates[neighbor] == "S":
#                             if flipstateI(neighbor) is True: 
#                                 infectedstates[neighbor] = "I"
#                                 infectedcount += 1 
#                                 susceptiblecount -= 1
#             if flipstateS(node) is True: 
#                 infectedstates[node] = "S"
#                 susceptiblecount += 1
#                 infectedcount -= 1
#             elif flipstateR(node) is True:
#                 infectedstates[node] = "R"
#                 recoveredcount += 1
#                 infectedcount -= 1
#     for j in range(len(reinject)):
#         if i == reinject[j]:
#             reinfectedcount = 0
#             nums = random.sample(range(0, 199), 10)
#             for node1, state1 in infectedstates.items():
#                 for n in range(10):
#                     if node1 == nums[n]:
#                         if state1 == "S":
#                             infectedstates[node1] = "I"
#                             reinfectedcount += 1
#                             infectedcount += 1
#                             susceptiblecount -= 1


for i in range(426):
    activelyinfected = 0 
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
                            if flipstateI(neighbor) is True: 
                                infectedstates[neighbor] = "I"
                                # activelyinfected += 1
                                infectedcount += 1 
                                susceptiblecount -= 1
            if flipstateR(node) is True:
                infectedstates[node] = "R"
                recoveredcount += 1
                infectedcount -= 1

        # if state == "R":
        #     # for keyr, neighborsr in adjacencydict.items():
        #     #     if keyr == node: 
        #     if flipstateS(node) is True: 
        #         infectedstates[node] = "S"
        #         recoveredcount -= 1
        #         susceptiblecount += 1
    for j in range(len(reinject)):
        if i == reinject[j]:
            reinfectedcount = 0
            nums = random.sample(range(0, 199), 10)
            for node1, state1 in infectedstates.items():
                for n in range(10):
                    if node1 == nums[n]:
                        if state1 == "S":
                            infectedstates[node1] = "I"
                            reinfectedcount += 1
                            infectedcount += 1
                            susceptiblecount -= 1
            # print(reinfectedcount)

    # print(infectedstates)
    # print(infectedcount)
    # print(recoveredcount)
    infectedcount_by_iteration.append(infectedcount)
    recoveredcount_by_iteration.append(recoveredcount)
    susceptiblecount_by_iteration.append(susceptiblecount)

# print(infectedcount_by_iteration)
# print(recoveredcount_by_iteration)

# # export graph so can be visualized
# outputdir = "/Users/brookeistvan/Documents/Thesis/seniorthesis"
# nx.write_gexf(G, outputdir+"SISRgraph.gexf")


# long durations   
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

# short durations 
shortdurations = []
for user, activedays in useractivedays.items():
    for k, g in groupby(enumerate(activedays), lambda (i, x): i-x):
        shortdurations.append(len(map(itemgetter(1), g)))
shortdurationsdict = {}
for i in range(427):
    shortdurationsdict.update({i:0})
for j in shortdurations:
    shortdurationsdict[j] += 1


print(shortdurationsdict)
sumd = 0 
for k,v in shortdurationsdict.items():
    sumd += k*v
print("average short user duration")
print(sumd/(len(shortdurations)))  


stillinfected = {}
for i in range(427):
    stillinfected.update({i:0})
longrecovered = {}
for j in range(427):
    longrecovered.update({j:0})

for user, activedays in useractivedays.items():
    for day in range(activedays[0], (activedays[-1]+1)):
        stillinfected[day] += 1
    for k in range(427): 
        if k > (activedays[-1]+1):
            if infectedstates[user] == "R":
                longrecovered[k] += 1
print(len(stillinfected))
print(longrecovered)
print(len(longrecovered))


# # graph key as x and value as y
# plt.bar(range(len(durationdict)), list(durationdict.values()), align='center')
# plt.xticks(range(len(durationdict)), list(durationdict.keys()))
plt.hist(shortdurations)
plt.xlabel("number of days infected")
plt.ylabel("number of nodes infected x days")
plt.show()

bins = []
alldurations = list(shortdurationsdict.keys())
for i in range(1, 20,1):
    bins.append(i)

plt.hist(shortdurations, bins)
plt.xticks(range(1, 20,1), bins)
plt.xlabel("number of days infected")
plt.ylabel("number of nodes infected x days")
plt.show()



# want number of iterations (x) and the number of infecteds (y)
x = []
for n in range(len(infectedcount_by_iteration)):
    x.append(n)
plt.plot(x, infectedcount_by_iteration, label="infected", color='r')
plt.plot(x, recoveredcount_by_iteration, label="recovered", color = 'g')
plt.plot(x, susceptiblecount_by_iteration, label="susceptible", color ='b')
plt.xlabel("iteration")
plt.ylabel("number of infected nodes")
plt.legend()
plt.show()

plt.plot(x, longrecovered.values(), label="long recovered", color='g')
plt.plot(x, stillinfected.values(), label="long infected", color='r')
plt.xlabel("iteration")
plt.ylabel("number of infected nodes")
plt.legend()
plt.show()