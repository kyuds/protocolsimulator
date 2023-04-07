from utils import Rnd
from statcollector import StatCollector
import random
import numpy as np

class CNode:
    def __init__(self, id: int, capacity: int, threshold: float, 
                 statcollector: StatCollector, rnd: Rnd):
        # node properties
        self.capacity = capacity
        self.minCapacity = int(0.1 * self.capacity)
        self.osc = int(0.2 * self.capacity)
        self.threshold = threshold # spill if threshold is exceeded

        # node state
        self.id = id
        self.numObjects = self.minCapacity

        # add all nodes to fingertable
        self.ftable = []


        # node utils
        self.sc = statcollector
        self.rnd = rnd
    
    def shuffle(self):
        self.numObjects += self.rnd.get(-1 * self.osc, self.osc + 1)
        
        if self.numObjects < self.minCapacity:
            self.numObjects = self.minCapacity
    
    def needToSpill(self):
        return self.numObjects > int(self.capacity * self.threshold)

    def __repr__(self):
        return "C" + str(self.id)
    
    def setFingerTable(self, idCircle):
        n = len(idCircle)
        m = int(np.log2(n))
        for k in range(m):
            start = (idCircle.index(self) + 2**k) % n
            for i in range(n):
                if idCircle[(start + i) % n] != -1:
                    successor = idCircle[(start + i) % n]
                    break
            self.ftable.append([start, successor])
        print(self.ftable)
    
    def run(self):
        pass

# CHORD: Create 2d-array ID Circle
# TODO: SHA-1 encoding
def idCircle(nodes):
    n = len(nodes)
    size, m = idCircleLength(n)
    circle = [-1] * size
    nodeIDs = random_combinations(range(size), n)
    i = 0
    for node in nodes:
        circle[nodeIDs[i]] = node
        i += 1
    return circle

# CHORD: temporary helper function to find smallest power of 2 that is greater than 2 * nn
# po2 = size of id circle
# m = # of bits to represent size of circle -> i.e. log(po2)
def idCircleLength(num_nodes):
    circleLength = 2*num_nodes
    po2 = 1
    m = 0
    while po2 < circleLength:
        po2 *= 2
        m += 1
    return po2, m

# CHORD: helper function for randomly picking ids for identifier circle
# id_length = [0, length of identifier circle]
# num_nodes = # of nodes
def random_combinations(id_length, num_nodes):
    idCircle = list(id_length)
    n = len(id_length)
    random_indices = random.sample(range(n), num_nodes)
    return list(idCircle[i] for i in random_indices)