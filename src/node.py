# Node Module for Protocol Simulation

class Node:
    def __init__(self, id, protocol, capacity, fillFactor, 
                 retrievalFactor, statCollector):
        self.id = id
        self.protocol = protocol
        self.capacity = capacity
        self.fillFactor = fillFactor
        self.retrivalFactor = retrievalFactor
        self.statCollector = statCollector
