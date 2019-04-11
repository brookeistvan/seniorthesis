import os
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import random

# Define network structure node is key and value is a list of neighbors, you can experience by changing neighbor connections 
networkgeom = {1:[2,3], 2:[1,4,5], 3:[1,4], 4:[2,3,5], 5:[2,4]}

# Define functions 
def isallinfected(states): 
    for k,v in states.items():
        if v == "S":    # there is still a susceptible ie not all infected 
            return False
    return True  # ie all are I 

def flipstate(node): 
    num = random.randint(0,99)  # random number 0-9
    if num < threshold: 
        return True
    return False 


## Run simulation
iterations_count_by_start_and_threshold = []

# Iterate through different infection probabilities here 1-10%
for threshold in range(1,11):
    iterations_count_by_start_node = []

    # Iterate through infection starting with each different node
    for s in range(1, (len(networkgeom)+1)):
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

        # List with 5 elements that are average number of iterations until all nodes are infected
        iterations_count_by_start_node.append(np.mean(itercount_by_iteration))
    iterations_count_by_start_and_threshold.append(iterations_count_by_start_node)

# Sort out indexing 
new_all = []
for j in range(5):
    iter_by_threshold = []
    for k in range(len(iterations_count_by_start_and_threshold)):
        iter_by_threshold.append(iterations_count_by_start_and_threshold[k][j])
    new_all.append(iter_by_threshold)

# Plot number of iterations until all nodes are infected vs beta for starting with each different node
x = []
count = 1 
for n in range(len(new_all[0])):
    x.append(count)
    count +=1

for l in range(len(new_all)):
    plt.plot(x, new_all[l], label='start node %s'%l)
plt.xlabel("Percent chance of infection (beta)")
plt.ylabel("Number of iterations until all infected")
plt.legend()
plt.show()


