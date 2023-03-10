# Chord Protocol Simulator
import random
from numpy.random import randint

class CNode:
    def __init__(self, id, capacity, fillFactor, 
                 restoreFactor, statCollector, rs, m):
        # settings
        id_length = m # m = identifier length -> must be large enough to make probability of two node/keys having same id negligible
        self.id = id
        self.capacity = capacity
        self.fillFactor = fillFactor
        self.restoreFactor = restoreFactor
        self.statCollector = statCollector
        
        # object store
        self.numLocalObjects = 0
        self.numFromRemote = 0

        # random variables
        self.rs = rs

        # finger table -> for now assume id is always initialized to 1.
        endpoints = [] # endpoints contain all .start values + the upper bound of the last finger interval
        for i in range(id_length + 1):
            endpoints.append((id + 2**i) % (2**id_length)) # assumes id is an int
        self.ftable = [] # [interval start, interval end] (interval start == .start)
        for i in range(len(endpoints) - 1):
            self.ftable.append([endpoints[i], endpoints[i + 1]])

        # node state
        self.successor = 0
        self.predecessor = 0

    def get_successor(self):
        return self.successor
    
    def get_predecessor(self):
        return self.predecessor

# CHORD: helper function for randomly picking ids for identifier circle
# id_length = [0, length of identifier circle]
# num_nodes = # of nodes
def random_combinations(id_length, num_nodes):
    idCircle = list(id_length)
    n = len(id_length)
    random_indices = random.sample(range(n), num_nodes)
    return list(idCircle[i] for i in random_indices)

# CHORD: helper function to find smallest power of 2 that is greater than 2 * nn
# po2 = size of id circle
# m = # of bits to represent size of circle -> i.e. log(po2)
def idCircleLength(num_nodes):
    circleLength = 2*num_nodes
    po2 = 1
    m = 0
    while po2 < circleLength:
        po2 = po2 * 2
        m += 1
    return po2, m

# CHORD: helper function to query a node for the closest finger preceding id
# node = node that receives query
# id = id that the query is requesting the closest preceding finger of
# m = number of bits to represent identifier circle
def closest_preceding_finger(node, id, m):
    int = [i for i in range(node + 1, id)] # check possible off by one error in id
    for i in range(m, -1, -1):
        if node.ftable[i][2].id in int:
            return node.ftable[i][2]
    return node

# CHORD: helper function to query a node for predecessor of id
def find_predecessor(node, id, m):
    pointer = node
    int = [i for i in range(node.id, node.successor.id)]
    while id not in int:
        pointer = closest_preceding_finger(pointer, id, m)
    return pointer

# CHORD: helper function to query for successor of id
def find_successor(node, id, m):
    previous = find_predecessor(node, id, m)
    return previous.successor

# CHORD: helper function to attempt object spilling to target node
# TODO: how to incorporate timestep into this?
# TODO: object is just counted as 1 for now. (can change)
def queryHandle(node, object=None): # ts?
    queryNodeList = list(set([node] + [i[2] for i in node.ftable]))
    ts = 0 # fix -> needs to be global
    while True:
        for node in queryNodeList:
            if ts % 10 == 0:
                memoryRandomize(queryNodeList)
            res, ts = tryToSpill(node, ts)
            if res:
                return
        print(f"spilling locally")
        node.numLocalObjects += 1 # assume one object is being spilled here
        return


# CHORD: helper function for attempting to spill to target node
def tryToSpill(targetnode, time):
    time += 1
    usage = (targetnode.numLocalObjects + targetnode.numFromRemote) / targetnode.capacity
    if usage >= targetnode.fillFactor:
        print(f"targetnode exceeded fillfactor, spill failed")
        return False, time
    targetnode.numFromRemote += 1 # assume one object is being spilled here
    print(f"spill to {targetnode} successful!")
    return True, time

# CHORD: helper function for re-allocating memory for all nodes -> same as oscillate()?
def memoryRandomize(nodelist):
    for node in nodelist:
        # randomly change numLocalObjects and numFromRemote -> prevention of 
        node.numLocalObjects = randint(0, node.capacity / 2)
        node.numFromRemote = randint(0, node.capacity / 2)



def cnodeFactory(id, args, statCollector, rs):
    return None


# For now don't think about hashing id. Work on base chord protocol
# Todo
# __init__ -> make finger table