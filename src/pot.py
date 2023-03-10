# Power Of Two (POT) Simulator
import argparse

from statcollector import StatCollector
from utils import Rnd

"""
Some Assumptions:
- Each object is of the same size.
- There can only be integer number of objects. 
- Restoration happens at a random distribution.

Node Settings:
- Capacity: denotes the total number of objects
            physical RAM of the node can store.
- FillFactor: denotes the percentage of RAM that
              needs to be available for the node 
              to accept incoming remote objects.
- RestorePeriod: probabilistical period on which
                 node tries to restore spilled
                 objects. This is in place of
                 actual algorithms.

Random Variables:
- mrnd (Memory Random): the random variable used for
                        memory oscillation, restoration
                        of spilled objects, etc.
- prnd (POT Random): the random variable to be used by
                     the POT algorithm exclusively to
                     find nodes to spill to. 
"""

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
        self.prnd = prnd
        self.mrnd = mrnd

        # node object state
        self.numLocallyOwned = self.mrnd.one(0, self.capacity * 0.9)
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
        # to figure out: whether to spill each node one by one
        # or whether to do batch spilling on the node. 
        pass

        """
        Steps:
        - declare backup list for nodes. 
        - Until node is found OR self.priorityNodes is empty:
        - choose two nodes at random. Pop them from list.
        - compare and evaluate if node has space.
        - if so:
            - add to that node's numLocalObjects
            - add node to spilledToNodes
        - else:
            - Move onto finding from spilledToNodes. 
        """
    
    def memOscillate(self):
        pass

        """
        Steps:
        - Choose an appropriate memory oscillation factor
        - Get a random number from `mrnd`
        - Add to node's self.numLocalObjects
        """

    def run(self):
        pass
        
        """
        Steps:
        - restore all relevant objects
        - calculate objects to evict
        - choose nodes to spill to using findNodeToSpill
        - send those nodes relevant remote objects
        """
    
    ## Helper Functions ##

    def filled(self):
        totalObjectCount = self.numLocallyOwned + self.numFromRemote
        return 1.0 * totalObjectCount / self.capacity
        

# helper function to create PNodes
def pnodeFactory(id: int, args: argparse.Namespace, 
                 statCollector:StatCollector, 
                 prnd: Rnd, mrnd: Rnd):
    return PNode(id, args.capacity, args.fill_factor, 
                 args.restore_period, statCollector, prnd, mrnd)
