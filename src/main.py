# library imports
import argparse
import numpy as np # prob wont need this later.
import random

# class imports
import chord
import pot

# custom imports
from statcollector import StatCollector
from pot import pnodeFactory
from chord import cnodeFactory
from utils import Rnd

def run():
    # parse arguments
    parser = argparse.ArgumentParser(description="Settings for Protocol Simulator")
    parser.add_argument("--num-nodes", default=10, type=int, help="Number of nodes")
    parser.add_argument("--protocol", default="chord", type=str, help="Type of protocol: chord/pot")
    parser.add_argument("--latency", default=10, type=int, help="Network latency (in ms)")
    parser.add_argument("--capacity", default=100, type=int, help="Object capacity")
    parser.add_argument("--fill-factor", default=0.7, type=float, help="Factor of memory fill achieved before eviction")
    parser.add_argument("--restore-period", default=0.2, type=float, help="Probability of object restore")
    parser.add_argument("--oscillate-period", default=10, type=float, help="Memory state change period")
    parser.add_argument("--total-epochs", default=1000, type=float, help="Total number of epochs to simulate")
    args = parser.parse_args()

    # settings
    op = args.oscillate_period
    mrnd = Rnd(1000)
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
        nodesList = []
        for i in range(len(idCircle)):
            if idCircle[i] != 0 and currNode == 0:
                startingNode = idCircle[i]
                currNode = idCircle[i]
                nodesList.append(idCircle[i])
            elif idCircle[i] != 0 and currNode != 0:
                currNode.successor = idCircle[i]
                idCircle[i].predecessor = currNode
                currNode = idCircle[i]
                nodesList.append(idCircle[i])

        # setting last node's successor/predecessor in the circle
        currNode.successor = startingNode
        startingNode.predecessor = currNode

        # CHORD TODO: set finger[k].node for every node's finger table
        # I think there should be a more efficient way of doing it but for now I leave it as is
        # 
        # nodeIdList = [i.id for i in nodesList]
        # for node in nodesList:
        #     # possible minor improvement: set node.ftable[0][2] = node.successor (for slight improvement in performance)
        #     for interval in node.ftable:
        #         i = interval[0]
        #         start = interval[0] - 1
        #         while (i % circleLength != start):
        #             # probably can optimize further by checking if nextNode's id is within other intervals as well
        #             if i in nodeIdList:
        #                 nextNode = nodesList[nodeIdList.index(i)]
        #                 interval.append(nextNode)
        #                 break
        #             i += 1
                # not taking into account edge case where there's only 1 node in the entire system
        
        # Spill attempt
        ts = 1 # ts = timestep
        while True:
            for node in nodesList: # TODO: replace nodesList with [(node receiving query), (node's first row successor), ... , (node's last row successor)]
                if t % 10 == 0:
                    memoryRandomize(nodesList) # TODO: memoryRandomize is the same as oscillate()?
                res, t = tryToSpill(node, ts)
                if res:
                    break
            print(f"spilling locally")
            return


        # CHORD TODO: set fill factor, retrieval factor, etc. (features for chord class)

        # TODO: stat collector
        # -> How does timing work for retrievals and everything?


    elif args.protocol == "pot":
        # initialize a single random generator for POT decision making.
        prnd = Rnd(12345)
        sc = StatCollector(args.latency)
        allNodes = [pnodeFactory(i, args, sc, prnd, mrnd) for i in range(nn)]
        for idx, nd in enumerate(allNodes):
            nd.addNodeInfo([n for i, n in enumerate(allNodes) if i != idx])
    else:
        print("Unknown protocol specified: ", args.protocol)
        return

    # run simulation
    for epc in range(args.total_epochs):
        sc.addNewEntry()
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

# CHORD: helper function to query a node for the closest finger preceding id
# node = node that receives query
# id = id that the query is requesting the closest preceding finger of
# m = number of bits to represent identifier circle
def closest_preceding_finger(node, id, m):
    int = [i for i in range(node + 1, id)] # check possible off by one error in id
    for i in range(m, -1, -1):
        if node.ftable[i][2].id in int:
            return node.ftable[i][2]
    return node

# CHORD: helper function to query a node for predecessor of id
def find_predecessor(node, id, m):
    pointer = node
    int = [i for i in range(node.id, node.successor.id)]
    while id not in int:
        pointer = closest_preceding_finger(pointer, id, m)
    return pointer

# CHORD: helper function to query for successor of id
def find_successor(node, id, m):
    previous = find_predecessor(node, id, m)
    return previous.successor

# CHORD: helper function for attempting to spill to target node
def tryToSpill(targetnode, time):
    # check if there is enough memory in targetnode to spill
    pass

# CHORD: helper function for re-allocating memory for all nodes -> same as oscillate()?
def memoryRandomize(nodelist):
    # randomize memory capacity for all nodes
    for node in nodelist:
        # do we have a variable to indicate how filled a node is?
        pass

if __name__ == "__main__":
    run()
