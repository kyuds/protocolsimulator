# Class for Collecting Various Statistics

class StatCollector:
    def __init__(self):
        self.data = []
    
    def addEntry(self, epoch: int):
        self.data.append([epoch, 0, 0])
    
    def addQueryTime(self, node):
        self.data[-1][1] += node.numQueries

    def nodeSpilledToDisk(self, node):
        if node.spilledToDisk:
            self.data[-1][2] += 1

"""
ok so statcollector is going to store 3 variables per epoch (this is per balancing):
1. epoch number
2. number of total queries done to balance
3. number of nodes that spilled to disk. 

So you can see in main.py from line 56, you add a new entry to the statcollector by
calling sc.addEntry(), and then you increment queryTime and also nodes spilled to disk
if the node actually did ended up spilling to disk.

To keep track of this, I added two new variables to CNode and PNode:
1. self.numQueries      (integer)
2. self.spilledToDisk   (boolean)

numQueries is supposed to keep track of how many queries this node ended up doing.
spilledToDisk is a boolean that is set to True when our protocol eventually decides 
to spill to disk.

using node.resetStats() (this i also coded into the class too and is used in main automatically)
we reset numQueries to 0 and spilledToDisk to False for a new "run"

so what we want to do, I think for now, is first increment numQueries by 1 whenever we
call run() on a node. Also, when we decide to spillToDisk, we "spill" by decreasing
numObjects by the appropriate amount (just set it to threshold?) and then set the variable
to True.
"""
