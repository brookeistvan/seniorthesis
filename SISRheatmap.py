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
import numpy as np
from networkx.algorithms.community import greedy_modularity_communities
from operator import add

# (# groups, # vertices in each group, probability of connecting within group, probability of connecting between groups, seed for random number generator)
G = nx.random_partition_graph([700,300],.1,.0125)
adjacencydict = nx.to_dict_of_dicts(G, nodelist=None, edge_data = None)
communities = list(greedy_modularity_communities(G))

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

def flipstateZ(node): 
    num = random.randint(0,99)  # random number 0-9
    if num < Beta: 
        return True
    return False 

def flipstateR(states):
    num2 = random.randint(0,99)
    if num2 < Gamma:
        return True
    return False

def flipstateS(states):
    num3 = random.randint(0,99)
    if num3 < Epsilon:
        return True
    return False

EGBavgdurations  = []
EGBavgnewusers = []
EGBbetweeninfection = []
for Epsilon in range(2,8,2): 
    print(Epsilon)
    Gammabetaavgdurations = []
    Gammabetaavgnewusers = []
    Gammabetabetweeninfection = []
    for Gamma in range(2,8,2):
        print(Gamma)
        betaavgdurations = []
        betaavgnewusers = []
        betbetweeninfection = []
        for Beta in [0.5,1,1.5,2]: #in range(2,8,2):
            print(Beta)

            # create dict for states and one infected
            infectedstates = {}
            for n in range(len(adjacencydict)):
                infectedstates.update({n:"S"})

            startnode = random.randint(0,len(communities[0])) 
            infectedstates.update({startnode:"I"})

            useractivedays = {}
            usersentering_by_iteration = []
            betweeninfection = 0 
            newusers = 0 
            for i in range(426):
                # activelyinfected = 0
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
                                                if neighbor not in useractivedays.keys():
                                                    newusers += 1
                                                # activelyinfected += 1
                                        elif neighbor in communities[1]:
                                            if flipstateZ(neighbor) is True: 
                                                infectedstates[neighbor] = "Z"
                                                if neighbor not in useractivedays.keys():
                                                    newusers += 1 
                                                # activelyinfected += 1
                                                betweeninfection += 1
                        if flipstateR(node) is True:
                            infectedstates[node] = "R"
                        elif flipstateS(node) is True: 
                            infectedstates[node] = "S"
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
                                                if neighbor not in useractivedays.keys():
                                                    newusers += 1
                                                # activelyinfected += 1
                                        elif neighborz in communities[0]:
                                            if flipstateI(neighborz) is True:
                                                infectedstates[neighborz] = "I"
                                                if neighbor not in useractivedays.keys():
                                                    newusers += 1
                                                # activelyinfected += 1 
                                                betweeninfection += 1
                        if flipstateR(node) is True:
                            infectedstates[node] = "R"
                        elif flipstateS(node) is True:
                            infectedstates[node] = "S"

                usersentering_by_iteration.append(newusers)
            avgnewusers = np.mean(usersentering_by_iteration)
            betaavgnewusers.append(avgnewusers)
            betbetweeninfection.append(betweeninfection)


            durations = []
            durationdict = {}
            for user, activedays in useractivedays.items():
                duration = 0
                duration += (activedays[-1] - activedays[0])
                durations.append(duration)

            avgduration = np.mean(durations)
            betaavgdurations.append(avgduration)

        Gammabetaavgdurations.append(np.round(betaavgdurations,1))
        Gammabetaavgnewusers.append(betaavgnewusers)
        Gammabetabetweeninfection.append(betbetweeninfection)
    EGBbetweeninfection.append(Gammabetabetweeninfection)
    EGBavgnewusers.append(Gammabetaavgnewusers)
    EGBavgdurations.append(Gammabetaavgdurations)

print("avg durations")
print(EGBavgdurations)
print("avg new users per day")
print(EGBavgnewusers)
print("number of users between infection")
print(EGBbetweeninfection)

MEavgduration = []
for row in Gammabetaavgdurations:
    for i in row:
        errori = (i - 28.0628477471)**2
        MEavgduration.append(errori) 


MEbetweeninfection = []
for row in Gammabetabetweeninfection:
    for j in row:
        scaledj = j/(len(useractivedays))
        errorj = (j - 0.15)**2
        MEbetweeninfection.append(errorj)


# make sure its NEW users in the simulation in SIR it is but in other is not
# Avg percent of users new
# MEavgnewusers = []
# for row in Gammabetaavgnewusers:
#     for k in row:
#         print(k)
#         scaledk = k/(len(useractivedays))
#         print(scaledk)
#         errork = (k - 0.549244279666)**2
#         print(errork)
#         MEavgnewusers.append(errork)


Meansqerror = map(sum, zip(MEbetweeninfection, MEavgduration)) #use avgnewusers
print(Meansqerror)

print(min(Meansqerror))
print(Meansqerror.index(min(Meansqerror))+1)

mesemap = [Meansqerror[i:i+4] for i in range(0, len(Meansqerror), 8)]

Gamma = [2,4,6] #,8,10,12,14,16,18,20,22,24,26,28,30]
Beta = [0.5,1,1.5,2] #[2,4,6] #,8,10,12,14,16,18,20,22,24,26,28,30]

fig, ax = plt.subplots()
im = ax.imshow(mesemap)

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
        text = ax.text(j, i, mesemap[i][j],
                       ha="center", va="center", color="w")

# ax.set_title("Harvest of local farmers (in tons/year)")
fig.tight_layout()
plt.xlabel("Infection Rate (Beta)")
plt.ylabel("Recovery Rate (Gamma)")
plt.show()