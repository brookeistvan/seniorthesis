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
import numpy as np
from networkx.algorithms.community import greedy_modularity_communities


# # create dict for states and one infected
# infectedstates = {}
# for n in range(len(adjacencydict)):
#     infectedstates.update({n:"S"})

# startnode = random.randint(0,len(adjacencydict)) 
# infectedstates.update({startnode:"I"})

def flipstateI(node): 
    num = random.randint(0,99)  # random number 0-9
    if num < 14: 
        return True
    return False 

def flipstateZ(node): 
    num = random.randint(0,99)  # random number 0-9
    if num < 14: 
        return True
    return False 

def flipstateR(states):
    num2 = random.randint(0,99)
    if num2 < 9:
        return True
    return False

betweenentertotal = []
for p in np.arange(.005, .3, .005):
    betweenenter = 0 
# (# groups, # vertices in each group, probability of connecting within group, probability of connecting between groups, seed for random number generator)
    G = nx.random_partition_graph([800,200],.1, p)
    adjacencydict = nx.to_dict_of_dicts(G, nodelist=None, edge_data = None)
    communities = list(greedy_modularity_communities(G))

    infectedstates = {}
    for n in range(len(adjacencydict)):
        infectedstates.update({n:"S"})
    infectedstates.update({1:"I"})

    useractivedays = {}
    recoveredcount_by_iteration = [0]
    susceptiblecount_by_iteration = [len(infectedstates)]
    activelyinfected_by_iteration = [1]
    recoveredcount = 0
    susceptiblecount = len(infectedstates) - 1
    for i in range(426): #426
        activelyinfected = 0 
        for node, state in infectedstates.items():
            if state == "I": 
                for key, neighbors in adjacencydict.items():
                    if key == node: 
                        for neighbor in neighbors:
                            if infectedstates[neighbor] == "S":
                                if neighbor in communities[0]:
                                    if flipstateI(neighbor) is True: 
                                        infectedstates[neighbor] = "I"
                                        activelyinfected += 1
                                        # infectedcount += 1 
                                        # susceptiblecount -= 1
                                elif neighbor in communities[1]:
                                    if flipstateZ(neighbor) is True:
                                        infectedstates[neighbor] = "Z"
                                        activelyinfected += 1 
                                        # skepticcount += 1
                                        # susceptiblecount -= 1
                                        betweenenter += 1

                # if flipstateS(node) is True: 
                #     infectedstates[node] = "S"
                #     susceptiblecount += 1
                #     infectedcount -= 1
                if flipstateR(node) is True:
                    infectedstates[node] = "R"
                    recoveredcount += 1
                    # infectedcount -= 1
            elif state == "Z": 
                for keyz, neighborsz in adjacencydict.items():
                    if keyz == node:
                        for neighborz in neighborsz:
                            if infectedstates[neighborz] == "S":
                                if neighborz in communities[1]:
                                    if flipstateZ(neighborz) is True:
                                        infectedstates[neighborz] = "Z"
                                        activelyinfected += 1
                                        # skepticcount += 1
                                        # susceptiblecount -= 1
                                elif neighborz in communities[0]:
                                    if flipstateI(neighborz) is True:
                                        infectedstates[neighborz] = "I"
                                        activelyinfected += 1
                                        # infectedcount += 1 
                                        # susceptiblecount -= 1
                                        betweenenter += 1
                # if flipstateS(node) is True: 
                #     infectedstates[node] = "S"
                #     susceptiblecount += 1
                #     skepticcount -= 1
                if flipstateR(node) is True:
                    infectedstates[node] = "R"
                    recoveredcount += 1
                    # skepticcount -= 1

        # activelyinfected_by_iteration.append(activelyinfected)
        # infectedcount_by_iteration.append(infectedcount)
        # skepticcount_by_iteration.append(skepticcount)
        # recoveredcount_by_iteration.append(recoveredcount)
        # susceptiblecount_by_iteration.append(susceptiblecount)

    betweenentertotal.append(betweenenter)

print(betweenentertotal)
print(len(betweenentertotal))

x = []
for p in np.arange(.005, .3, .005):
    x.append(p)

# x = [.005, .01, .015, .02, .025, .03, .035, .04, .045, .05, .055, .06, .065, .07, .075, .08, .085, .09, .095, .1, .105, .11, .115, .12, .125, .13, .135, .14, .145, .15, .155, .16, .165, .17, .175, .18, .185, .19, .195]
print(len(x))
plt.plot(x, betweenentertotal)
plt.xlabel('probability of connecting between groups')
plt.ylabel(" number of nodes enetering from between group connection")
plt.show()
