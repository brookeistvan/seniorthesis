import os
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import random

networkgeom = {1:[2,3], 2:[1,4,5], 3:[1,4], 4:[2,3,5], 5:[2,4]}

def isallinfected(states): 
    for k,v in states.items():
        if v == "S":    # there is still a susceptible ie not all infected 
            return False
    return True  # ie all are I 

def flipstate(node): 
    num = random.randint(0,9)  # random number 0-9
    if num < threshold: 
        return True
    return False 



iterations_count_by_start_and_threshold = []

for threshold in range(1,11):
    iterations_count_by_start_node = []
    for s in range(1, (len(networkgeom)+1)):
        # infectedstates = {1:"S", 2:"S", 3:"S", 4:"S", 5:"S"}
        # infectedstates.update({s:"I"})
        itercount_by_iteration = []
        for i in range(100):
            itercount = 0 
            infectedstates = {1:"S", 2:"S", 3:"S", 4:"S", 5:"S"}
            infectedstates.update({s:"I"})
            while isallinfected(infectedstates) is not True:
                itercount +=1
                for node, state in infectedstates.items():
                    if state == "I": 
                        for key, neighbors in networkgeom.items():
                            if key == node: 
                                for neighbor in neighbors:
                                    if flipstate(neighbor) is True: 
                                        infectedstates[neighbor] = "I"
            itercount_by_iteration.append(itercount)

        # list with 5 elements that are average number of iterations
        iterations_count_by_start_node.append(np.mean(itercount_by_iteration))
    iterations_count_by_start_and_threshold.append(iterations_count_by_start_node)

# print(iterations_count_by_start_node)
print(iterations_count_by_start_and_threshold)

x = [1,2,3,4,5,6,7,8,9,10]
# plt.plot(iterations_count_by_start_and_threshold[1][1])

new_all = []
for j in range(5):
    iter_by_threshold = []
    for k in range(len(iterations_count_by_start_and_threshold)):
        iter_by_threshold.append(iterations_count_by_start_and_threshold[k][j])
    new_all.append(iter_by_threshold)
        # plt.plot([pt[k][j] for pt in iterations_count_by_start_and_threshold],label = 'id %s'%j)
print(new_all)
# for j in range(len(iterations_count_by_start_and_threshold)):
#     for k in range(5):
#         new_list_of_lists.append(iterations_count_by_start_and_threshold[j][k])
#         plt.plot([pt[j][k] for pt in iterations_count_by_start_and_threshold],label = 'id %s'%j)
for l in range(len(new_all)):
    plt.plot(x, new_all[l], label='start node %s'%l)
plt.legend()
plt.show()

# use a for loop to generate individual plots, then show them

