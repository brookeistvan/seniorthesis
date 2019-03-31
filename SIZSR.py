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
G = nx.random_partition_graph([800,200],.1,.0125)
adjacencydict = nx.to_dict_of_dicts(G, nodelist=None, edge_data = None)
communities = list(greedy_modularity_communities(G))
# print(communities)

# # export graph so can be visualized
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
    num = random.randint(0,999)  # random number 0-9
    if num < 400: 
        return True
    return False 

def flipstateZ(node): 
    num = random.randint(0,999)  # random number 0-9
    if num < 5: 
        return True
    return False 

def flipstateR(states):
    num2 = random.randint(0,999)
    if num2 < 90:
        return True
    return False


def flipstateS(states):
    num3 = random.randint(0,999)
    if num3 < 3:
        return True
    return False

reinject = [25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425]
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
                                    infectedcount += 1 
                                    susceptiblecount -= 1
                            elif neighbor in communities[1]:
                                if flipstateZ(neighbor) is True:
                                    infectedstates[neighbor] = "Z"
                                    activelyinfected += 1 
                                    skepticcount += 1
                                    susceptiblecount -= 1

            # if flipstateS(node) is True: 
            #     infectedstates[node] = "S"
            #     susceptiblecount += 1
            #     infectedcount -= 1
            if flipstateR(node) is True:
                infectedstates[node] = "R"
                recoveredcount += 1
                infectedcount -= 1
        elif state == "Z": 
            for keyz, neighborsz in adjacencydict.items():
                if keyz == node:
                    for neighborz in neighborsz:
                        if infectedstates[neighborz] == "S":
                            if neighborz in communities[1]:
                                if flipstateZ(neighborz) is True:
                                    infectedstates[neighborz] = "Z"
                                    activelyinfected += 1
                                    skepticcount += 1
                                    susceptiblecount -= 1
                            elif neighborz in communities[0]:
                                if flipstateI(neighborz) is True:
                                    infectedstates[neighborz] = "I"
                                    activelyinfected += 1
                                    infectedcount += 1 
                                    susceptiblecount -= 1
            # if flipstateS(node) is True: 
            #     infectedstates[node] = "S"
            #     susceptiblecount += 1
            #     skepticcount -= 1
            if flipstateR(node) is True:
                infectedstates[node] = "R"
                recoveredcount += 1
                skepticcount -= 1
        # print(skepticcount)

   # # reinject infected nodes exogenouslyh into the network 
   #  for j in range(len(reinject)):
   #      if i == reinject[j]:
   #          reinfectedcount = 0
   #          nums = random.sample(range(0, 199), 10)
   #          for node1, state1 in infectedstates.items():
   #              for n in range(10):
   #                  if node1 == nums[n]:
   #                      if state1 == "S":
   #                          infectedstates[node1] = "I"
   #                          reinfectedcount += 1
   #                          infectedcount += 1
   #                          susceptiblecount -= 1
   #          print(reinfectedcount)

    # print(infectedstates)
    # print(infectedcount)
    # print(recoveredcount)
    activelyinfected_by_iteration.append(activelyinfected)
    infectedcount_by_iteration.append(infectedcount)
    skepticcount_by_iteration.append(skepticcount)
    recoveredcount_by_iteration.append(recoveredcount)
    susceptiblecount_by_iteration.append(susceptiblecount)

# print(infectedcount_by_iteration)
# print(recoveredcount_by_iteration)

# # export graph so can be visualized
# outputdir = "/Users/brookeistvan/Documents/Thesis/seniorthesis"
# nx.write_gexf(G, outputdir+"SISRgraph.gexf")

# want number of iterations (x) and the number of infecteds (y)
x = []
for n in range(len(infectedcount_by_iteration)):
    x.append(n)
#plt.plot(x, activelyinfected_by_iteration, label="activelyinfected")
plt.plot(x, infectedcount_by_iteration, label="infected group1", color="r")
plt.plot(x, skepticcount_by_iteration, label="infected group2", color="k")
plt.plot(x, recoveredcount_by_iteration, label="recovered", color="b")
plt.plot(x, susceptiblecount_by_iteration, label="susceptible", color="g")
plt.xlabel("iteration")
plt.ylabel("number of infected nodes")
plt.legend()
plt.show()