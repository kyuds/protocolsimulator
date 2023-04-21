from utils import Rnd

class PNode:
    def __init__(self, id: int, capacity: int, threshold: float, 
                 rnd: Rnd, prnd: Rnd):
        # node properties
        self.capacity = capacity
        self.minCapacity = int(0.1 * self.capacity)
        self.osc = int(0.5 * self.capacity)
        self.threshold = threshold # spill if threshold is exceeded

        # node state
        self.id = id
        self.numObjects = self.minCapacity
        self.otherNodes = []
        self.searchedNodes = []

        # node utils
        self.rnd = rnd
        self.prnd = prnd # different from rnd in that used by POT.

        # query stats
        self.spilledToDisk = False
        self.numQueries = 0
    
    def shuffle(self):
        self.numObjects += self.rnd.get(-1 * self.osc, self.osc + 1)
        
        if self.numObjects < self.minCapacity:
            self.numObjects = self.minCapacity

    def needToSpill(self):
        return self.numObjects > int(self.capacity * self.threshold)
    
    def addNodes(self, nodes):
        self.otherNodes.extend(nodes)
    
    def resetStats(self):
        self.spilledToDisk = False
        self.numQueries = 0
        self.otherNodes.extend(self.searchedNodes)
        self.searchedNodes = []

    def __repr__(self):
        return "P" + str(self.id)
    
    def run(self, verbose=False):
        target = None
        numObjectsToSpill = self.numObjects - int(self.threshold * self.capacity)

        if verbose:
            print(f"Running: {self}")
            print(f"Need to spill: {numObjectsToSpill}")
    
        if len(self.otherNodes) == 0:
            if verbose:
                print(f"No nodes to query. Spilling to disk.\n")
            self.spilledToDisk = True
            self.numObjects = int(self.threshold * self.capacity)
            return
        
        if len(self.otherNodes) == 1:
            target = self.otherNodes.pop(0)
            self.searchedNodes.append(target)
            self.numQueries += 1
            if verbose:
                print(f"Querying 1 node: {target}")
        else:
            idx1, idx2 = self.prnd.distinctPair(0, len(self.otherNodes))
            # order is important as popping removes elements
            n2 = self.otherNodes.pop(idx2)
            n1 = self.otherNodes.pop(idx1)
            self.searchedNodes.extend([n1, n2])
            target = min([n1, n2], key=lambda x: x.numObjects)
            self.numQueries += 2 # add two as we are searching two nodes.
            if verbose:
                print(f"Querying 2 nodes: {n1}, {n2}.")
        
        if target.numObjects + numObjectsToSpill <= int(target.threshold * target.capacity):
            self.numObjects -= numObjectsToSpill
            target.numObjects += numObjectsToSpill
            if verbose:
                print(f"Remotely spilled to {target}")
                print(f"{target} numObjects before: {target.numObjects - numObjectsToSpill}")
                print(f"{target} numObjects after:  {target.numObjects}")
        elif verbose:
            print(f"{target} too full.")
        
        if verbose:
            print()
