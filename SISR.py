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

# (# groups, # vertices in each group, probability of connecting within group, probability of connecting between groups, seed for random number generator)
G = nx.random_partition_graph([700,300],.1,.0125)
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
    if num < 12:
        return True
    return False 


def flipstateR(states):
    num2 = random.randint(0,99)
    if num2 < 10:
        return True
    return False


def flipstateS(states):
    num3 = random.randint(0,99)
    if num3 < 50:
        return True
    return False

infectedcount_by_iteration = [1]
recoveredcount_by_iteration = [0]
susceptiblecount_by_iteration = [len(infectedstates)]
infectedcount = 1
recoveredcount = 0
susceptiblecount = len(infectedstates) - 1
useractivedays = {}
for i in range(426):
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
                                infectedcount += 1 
                                susceptiblecount -= 1
            if flipstateS(node) is True: 
                infectedstates[node] = "S"
                susceptiblecount += 1
                infectedcount -= 1
            elif flipstateR(node) is True:
                infectedstates[node] = "R"
                recoveredcount += 1
                infectedcount -= 1


    # activelyinfected_by_iteration.append(activelyinfected)
    infectedcount_by_iteration.append(infectedcount)
    recoveredcount_by_iteration.append(recoveredcount)
    susceptiblecount_by_iteration.append(susceptiblecount)


# Long duration
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
sumd = 0 
for k,v in durationdict.items():
    sumd += k*v
print(sumd/(1000))    


# To calculate and plot number still infected
stillinfected = {}
for i in range(427):
    stillinfected.update({i:0})
for user, activedays in useractivedays.items():
    for day in range(activedays[0], (activedays[-1]+1)):
        stillinfected[day] += 1
print(len(stillinfected))

# Short graph
# want number of iterations (x) and the number of infecteds (y)
x = []
for n in range(len(infectedcount_by_iteration)):
    x.append(n)
print(len(x))
# plt.plot(x, activelyinfected_by_iteration, label="actively infected")
# plt.plot(x, infectedcount_by_iteration, label="infected")
plt.plot(x, recoveredcount_by_iteration, label="recovered", color='g')
plt.plot(x, susceptiblecount_by_iteration, label="susceptible", color='b')
plt.plot(x, stillinfected.values(), label="infected", color='r')
plt.xlabel("iteration")
plt.ylabel("number of infected nodes")
plt.legend()
plt.show()

# Long graph
plt.plot(x, stillinfected.values(), label="still infected")
plt.xlabel("iteration")
plt.ylabel("number of infected nodes")
plt.legend()
plt.show()
# # graph key as x and value as y
# plt.bar(range(len(durationdict)), list(durationdict.values()), align='center')
# plt.xticks(range(len(durationdict)), list(durationdict.keys()))
bins = []
alldurations = list(durationdict.keys())
for i in range(0,(max(alldurations)+50),10):
    bins.append(i)

print(bins)
# print(bins)
# print(max(alldurations))

plt.hist(durations, bins)
plt.xticks(range(0,(max(alldurations)+50),10), bins)
plt.xlabel("number of days infected")
plt.ylabel("number of nodes infected x days")
plt.show()



