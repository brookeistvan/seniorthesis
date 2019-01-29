import os
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import random

networkgeom = {1:[2,3], 2:[1,4,5], 3:[1,4], 4:[2,3,5], 5:[2,4]}

infectedstates = {1:"S", 2:"I", 3:"S", 4:"S", 5:"S"}
# for i in range(1, len(networkgeom)):
#     infectedstates.update({i:S})


def isallinfected(states): 
    for k,v in states.items():
        if v == "S":    # there is still a susceptible ie not all infected 
            return False
    return True  # ie all are I 

def flipstate(node): 
    num = random.randint(0,9)  # random number 0-9
    if num < 5: 
        return True
    return False 

itercount = 0 

# for i in range(10)
# for different start node 
while isallinfected(infectedstates) is not True:
    itercount +=1
    for node, state in infectedstates.items():
        if state == "I": 
            for key, neighbors in networkgeom.items():
                if key == node: 
                    for neighbor in neighbors:
                        if flipstate(neighbor) is True: 
                            infectedstates[neighbor] = "I"
#itercount_by_iteration.append(itercount)
print(itercount)

