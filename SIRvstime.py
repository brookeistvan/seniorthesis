import os
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import random

networkgeom = {0:[1,2], 1:[0,3,4], 2:[0,3], 3:[1,2,4], 4:[1,3]}

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

def isallrecovered(states):
    for k1, v1 in states.items():
        if v1 == "R":
            return True
        return False

def flipstate2(states):
    num2 = random.randint(0,9)
    if num2 < 2:
        return True
    return False

infectedcount_by_iteration = [1]
recoveredcount_by_iteration = [0]
infectedcount = 1
recoveredcount = 0
infectedstates = {0:"I", 1:"S", 2:"S", 3:"S", 4:"S"}
for i in range(10):
    # infectedstates.update({s:"I"})

    # while isallrecovered(infectedstates) is not True:

    for node, state in infectedstates.items():
        if state == "I": 
            for key, neighbors in networkgeom.items():
                if key == node: 
                    for neighbor in neighbors:
                        if infectedstates[neighbor] == "S":
                            if flipstate(neighbor) is True: 
                                infectedstates[neighbor] = "I"
                                infectedcount += 1 
            if flipstate2(node) is True:
                infectedstates[node] = "R"
                recoveredcount += 1
                infectedcount -= 1
    print(infectedstates)
    print(infectedcount)
    print(recoveredcount)
    infectedcount_by_iteration.append(infectedcount)
    recoveredcount_by_iteration.append(recoveredcount)

print(infectedcount_by_iteration)
print(recoveredcount_by_iteration)

# want number of iterations (x) and the number of infecteds (y)
x = []
for n in range(len(infectedcount_by_iteration)):
    x.append(n)
plt.plot(x, infectedcount_by_iteration, label="infected")
plt.plot(x, recoveredcount_by_iteration, label="recovered")
# plt.plot(x, susceptiblecount_by_iteration, label="recovered")
plt.xlabel("iteration")
plt.ylabel("number of infected nodes")
plt.legend()
plt.show()

