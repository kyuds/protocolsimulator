from utils import Rnd
from statcollector import StatCollector

class PNode:
    def __init__(self, id: int, capacity: int, threshold: float, 
                 statcollector: StatCollector, rnd: Rnd, prnd: Rnd):
        # node properties
        self.capacity = capacity
        self.minCapacity = int(0.1 * self.capacity)
        self.osc = int(0.2 * self.capacity)
        self.threshold = threshold # spill if threshold is exceeded

        # node state
        self.id = id
        self.numObjects = self.minCapacity
        self.otherNodes = []

        # node utils
        self.sc = statcollector
        self.rnd = rnd
        self.prnd = prnd # different from rnd in that used by POT.
    
    def shuffle(self):
        self.numObjects += self.rnd.get(-1 * self.osc, self.osc + 1)
        
        if self.numObjects < self.minCapacity:
            self.numObjects = self.minCapacity

    def needToSpill(self):
        return self.numObjects > int(self.capacity * self.threshold)
    
    def addNodes(self, nodes):
        self.otherNodes.extend(nodes)

    def __str__(self):
        return "P" + str(self.id)
    
    def run(self):
        pass
