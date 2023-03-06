# library imports
import argparse
import numpy as np

# custom imports
from statcollector import StatCollector
from pot import pnodeFactory
from chord import cnodeFactory

def run():
    # parse arguments
    parser = argparse.ArgumentParser(description="Settings for Protocol Simulator")
    parser.add_argument("--num-nodes", default=10, type=int, help="Number of nodes")
    parser.add_argument("--protocol", default="chord", type=str, help="Type of protocol: chord/pot")
    parser.add_argument("--latency", default=10, type=int, help="Network latency (in ms)")
    parser.add_argument("--capacity", default=100, type=int, help="Object capacity")
    parser.add_argument("--fill-factor", default=0.7, type=float, help="Factor of memory fill achieved before eviction")
    parser.add_argument("--retrieval-factor", default=0.2, type=float, help="Probability of object restore")
    parser.add_argument("--oscillate-period", default=10, type=float, help="Memory state change period")
    parser.add_argument("--total-epochs", default=1000, type=float, help="Total number of epochs to simulate")
    args = parser.parse_args()

    # settings
    op = args.oscillate_period
    rs = np.random.default_rng(1000)

    if args.protocol == "chord":
        # follow template as shown in below. Lets try to have the same formatting. 
        # unlike POT, Chord only needs one random variable (for memory oscillation)
        # so you just need to add "rs", which is the oscillator variable. 
        allNodes = []
        pass
    elif args.protocol == "pot":
        # initialize a single random generator for POT decision making.
        rnd = np.random.default_rng(12345)
        sc = StatCollector(args.latency)
        allNodes = [pnodeFactory(i, args, sc, rnd, rs) for i in range(args.num_nodes)]
        for idx, nd in enumerate(allNodes):
            nd.addNodeInfo([n for i, n in enumerate(allNodes) if i != idx])
    else:
        print("Wrong protocol specified: ", args.protocol)
        return

    for _ in range(args.total_epochs):
        for nd in allNodes:
            pass

if __name__ == "__main__":
    run()
