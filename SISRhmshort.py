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
from itertools import groupby
from operator import itemgetter

# (# groups, # vertices in each group, probability of connecting within group, probability of connecting between groups, seed for random number generator)
G = nx.random_partition_graph([800,200],.1,.0125)
adjacencydict = nx.to_dict_of_dicts(G, nodelist=None, edge_data = None)
communities = list(greedy_modularity_communities(G))

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

mses = []
for iteration in range(3):
    EGBavgdurations  = []
    EGBavgnewusers = []
    EGBbetweeninfection = []
    for Epsilon in [5,10,15,20,25,30]: 
        print(Epsilon)
        Gammabetaavgdurations = []
        Gammabetaavgnewusers = []
        Gammabetabetweeninfection = []
        for Gamma in [5, 10, 15, 20,25,30]:
            print(Gamma)
            betaavgdurations = []
            betaavgnewusers = []
            betbetweeninfection = []
            for Beta in [8,10,12,14,16]: #in range(2,8,2):
                print(Beta)

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
                    didnottweetyesterday = 0
                    infecteds = 0
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
                                                    didnottweetyesterday += 1
                                                    # if neighbor not in useractivedays.keys():
                                                    #     newusers += 1
                                                    # activelyinfected += 1
                                            elif neighbor in communities[1]:
                                                if flipstateZ(neighbor) is True: 
                                                    infectedstates[neighbor] = "Z"
                                                    didnottweetyesterday += 1
                                                    # if neighbor not in useractivedays.keys():
                                                    #     newusers += 1 
                                                    # activelyinfected += 1
                                                    betweeninfection += 1
                            if flipstateR(node) is True:
                                infectedstates[node] = "R"
                            elif flipstateS(node) is True: 
                                infectedstates[node] = "S"
                        elif state == "Z":
                            infecteds += 1
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
                                                    didnottweetyesterday += 1
                                                    # if neighbor not in useractivedays.keys():
                                                    #     newusers += 1
                                                    # activelyinfected += 1
                                            elif neighborz in communities[0]:
                                                if flipstateI(neighborz) is True:
                                                    infectedstates[neighborz] = "I"
                                                    didnottweetyesterday += 1
                                                    # if neighbor not in useractivedays.keys():
                                                    #     newusers += 1
                                                    # activelyinfected += 1 
                                                    betweeninfection += 1
                            if flipstateR(node) is True:
                                infectedstates[node] = "R"
                            elif flipstateS(node) is True:
                                infectedstates[node] = "S"

                    usersinfected_by_iteration.append(infecteds)
                    usersentering_by_iteration.append(didnottweetyesterday)
                enteroverinfect = np.array(usersentering_by_iteration)/np.array(usersinfected_by_iteration)
                avgnewusers = []
                for i in enteroverinfect: 
                    if math.isnan(i) is False: 
                        avgnewusers.append(i)
                meannewusers = np.mean(np.array(avgnewusers))
                betaavgnewusers.append(meannewusers)
                betbetweeninfection.append(betweeninfection)


                # durations = []
                # durationdict = {}
                # for user, activedays in useractivedays.items():
                #     duration = 0
                #     duration += (activedays[-1] - activedays[0])
                #     durations.append(duration)

                # # to find short duration
                shortdurations = []
                for user, activedays in useractivedays.items():
                    for k, g in groupby(enumerate(activedays), lambda (i, x): i-x):
                        shortdurations.append(len(map(itemgetter(1), g)))
                # print(np.mean(shortdurations))
                # print(len(shortdurations))

                avgduration = np.mean(shortdurations)
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

    zavgduration =[]
    MEavgduration = []
    for a in EGBavgdurations:
        for row in a:
            for i in row:
                errori = np.round((i - 1.03932135873)**2,2)
                MEavgduration.append(errori) 
    sd1 = np.std(MEavgduration)
    for i in MEavgduration:
        zavgduration.append(i/sd1)

    zbetweeninfection = []
    MEbetweeninfection = []
    for b in EGBbetweeninfection:
        for row in b:
            for j in row:
                scaledj = 100*(j/(len(useractivedays)))
                errorj = np.round((scaledj - 26.5)**2,2)
                MEbetweeninfection.append(errorj)
    sd2 = np.std(MEbetweeninfection)
    for i in MEbetweeninfection:
        zbetweeninfection.append(i/sd2)

    # make sure its NEW users in the simulation in SIR it is but in other is not
    # Avg percent of users new
    zavgnewusers = []
    MEavgnewusers = []
    for c in EGBavgnewusers:
        for row in c:
            for k in row:
                scaledk = 100*(k)
                errork = np.round((scaledk - 96.22)**2, 2)
                MEavgnewusers.append(errork)
    sd3 = np.std(MEavgnewusers)
    for i in MEavgnewusers:
        zavgnewusers.append(i/sd3)

    # print(MEavgnewusers)
    # print(MEbetweeninfection)
    # print(MEavgduration)
    Meansqerror = np.array(map(sum, zip(zavgduration, zbetweeninfection, zavgnewusers))) #use avgnewusers
    # sd4 = np.std(Meansqerror)
    # zmsei = []
    # for i in Meansqerror: 
    #     zmsei.append(i/sd4)
    # zmse = np.array(zmsei)
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
avgmse = np.array([np.mean(item) for item in zippedmse])
print(avgmse)
print("min avg mse")
print(min(avgmse))
print((avgmse.tolist()).index(min(avgmse))+1)
print("standard deviations")
print(stdmse)

# mesemap = [Meansqerror[i:i+8] for i in range(0, len(Meansqerror), 8)]
# epsilon, gamma, beta
mesemap = avgmse.reshape(6,6,5)
BGmap = np.round(mesemap.mean(axis=0),2)
print(BGmap)


Gamma = [5, 10, 15, 20,25,30] #[2,5,10,15,20,25,30] #, 20, 25, 30] #,8,10,12,14,16,18,20,22,24,26,28,30]
Beta = [8,10,12,14,16] #[2,3,4,5,6,8,10] #[2,4,6,8,10,12] #,10,15] #2.5,3,3.5,4] #[2,4,6] #,8,10,12,14,16,18,20,22,24,26,28,30]
Epsilon = [5, 10, 15, 20,25,30]  #[5,10,15,20,25, 30] #,8,10]
# 1,40,3

fig, ax = plt.subplots()
im = ax.imshow(BGmap)

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
        text = ax.text(j, i, BGmap[i][j],
                       ha="center", va="center", color="w")

fig.tight_layout()
plt.xlabel("Infection Rate (Beta)")
plt.ylabel("Recovery Rate (Gamma)")
plt.show()

GEmap = np.round(mesemap.mean(axis=2),2)
print(GEmap)
fig, ax = plt.subplots()
im = ax.imshow(GEmap)

# We want to show all ticks...
ax.set_xticks(np.arange(len(Gamma)))
ax.set_yticks(np.arange(len(Epsilon)))
# ... and label them with the respective list entries
ax.set_xticklabels(Gamma)
ax.set_yticklabels(Epsilon)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(Epsilon)):
    for j in range(len(Gamma)):
        text = ax.text(j, i, GEmap[i][j],
                       ha="center", va="center", color="w")

fig.tight_layout()
plt.xlabel("Recovery Rate (Gamma)")
plt.ylabel("Recvoered to Susceptible Transition Rate (Xi)")
plt.show()

BEmap = np.round(mesemap.mean(axis=1),2)
print(BEmap)
fig, ax = plt.subplots()
im = ax.imshow(BEmap)

# We want to show all ticks...
ax.set_xticks(np.arange(len(Beta)))
ax.set_yticks(np.arange(len(Epsilon)))
# ... and label them with the respective list entries
ax.set_xticklabels(Beta)
ax.set_yticklabels(Epsilon)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(Epsilon)):
    for j in range(len(Beta)):
        text = ax.text(j, i, BEmap[i][j],
                       ha="center", va="center", color="w")

fig.tight_layout()
plt.xlabel("Infection Rate (Beta)")
plt.ylabel("Recovered to Susceptible Transition Rate (Xi)")
plt.show()