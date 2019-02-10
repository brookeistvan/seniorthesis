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
import datetime as dt
import matplotlib.dates as mdates


G = nx.random_partition_graph([50,30],.7,.2)
adjacencydict = nx.to_dict_of_dicts(G, nodelist=None, edge_data = None)

# make a visual graph to represent the network underlying simulation
# outputdir = "/Users/brookeistvan/Documents/Thesis/seniorthesis"
# nx.write_gexf(G, outputdir+"SIgraph.gexf")

# define functions 
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

iteration_count_by_threshold = []
for threshold in range(1,11):
    itercount_by_iteration = []
    iteration_count_by_iteration = []
    for i in range(10):
        itercount = 0 
        infectedstates = {}
        for n in range(len(adjacencydict)):
            infectedstates.update({n:"S"})
        startnode = random.randint(0,len(adjacencydict)) 
        infectedstates.update({startnode:"I"})
        while isallinfected(infectedstates) is not True:
            itercount +=1
            for node, state in infectedstates.items():
                if state == "I": 
                    for key, neighbors in adjacencydict.items():
                        if key == node: 
                            for neighbor in neighbors:
                                if flipstate(neighbor) is True: 
                                    infectedstates[neighbor] = "I"
        itercount_by_iteration.append(itercount)
        print(itercount_by_iteration)
        print(itercount)

    # list with 5 elements (because was 5 start nodes) that are average number of iterations
    iteration_count_by_iteration.append(np.mean(itercount_by_iteration))
    print(iteration_count_by_iteration)
iteration_count_by_threshold.append(iteration_count_by_iteration)

# print(iterations_count_by_start_node)
print(iteration_count_by_threshold)
