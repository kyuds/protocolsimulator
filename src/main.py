# library imports
import argparse
import numpy as np
import random

# class imports
import chord
import pot

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
    nn = args.num_nodes

    # setup for protocol type
    if args.protocol == "chord":
        sc = StatCollector(args.latency)
        allNodes = [cnodeFactory(i, args, sc, rs) for i in range(nn)]
        # add other node info that is necessary... idk how to initialize

        # for now assume identifier circle has length 2nn
        idCircle = [0]*nn
        nodeIDs = random_combinations(range(2 * nn), nn) # returns random list of indices for the nn nodes
        for i in range(nn):
            currentNode = chord.CNode(nodeIDs[i], args.capacity, args.fill_factor,
                                      args.retrieval_factor, sc, rs) # create chord instance with unique id
            idCircle[nodeIDs[i]] = currentNode
        
        # iterate through idCircle and set successors of every node
        currNode = 0
        for i in range(len(idCircle)):
            if idCircle[i] != 0 and currNode == 0:
                currNode = idCircle[i]
            elif idCircle[i] != 0 and currNode != 0:
                # currNode.ftable.get(endpoints[i])
                # update fingertable dictionary's 3rd entry in list to successor (i.e. idCircle[i])
                pass


        
            


    elif args.protocol == "pot":
        # initialize a single random generator for POT decision making.
        rnd = np.random.default_rng(12345)
        sc = StatCollector(args.latency)
        allNodes = [pnodeFactory(i, args, sc, rnd, rs) for i in range(nn)]
        for idx, nd in enumerate(allNodes):
            nd.addNodeInfo([n for i, n in enumerate(allNodes) if i != idx])
    else:
        print("Unknown protocol specified: ", args.protocol)
        return

    # run simulation
    for epc in range(args.total_epochs):
        for nd in allNodes:
            nd.run()
        if epc != 0 and epc % op == 0:
            for nd in allNodes:
                nd.oscillate()
    
    # log statistics 
    sc.logStats()

# CHORD: helper function for randomly picking ids for identifier circle
# id_length = [0, length of identifier circle]
# num_nodes = # of nodes
def random_combinations(id_length, num_nodes):
    idCircle = list(id_length)
    n = len(id_length)
    random_indices = random.sample(range(n), num_nodes)
    return list(idCircle[i] for i in random_indices)

if __name__ == "__main__":
    run()
