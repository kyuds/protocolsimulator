from utils import Rnd
from statcollector import StatCollector

class PNode:
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

        # node utils
        self.sc = statcollector
        self.rnd = rnd
    
    def shuffle(self):
        self.numObjects += self.rnd.get(-1 * self.osc, self.osc + 1)
        
        if self.numObjects < self.minCapacity:
            self.numObjects = self.minCapacity

    def needToSpill(self):
        return self.numObjects > int(self.capacity * self.threshold)
    
    def run(self):
        pass
