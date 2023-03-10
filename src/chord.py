# Chord Protocol Simulator

class CNode:
    def __init__(self, id, capacity, fillFactor, 
                 retrievalFactor, statCollector, rs, m):
        # settings
        id_length = m # m = identifier length -> must be large enough to make probability of two node/keys having same id negligible
        self.id = id
        self.capacity = capacity
        self.fillFactor = fillFactor
        self.restoreFactor = restoreFactor
        self.statCollector = statCollector

        # random variables
        self.rs = rs

        # finger table -> for now assume id is always initialized to 1.
        endpoints = [] # endpoints contain all .start values + the upper bound of the last finger interval
        for i in range(id_length + 1):
            endpoints.append((id + 2**i) % (2**id_length)) # assumes id is an int
        self.ftable = {} # maps from starting id -> interval
        for i in range(len(endpoints) - 1):
            self.ftable[endpoints[i]] = [endpoints[i], endpoints[i + 1]]

        # node state
        self.successor = 0
        self.predecessor = 0

    def get_successor(self):
        return self.successor
    
    def get_predecessor(self):
        return self.predecessor

def cnodeFactory(id, args, statCollector, rs):
    return None


# For now don't think about hashing id. Work on base chord protocol
# Todo
# __init__ -> make finger table