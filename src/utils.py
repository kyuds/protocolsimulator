import numpy as np

class Rnd:
    def __init__(self, seed: int):
        self.seed = seed
        self.rnd = np.random.default_rng(seed)
    
    def reset(self):
        self.rnd = np.random.default_rng(self.seed)

    def one(self, low: int, high: int):
        self.rnd.integers(low=low, high=high, size=1)[0]
    
    def distinctPair(self, low: int, high: int):
        f = s = self.one(low, high)
        while f == s:
            s = self.one(low, high)
        return f, s