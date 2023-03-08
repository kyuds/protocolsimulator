# Class for Collecting Various Statistics

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
