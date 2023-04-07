import argparse
import numpy as np

from pot import PNode
from chord import CNode
from utils import Rnd

def simulate(args):
    nodes, rnd, sc = [], Rnd(0), None

    # setup nodes based on simulation type
    if args.protocol == "chord": 
        for id in range(args.num_nodes):
            nodes.append(CNode(id, args.capacity, args.threshold, sc, rnd))
        # create ID circle

    elif args.protocol == "pot":
        for id in range(args.num_nodes):
            nodes.append(PNode(id, args.capacity, args.threshold, sc, rnd))

        # add all nodes info to each node
    else:
        print("Simulation name not supported.")
        return

    for ep in range(args.total_epochs):
        for n in nodes:
            n.run()
        if ep != 0 and ep % args.oscillate_period == 0:
            for n in nodes:
                n.shuffle()

if __name__=="__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description="Settings for Protocol Simulator")
    parser.add_argument("--num-nodes", default=50, type=int, help="Number of nodes")
    parser.add_argument("--protocol", default="chord", type=str, help="Type of protocol: chord/pot")
    parser.add_argument("--capacity", default=100, type=int, help="Object capacity")
    parser.add_argument("--threshold", default=0.9, type=float, help="Max memory fill before remote spill")
    parser.add_argument("--oscillate-period", default=10, type=float, help="Memory state change period")
    parser.add_argument("--total-epochs", default=1000, type=float, help="Total number of epochs to simulate")

    simulate(parser.parse_args())
