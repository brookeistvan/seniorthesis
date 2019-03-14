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

# create dict for states and one infected
infectedstates = {}
for n in range(len(adjacencydict)):
    infectedstates.update({n:"S"})

startnode = random.randint(0,len(adjacencydict)) 
infectedstates.update({startnode:"I"})

def flipstateI(node): 
    num = random.randint(0,99)  # random number 0-9
    if num < 6: 
        return True
    return False 


def flipstateR(states):
    num2 = random.randint(0,99)
    if num2 < 6:
        return True
    return False

infectedcount_by_iteration = [1]
recoveredcount_by_iteration = [0]
susceptiblecount_by_iteration = [len(infectedstates)]
activelyinfected_by_iteration = [1]
infectedcount = 1
recoveredcount = 0
susceptiblecount = len(infectedstates) - 1
useractivedays ={}
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
                                activelyinfected += 1
                                infectedcount += 1 
                                susceptiblecount -= 1
            if flipstateR(node) is True:
                infectedstates[node] = "R"
                recoveredcount += 1
                infectedcount -= 1
    # print(infectedstates)
    # print(infectedcount)
    # print(recoveredcount)
    if infectedcount < 100:
        print(i)

    activelyinfected_by_iteration.append(activelyinfected)
    infectedcount_by_iteration.append(infectedcount)
    recoveredcount_by_iteration.append(recoveredcount)
    susceptiblecount_by_iteration.append(susceptiblecount)

# print(infectedcount_by_iteration)
# print(recoveredcount_by_iteration)

# # export graph so can be visualized
# outputdir = "/Users/brookeistvan/Documents/Thesis/seniorthesis"
# nx.write_gexf(G, outputdir+"SIRgraph.gexf")

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


print(activelyinfected_by_iteration)
# want number of iterations (x) and the number of infecteds (y)
x = []
for n in range(len(infectedcount_by_iteration)):
    x.append(n)
plt.plot(x, activelyinfected_by_iteration, label="infected that day")
plt.show()
# plt.plot(x, infectedcount_by_iteration, label="infected")
# plt.plot(x, recoveredcount_by_iteration, label="recovered")
# plt.plot(x, susceptiblecount_by_iteration, label="susceptible")
# plt.xlabel("iteration")
# plt.ylabel("number of infected nodes")
# plt.legend()
# plt.show()


# alldurations = list(durationdict.keys())
# bins = list(range(max(alldurations)))
# # print(bins)
# # print(max(alldurations))

# plt.hist(durations)
# plt.xlabel("number of days infected")
# plt.ylabel("number of nodes infected x days")
# plt.show()
