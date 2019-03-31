from __future__ import division
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
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import random
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
    num = random.randint(0,999)  # random number 0-9
    if num < 140: 
        return True
    return False 


def flipstateR(states):
    num2 = random.randint(0,99)
    if num2 < 96:
        return True
    return False


def flipstateS(states):
    num3 = random.randint(0,99)
    if num3 < 8:
        return True
    return False

# def isrecovered(username):
#     for key, value in users_by_day.items():
#         if key > newdaycount:
#             if username in users_by_day[key]:
#                 return False
#     return True

# reinject = [25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425]
infectedcount_by_iteration = [1]
recoveredcount_by_iteration = [0]
susceptiblecount_by_iteration = [len(infectedstates)]
activelyinfected_by_iteration = [1]
infectedcount = 1
recoveredcount = 0
susceptiblecount = len(infectedstates) - 1
useractivedays = {}
# users_by_day = {}
# user_num_by_day = []
# tweets_by_day = []
for i in range(426):
    activelyinfected = 0 
    # todaysusers = {"removeme"}
    for node, state in infectedstates.items():
        if state == "I": 
            # todaysusers.add(node)
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
                                activelyinfected += 1
                                infectedcount += 1 
                                susceptiblecount -= 1
            if flipstateR(node) is True:
                infectedstates[node] = "R"
                recoveredcount += 1
                infectedcount -= 1

        if state == "R":
            # for keyr, neighborsr in adjacencydict.items():
            #     if keyr == node: 
            if flipstateS(node) is True: 
                infectedstates[node] = "S"
                recoveredcount -= 1
                susceptiblecount += 1



    #                 for neighborz in neighborsr:
    #                     if infectedstates[neighbor] == "S":
    #                         if flipstateI(neighbor) is True: 
    #                             infectedstates[neighbor] = "I"
    #                             infectedcount += 1 
    #                             susceptiblecount -= 1
    #         if flipstateS(node) is True: 
    #             infectedstates[node] = "S"
    #             susceptiblecount += 1
    #             infectedcount -= 1
    #         elif flipstateR(node) is True:
    #             infectedstates[node] = "R"
    #             recoveredcount += 1
    #             infectedcount -= 1
    # for j in range(len(reinject)):
    #     if i == reinject[j]:
    #         reinfectedcount = 0
    #         nums = random.sample(range(0, 199), 10)
    #         for node1, state1 in infectedstates.items():
    #             for n in range(10):
    #                 if node1 == nums[n]:
    #                     if state1 == "S":
    #                         infectedstates[node1] = "I"
    #                         reinfectedcount += 1
    #                         infectedcount += 1
    #                         susceptiblecount -= 1
            # print(reinfectedcount)

    # print(infectedstates)
    # print(infectedcount)
    # print(recoveredcount)
    
    # todaysusers.remove("removeme")
    # users_by_day.update({i:todaysusers})
    # user_num_by_day.append(len(todaysusers))
    activelyinfected_by_iteration.append(activelyinfected)
    infectedcount_by_iteration.append(infectedcount)
    recoveredcount_by_iteration.append(recoveredcount)
    susceptiblecount_by_iteration.append(susceptiblecount)


# # Long duration
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
print("average long duration")
print(np.mean(durations))

# # to find short duration
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


# To calculate and plot number still infected
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

## to find short duration
# consecutives = []
# for user1, activedays1 in useractivedays.items():
#     userconsecutives = []
#     for k, g in groupby(enumerate(activedays1), lambda (i, x): i-x):
#         userconsecutives.append(map(itemgetter(1), g))
#     consecutives.append(userconsecutives)

# shortrecovereddict = {}
# for i in range(1,428):
#     shortrecovereddict.update({i:0})

# for userconsec in consecutives:
#     for j in range(1,428):
#         # for day in userconsec:
#         if j > userconsec[0][0]: 
#             if j not in userconsec:
#                 shortrecovereddict[j] += 1
# print(shortrecovereddict)
# print(len(shortrecovereddict))

# Short graph
# want number of iterations (x) and the number of infecteds (y)
x = []
for n in range(len(infectedcount_by_iteration)):
    x.append(n)
print(len(x))
# plt.plot(x, activelyinfected_by_iteration, label="actively infected")
plt.plot(x, infectedcount_by_iteration, label="infected", color = 'r')
plt.plot(x, recoveredcount_by_iteration, label="recovered", color = 'g')
plt.plot(x, susceptiblecount_by_iteration, label="susceptible", color='b')
# plt.plot(x, stillinfected.values(), label="long infected", color='r')
# plt.plot(x, longrecovered.values(), label="long recovered", color='g')
# plt.plot(x, shortrecovereddict.values(), label = "short recovered")
plt.xlabel("iteration")
plt.ylabel("number of infected nodes")
plt.legend()
plt.show()

# Long graph
plt.plot(x, stillinfected.values(), label="long infected", color='r')
plt.plot(x, longrecovered.values(), label="long recovered", color = 'g')
plt.xlabel("iteration")
plt.ylabel("number of infected nodes")
plt.legend()
plt.show()

# # graph key as x and value as y
# plt.bar(range(len(durationdict)), list(durationdict.values()), align='center')
# plt.xticks(range(len(durationdict)), list(durationdict.keys()))
bins = []
alldurations = list(shortdurationsdict.keys())
for i in range(1, 20,1):
    bins.append(i)

print(bins)
# print(bins)
# print(max(alldurations))

plt.hist(shortdurations, bins)
plt.xticks(range(1, 20,1), bins)
plt.xlabel("number of days infected")
plt.ylabel("number of nodes infected x days")
plt.show()

plt.bar(range(len(durationdict)), list(durationdict.values()), align='center')
np.arange(0, max(durationdict.keys())+1, 1.0)
#plt.xticks(range(len(durationdict)), bins1)
plt.xlabel("number of days infected")
plt.ylabel("number of users infected x days")
plt.show()







