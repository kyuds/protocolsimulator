# library imports
import argparse
import numpy as np

# custom imports
from statcollector import StatCollector
from pot import PNode, pnodeFactory

def run():
    # parse arguments
    parser = argparse.ArgumentParser(description="Settings for Protocol Simulator")
    parser.add_argument("--num-nodes", default=10, type=int, help="Number of nodes")
    parser.add_argument("--protocol", default="chord", type=str, help="Type of protocol: chord/pot")
    parser.add_argument("--latency", default=10, type=int, help="Network latency (in ms)")
    parser.add_argument("--capacity", default=100, type=int, help="Object capacity")
    parser.add_argument("--fill-factor", default=0.7, type=float, help="Factor of memory fill achieved before eviction")
    parser.add_argument("--retrieval-factor", default=0.2, type=float, help="Probability of object restore")
    args = parser.parse_args()

    if args.protocol == "chord":
        pass
    elif args.protocol == "pot":
        # initialize a single random generator for POT decision making.
        rnd = np.random.default_rng(12345)
        sc = StatCollector(args.latency)
        allNodes = [pnodeFactory(i, args, sc, rnd) for i in range(args.num_nodes)]
        for idx, nd in enumerate(allNodes):
            nd.addNodeInfo([n for i, n in enumerate(allNodes) if i != idx])
    else:
        print("Wrong protocol specified: ", args.protocol)
        return

if __name__ == "__main__":
    run()
