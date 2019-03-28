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
import math

# (# groups, # vertices in each group, probability of connecting within group, probability of connecting between groups, seed for random number generator)
G = nx.random_partition_graph([800,200],.1,.0125)
adjacencydict = nx.to_dict_of_dicts(G, nodelist=None, edge_data = None)
communities = list(greedy_modularity_communities(G))

# # create dict for states and one infected
# infectedstates = {}
# for n in range(len(adjacencydict)):
#     infectedstates.update({n:"S"})

# startnode = random.randint(0,len(adjacencydict)) 
# infectedstates.update({startnode:"I"})

def flipstateI(node): 
    num = random.randint(0,999)  # random number 0-9
    if num < Beta: 
        return True
    return False 

def flipstateZ(node): 
    num = random.randint(0,999)  # random number 0-9
    if num < Beta: 
        return True
    return False 

def flipstateR(states):
    num2 = random.randint(0,99)
    if num2 < Gamma:
        return True
    return False


mses = []
for iteration in range(3):
    Gammabetaavgdurations = []
    Gammabetaavgnewusers = []
    Gammabetabetweeninfection = []
    for Gamma in [2, 3, 4, 5, 6, 8, 10, 12]: 
        # print(Gamma)
        betaavgdurations = []
        betaavgnewusers = []
        betbetweeninfection = []
        for Beta in [4,5,6,7,8,9,10]:
            # print(Beta)

            # create dict for states and one infected
            infectedstates = {}
            for n in range(len(adjacencydict)):
                infectedstates.update({n:"S"})

            startnode = random.randint(0,len(communities[0])) 
            infectedstates.update({startnode:"I"})

            useractivedays = {}
            usersentering_by_iteration = []
            usersinfected_by_iteration = []
            betweeninfection = 0 
            for i in range(426):
                infecteds = 0
                newusers = 0 
                # activelyinfected = 0
                for node, state in infectedstates.items():
                    if state == "I": 
                        infecteds += 1
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
                                        elif neighbor in communities[1]:
                                            if flipstateZ(neighbor) is True: 
                                                infectedstates[neighbor] = "Z"
                                                if neighbor not in useractivedays.items():
                                                    newusers += 1
                                                    betweeninfection += 1
                        if flipstateR(node) is True:
                            infectedstates[node] = "R"
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
                                                if neighborz not in useractivedays.keys():
                                                    newusers += 1
                                        elif neighborz in communities[0]:
                                            if flipstateI(neighborz) is True:
                                                infectedstates[neighborz] = "I"
                                                if neighborz not in useractivedays.keys():
                                                    newusers += 1
                                                    betweeninfection += 1
                        if flipstateR(node) is True:
                            infectedstates[node] = "R"


                usersentering_by_iteration.append(newusers)
                usersinfected_by_iteration.append(infecteds)
            enteroverinfect = np.array(usersentering_by_iteration)/np.array(usersinfected_by_iteration)
            avgnewusers = []
            for i in enteroverinfect: 
                if math.isnan(i) is False: 
                    avgnewusers.append(i)
            meannewusers = np.mean(np.array(avgnewusers))
            betaavgnewusers.append(meannewusers)
            betbetweeninfection.append(np.array(betweeninfection))

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

    print("avg durations")
    print(Gammabetaavgdurations)
    print("avg new users per day")
    print(Gammabetaavgnewusers)
    print("number of users between infection")
    print(Gammabetabetweeninfection)

    zavgduration = []
    MEavgduration = []
    for row in Gammabetaavgdurations:
        for i in row:
            errori = np.round((i - 28.0628477471)**2,2)
            MEavgduration.append(errori) 
    sd1 = np.std(MEavgduration)
    for i in MEavgduration:
        zavgduration.append(i/sd1)

    zbetweeninfection = []
    MEbetweeninfection = []
    for row in Gammabetabetweeninfection:
        for j in row:
            scaledj = 100*(j/(len(useractivedays)))
            errorj = np.round((scaledj - 15)**2,2)
            MEbetweeninfection.append(errorj)
    sd2 = np.std(MEbetweeninfection)
    for i in MEbetweeninfection:
        zbetweeninfection.append(i/sd2)

    # make sure its NEW users in the simulation in SIR it is but in other is not
    # Avg percent of users new
    zavgnewusers = []
    MEavgnewusers = []
    for row in Gammabetaavgnewusers:
        for k in row:
            scaledk = 100*(k)
            errork = np.round((scaledk - 54.9244279666)**2, 2)
            MEavgnewusers.append(errork)
    sd3 = np.std(MEavgnewusers)
    for i in MEavgnewusers:
        zavgnewusers.append(i/sd3)

    Meansqerror = np.array(map(sum, zip(zavgduration, zbetweeninfection, zavgnewusers)))
    print(Meansqerror)
    print("Min MSE")
    print(min(Meansqerror))
    print((Meansqerror.tolist()).index(min(Meansqerror))+1)
    mses.append(Meansqerror)
print(mses)
print(mses[0])
print(mses[1])
zippedmse = zip(mses[0], mses[1], mses[1])
print(zippedmse)
stdmse = [np.std(i) for i in zippedmse]
avgmse = np.round(np.array([np.mean(item) for item in zippedmse]),2)
print(avgmse)
print("min avg mse")
print(min(avgmse))
print((avgmse.tolist()).index(min(avgmse))+1)
print("standard deviations")
print(stdmse)


mesemap = [avgmse[i:i+7] for i in range(0, len(avgmse), 7)]
print(mesemap)

Gamma = [2, 3,4,5,6,8,10,12] #[2,4,6] #,8,10,12,14,16,18,20,22,24,26,28,30]
Beta = [4,5,6,7,8,9,10]#[2,3,4,5,6,8,10,12] #[2,4,6] #,8,10,12,14,16,18,20,22,24,26,28,30]

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

