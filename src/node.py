# Node Module for Protocol Simulation

from numpy import random

class Node:
    def __init__(self, protocol, capacity, fillFactor, 
                 retrievalFactor, statCollector):
        self.protocol = protocol
        self.capacity = capacity
        self.fillFactor = fillFactor
        self.retrivalFactor = retrievalFactor
        self.statCollector = statCollector
