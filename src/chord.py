# Chord Protocol Simulator

class CNode:
    def __init__(self, id, capacity, fillFactor, 
                 retrievalFactor, statCollector):
        # settings
        self.id = id
        self.capacity = capacity
        self.fillFactor = fillFactor
        self.retrievalFactor = retrievalFactor
        self.statCollector = statCollector

        # node state

