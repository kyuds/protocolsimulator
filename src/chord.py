# Chord Protocol Simulator

class CNode:
    def __init__(self, id, capacity, fillFactor, 
                 restoreFactor, statCollector, rs):
        # settings
        self.id = id
        self.capacity = capacity
        self.fillFactor = fillFactor
        self.restoreFactor = restoreFactor
        self.statCollector = statCollector

        # random variables
        self.rs = rs

        # node state

def cnodeFactory(id, args, statCollector, rs):
    return None
