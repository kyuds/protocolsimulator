# Power Of Two (POT) Simulator
from statcollector import StatCollector
import numpy as np
import argparse

# PNode Class
class PNode:
    def __init__(self, id: int, capacity: int, fillFactor: float, 
                 restorePeriod: int, statCollector: StatCollector, 
                 rnd: np.random._generator.Generator, 
                 rs: np.random._generator.Generator):
        # settings
        self.id = id
        self.capacity = capacity
        self.fillFactor = fillFactor
        self.restorePeriod = restorePeriod
        self.statCollector = statCollector

        # random variables
        # rnd : POT random chooser
        # rs  : Node memory randomness
        #       used for both oscillation
        #       and spilled obj restore
        self.rnd = rnd
        self.rs = rs

        # node object state
        self.numLocallyOwned = 0
        self.numFromRemote = 0
        self.numRemotelySpilled = 0

        # node communication state
        self.remoteObjLoc = {}
        self.priorityNodes = []
        self.spilledToNodes = []
    
    # nd can both be a list of nodes or just a single one. 
    def addNodeInfo(self, nd: list):
        self.priorityNodes.extend(nd)
    
    # samples two random numbers from 0 ~ bnd (exclusive)
    def twoRandomSample(self, bnd: int):
        f = s = rndOne(self.rnd, 0, bnd)
        while f == s:
            s = rndOne(self.rnd, 0, bnd)
        return f, s

    def findNodeToSpill(self):
        pass
    
    def oscillate(self):
        pass

    def run(self):
        # conduct object restore first
        toRetrieve = 0
        if rndOne(self.rs, 0, self.restorePeriod) == 0:
            toRetrieve = rndOne(self.rs, 1, self.numRemotelySpilled)
            # do restore
        
        self.statCollector.addRestoreData(id, toRetrieve)

        numObjects = self.numLocallyOwned + self.numFromRemote
        numPossible = round(self.capacity * self.fillFactor)
        fp = numObjects / numPossible

        if numObjects <= numPossible:
            # no need as server is relatively sparse
            self.statCollector.addNodeState(self.id, fp)
            return

        # figure out how to actually spill stuff
        

# helper function to create PNodes
def pnodeFactory(id: int, args: argparse.Namespace, 
                 statCollector:StatCollector, 
                 rnd: np.random._generator.Generator, 
                 rs: np.random._generator.Generator):
    return PNode(id, args.capacity, args.fill_factor, 
                 args.restore_period, statCollector, rnd, rs)

# other helper functions
def rndOne(rnd, low: int, high: int):
    return rnd.integers(low=low, high=high, size=1)[0]
