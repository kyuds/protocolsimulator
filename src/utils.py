import numpy as np

class Rnd:
    def __init__(self, seed: int):
        self.seed = seed
        self.rnd = np.random.default_rng(seed)
    
    def reset(self):
        self.rnd = np.random.default_rng(self.seed)

    def one(self, low: int, high: int):
        self.rnd.integers(low=low, high=high, size=1)[0]
    
    # specifically for power of two: choose two distinct
    # numbers from given range, high exclusive.
    # smaller number is always returned first 
    def distinctPair(self, low: int, high: int):
        f = s = self.one(low, high)
        while f == s:
            s = self.one(low, high)
        return min(f, s), max(f, s)
    