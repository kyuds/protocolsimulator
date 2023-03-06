# Power Of Two (POT) Simulator

# PNode Class
class PNode:
    def __init__(self, id, capacity, fillFactor, 
                 retrievalFactor, statCollector, rnd, rs):
        # settings
        self.id = id
        self.capacity = capacity
        self.fillFactor = fillFactor
        self.retrievalFactor = retrievalFactor
        self.statCollector = statCollector

        # random variables
        self.rnd = rnd
        self.rs = rs

        # node object state
        self.numLocallyOwned = 0
        self.numFromRemote = 0

        # node communication state
        self.remoteObjLoc = {}
        self.priorityNodes = []
        self.spilledNodes = []
    
    def addNodeInfo(self, nodesList):
        self.priorityNodes.extend(nodesList)
    
    # samples two random numbers from 0 ~ bnd (exclusive)
    def twoRandomSample(self, bnd):
        gen = lambda b: self.rnd.integers(low=0, high=b, size=1)
        f = s = gen(bnd)[0]
        while f == s:
            s = gen(bnd)[0]
        return f, s

    def findNodeToSpill(self):
        pass
    
    def oscillate(self):
        pass

# helper function to create PNodes
def pnodeFactory(id, args, statCollector, rand):
    return PNode(id, args.capacity, args.fill_factor, 
                 args.retrieval_factor, statCollector, rand)
