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

# (# groups, # vertices in each group, probability of connecting within group, probability of connecting between groups, seed for random number generator)
G = nx.random_partition_graph([700,300],.1,.0125)
adjacencydict = nx.to_dict_of_dicts(G, nodelist=None, edge_data = None)

# # create dict for states and one infected
# infectedstates = {}
# for n in range(len(adjacencydict)):
#     infectedstates.update({n:"S"})

# startnode = random.randint(0,len(adjacencydict)) 
# infectedstates.update({startnode:"I"})

def flipstateI(node): 
    num = random.randint(0,99)  # random number 0-9
    if num < Beta: 
        return True
    return False 


def flipstateR(states):
    num2 = random.randint(0,99)
    if num2 < Gamma:
        return True
    return False

Gammabetaavgdurations = []
for Gamma in range(2,32,2):
    print(Gamma)
    betaavgdurations = []
    for Beta in range(2,32,2):
        print(Beta)

        # create dict for states and one infected
        infectedstates = {}
        for n in range(len(adjacencydict)):
            infectedstates.update({n:"S"})

        startnode = random.randint(0,len(adjacencydict)) 
        infectedstates.update({startnode:"I"})

        useractivedays = {}
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
                    if flipstateR(node) is True:
                        infectedstates[node] = "R"
            # put code for time to reach a certain level of infection here
            # if infectedcount < 100:
            #     print(i)


        durations = []
        durationdict = {}
        for user, activedays in useractivedays.items():
            duration = 0
            duration += (activedays[-1] - activedays[0])
            durations.append(duration)

        avgduration = np.mean(durations)
        betaavgdurations.append(avgduration)
    Gammabetaavgdurations.append(np.round(betaavgdurations,1))

    print(Gammabetaavgdurations)

Gamma = [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]
Beta = [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]

fig, ax = plt.subplots()
im = ax.imshow(Gammabetaavgdurations)

# We want to show all ticks...
ax.set_xticks(np.arange(len(Beta)))
ax.set_yticks(np.arange(len(Gamma)))
# ... and label them with the respective list entries
ax.set_xticklabels(Beta)
ax.set_yticklabels(Gamma)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(Gamma)):
    for j in range(len(Beta)):
        text = ax.text(j, i, Gammabetaavgdurations[i][j],
                       ha="center", va="center", color="w")

# ax.set_title("Harvest of local farmers (in tons/year)")
fig.tight_layout()
plt.xlabel("Infection Rate (Beta)")
plt.ylabel("Recovery Rate (Gamma)")
plt.show()

