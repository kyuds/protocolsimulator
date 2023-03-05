# Power Of Two (POT) Simulator

class PNode:
    def __init__(self, id, capacity, fillFactor, 
                 retrievalFactor, statCollector):
        # settings
        self.id = id
        self.capacity = capacity
        self.fillFactor = fillFactor
        self.retrievalFactor = retrievalFactor
        self.statCollector = statCollector

        # node state

