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
    num = random.randint(0,99)
    if num < Beta: 
        return True
    return False 

def flipstateZ(node): 
    num = random.randint(0,99)  
    if num < Beta: 
        return True
    return False 

def flipstateR(states):
    num2 = random.randint(0,999)
    if num2 < Gamma:
        return True
    return False

def flipstateS(states):
    num3 = random.randint(0,999)
    if num3 < Epsilon:
        return True
    return False

mses = []
for iteration in range(3):
    EGBavgdurations  = []
    EGBavgnewusers = []
    EGBbetweeninfection = []
    for Epsilon in [7,8,9,10,11]: #, 30,40,50,60,70]: 
        print(Epsilon)
        Gammabetaavgdurations = []
        Gammabetaavgnewusers = []
        Gammabetabetweeninfection = []
        for Gamma in [70,80,90,100,110,120]: #, 10, 15, 20,25,30]:
            print(Gamma)
            betaavgdurations = []
            betaavgnewusers = []
            betbetweeninfection = []
            for Beta in [10, 15, 20,25,30]: #,6, 8,10,12]: #in range(2,8,2):
                print(Beta)

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
                    didnottweetyesterday = 0 
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
                                                        # activelyinfected += 1
                                                elif neighbor in communities[1]:
                                                    if flipstateZ(neighbor) is True: 
                                                        infectedstates[neighbor] = "Z"
                                                        didnottweetyesterday += 1
                                                        betweeninfection += 1
                                if flipstateR(node) is True:
                                    infectedstates[node] = "R"
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
                                                        # activelyinfected += 1
                                                elif neighborz in communities[0]:
                                                    if flipstateI(neighborz) is True:
                                                        infectedstates[neighborz] = "I"
                                                        didnottweetyesterday += 1
                                                        betweeninfection += 1
                                if flipstateR(node) is True:
                                    infectedstates[node] = "R"

                            elif state == "R":
                                if flipstateS(node) is True: 
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

                # # to find short duration
                shortdurations = []
                for user, activedays in useractivedays.items():
                    for k, g in groupby(enumerate(activedays), lambda (i, x): i-x):
                        shortdurations.append(len(map(itemgetter(1), g)))
        
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

    Meansqerror = np.array(map(sum, zip(zavgduration, zbetweeninfection, zavgnewusers))) #use avgnewusers
    print(Meansqerror)
    print("Min MSE")
    print(min(Meansqerror))
    print((Meansqerror.tolist()).index(min(Meansqerror))+1)

    mses.append(Meansqerror)

print(mses)
# print(mses[0])
# print(mses[1])
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

# mesemap = [Meansqerror[i:i+8] for i in range(0, len(Meansqerror), 8)]
mesemap = avgmse.reshape(5,6,5)
BGmap = np.round(mesemap.mean(axis=0),2)


Gamma = [70,80,90,100,110,120] #, 10, 15, 20,25]  #,8,10,12,14,16,18,20,22,24,26,28,30]
Beta = [10, 15, 20,25,30] #,6,8,10,12]  #2.5,3,3.5,4] #[2,4,6] #,8,10,12,14,16,18,20,22,24,26,28,30]
Epsilon = [7,8,9,10,11] #, 30,40,50,60]
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

# ax.set_title("Harvest of local farmers (in tons/year)")
fig.tight_layout()
plt.xlabel("Infection Rate (Beta)")
plt.ylabel("Recovery Rate (Gamma)")
plt.show()

GEmap = np.round(mesemap.mean(axis=2),2)
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

# ax.set_title("Harvest of local farmers (in tons/year)")
fig.tight_layout()
plt.xlabel("Recovery Rate (Gamma)")
plt.ylabel("Recvoered to Susceptible Transition Rate (Xi)")
plt.show()

BEmap = np.round(mesemap.mean(axis=1),2)
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

# ax.set_title("Harvest of local farmers (in tons/year)")
fig.tight_layout()
plt.xlabel("Infection Rate (Beta)")
plt.ylabel("Recovered to Susceptible Transition Rate (Xi)")
plt.show()

