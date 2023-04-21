import argparse
import numpy as np

from pot import PNode
from chord import CNode
from utils import Rnd
from statcollector import StatCollector

# Class imports
import chord
import pot

def simulate(args):
    nodes, rnd, sc = [], Rnd(0), StatCollector()

    # setup nodes based on simulation type
    if args.protocol == "chord": 
        for id in range(args.num_nodes):
            nodes.append(CNode(id, args.capacity, args.threshold, rnd))
        
        # create ID circle
        IDCircle = chord.idCircle(nodes)

        # setup finger table
        for node in nodes:
            node.setFingerTable(IDCircle)

    elif args.protocol == "pot":
        prnd = Rnd(2)
        for id in range(args.num_nodes):
            pnode = PNode(id, args.capacity, args.threshold, rnd, prnd)
            nodes.append(pnode)
        
        for id in range(args.num_nodes):
            tmp = nodes.pop(id)
            tmp.addNodes(nodes)
            nodes.insert(id, tmp)
    else:
        print("Simulation name not supported.")
        return

    for _ in range(100):
        for n in nodes:
            n.shuffle()
            if n.numObjects > int(1.5 * args.capacity):
                n.numObjects = int(1.5 * args.capacity)

    for ep in range(args.total_epochs):
        unbalanced = True
        while unbalanced:
            unbalanced = False
            for n in nodes:
                if n.needToSpill():
                    unbalanced = True
                    n.run(args.verbose)
        
        sc.addEntry(ep)
        for n in nodes:
            sc.addQueryTime(n)
            sc.nodeSpilledToDisk(n)
            sc.addMemoryUsage(n)
            n.resetStats()
        
        for n in nodes:
            n.shuffle()
    
    sc.printStats()
    sc.generateMemoryGraph(args.protocol)

if __name__=="__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description="Settings for Protocol Simulator")
    parser.add_argument("--num-nodes", default=3000, type=int, help="Number of nodes")
    parser.add_argument("--protocol", default="pot", type=str, help="Type of protocol: chord/pot")
    parser.add_argument("--capacity", default=100, type=int, help="Object capacity")
    parser.add_argument("--threshold", default=0.9, type=float, help="Max memory fill before remote spill")
    parser.add_argument("--total-epochs", default=10, type=float, help="Total number of epochs to simulate")
    parser.add_argument("--verbose", default=False, type=bool, help="Log queries")

    simulate(parser.parse_args())
