# Class for Collecting Various Statistics

"""
Data to collect:
- Node State: Percentage Full
"""

class StatCollector:
    def __init__(self, latency):
        self.latency = latency
        self.data = []
    
    def aggregate(self):
        totalStats = {}

        for key in self.data[0].keys():
            st = 0
            for d in self.data:
                st += d[key]
            totalStats[key] = st

        return totalStats

    def logStats(self):
        print("Results:")
    
    def addNewEntry(self):
        self.data.append({
            "nodeStates": [],
            "spillRestore": [],
            # add more fields here. 
        })
    
    def addNodeState(self, id, fp):
        self.data[-1]["nodeStates"].append((id, fp))
    
    def addRestoreData(self, id, n):
        self.data[-1]["spillRestore"].append((id, n))
