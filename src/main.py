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

        # for now assume identifier circle has length (smallest power of 2 greater than 2nn)
        circleLength, m = idCircleLength(nn)
        idCircle = [0]*circleLength
        nodeIDs = random_combinations(range(2 * nn), nn) # returns random list of indices for the nn nodes
        for i in range(nn):
            currentNode = chord.CNode(nodeIDs[i], args.capacity, args.fill_factor,
                                      args.retrieval_factor, sc, rs, m) # create chord instance with unique id
            idCircle[nodeIDs[i]] = currentNode
        
        # iterate through idCircle and set successors of every node (along with predecessor)
        # iteration starts from index 0
        currNode = 0
        startingNode = 0
        for i in range(len(idCircle)):
            if idCircle[i] != 0 and currNode == 0:
                startingNode = idCircle[i]
                currNode = idCircle[i]
            elif idCircle[i] != 0 and currNode != 0:
                currNode.successor = idCircle[i]
                idCircle[i].predecessor = currNode
                currNode = idCircle[i]
        # setting last node's successor/predecessor in the circle
        currNode.successor = startingNode
        startingNode.predecessor = currNode

        # CHORD TODO: set finger[k].node for every node's finger table

        # currNode.ftable.get(endpoints[i]) -> can't directly access endpoints[i]
        # update fingertable dictionary's 3rd entry in list to successor (i.e. idCircle[i])

        # CHORD TODO: set fill factor, retrieval factor, etc. (features for chord class)
        # CHORD TODO: spilling to another node
        # -> How to select which node to spill? (Need to conceptually understand how chord exactly works)

        # CHORD maybe TODO:
        # find_successor, find_predecessor, closest_preceding_finger (i.e. node n receives query to find a random id's succ/predecessor)

        # TODO: stat collector
        # -> How does timing work for retrievals and everything?


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

# CHORD: helper function to find smallest power of 2 that is greater than 2 * nn
# po2 = size of id circle
# m = # of bits to represent size of circle -> i.e. log(po2)
def idCircleLength(num_nodes):
    circleLength = 2*num_nodes
    po2 = 1
    m = 0
    while po2 < circleLength:
        po2 = po2 * 2
        m += 1
    return po2, m

if __name__ == "__main__":
    run()
