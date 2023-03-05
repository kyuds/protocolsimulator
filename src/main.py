import argparse

from node import Node
from statcollector import StatCollector
from chord import chord
from pot import pot

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

    sc = StatCollector()

    def createNode(id, args, sc):
        if args.protocol == "chord":
            p = chord
        else:
            p = pot
        return Node(id, p, args.capacity, args.fill_factor, args.retrieval_factor, sc)
        
    nodes = [createNode(id, args, sc) for id in range(args.num_nodes)]

    # somehow do stuff

if __name__ == "__main__":
    run()
