# Power Of Two (POT) Simulator
import argparse

from statcollector import StatCollector
from utils import Rnd

# PNode Class
class PNode:
    def __init__(self, id: int, capacity: int, fillFactor: float, 
                 restorePeriod: int, statCollector: StatCollector, 
                 prnd: Rnd, mrnd: Rnd):
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
        self.prnd = prnd
        self.mrnd = mrnd

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
                 prnd: Rnd, mrnd: Rnd):
    return PNode(id, args.capacity, args.fill_factor, 
                 args.restore_period, statCollector, prnd, mrnd)
