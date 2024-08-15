import argparse
import network_builder
import link_strategy
import output_strategy
import flow_strategy
import os
import glob
from datetime import datetime

"""
File names
"""

TOPO_FILENAME = "topology.txt"
FLOW_FILENAME = "flow.txt"

"""
Spine-Leaf topology parameters
"""

SPINE_SWITCHES = 2
LEAF_SWITCHES = 3
HOSTS_PER_LEAF = 3

"""
Fat-Tree topology parameters
"""

FAT_TREE_K = 4
FAT_TREE_HOST_PER_EDGE = 3

"""
BCube topology parameters
"""


BCUBE_N = 4

"""
Other parameters
"""


SWITCH_TO_SWITCH_BANDWIDTH = "100Gbps"
SWITCH_TO_SWITCH_DELAY = "0.001ms"
SWITCH_TO_SWITCH_ERROR_RATE = "0"
SWITCH_TO_HOST_BANDWIDTH = "100Gbps"
SWITCH_TO_HOST_DELAY = "0.001ms"
SWITCH_TO_HOST_ERROR_RATE = "0"


def generate_spine_leaf(
    link,
    flow,
    spine=SPINE_SWITCHES,
    leaf=LEAF_SWITCHES,
    host=HOSTS_PER_LEAF,
):

    network_builder.SpineLeafBuilder(link, flow, spine, leaf, host).construct(
        bandwidth="100Gbps",
        delay="0.001ms",
        error_rate="0",
        payload=1024,
        initial_time=0,
        pfc_priority=1,
        port=100,
    )


def generate_fat_tree(
    link,
    flow,
    k=FAT_TREE_K,
    host=FAT_TREE_HOST_PER_EDGE,
):

    network_builder.FatTreeBuilder(link, flow, k, host).construct(
        bandwidth="100Gbps",
        delay="0.001ms",
        error_rate="0",
        payload=1024,
        initial_time=0,
        pfc_priority=1,
        port=100,
    )


def generate_bcube(
    link,
    flow,
    n=BCUBE_N,
):

    network_builder.BCubeBuilder(link, flow, n).construct(
        bandwidth="100Gbps",
        delay="0.001ms",
        error_rate="0",
        payload=1024,
        initial_time=0,
        pfc_priority=1,
        port=100,
    )


def clean_files():
    txt_files = glob.glob("*.txt")
    try:
        for f in txt_files:
            os.remove(f)
    except:
        print("Error while deleting files.")


if __name__ == "__main__":

    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    topo_file = f"topology_{current_time}.txt"
    flow_file = f"flow_{current_time}.txt"

    parser = argparse.ArgumentParser(
        description="Generate topology and flow files for network simulation."
    )
    parser.add_argument(
        "-t",
        "--topology",
        type=str,
        default="spine_leaf",
        choices=["spine_leaf", "fat_tree", "bcube"],
        help="Topology to generate.",
    )
    parser.add_argument(
        "-tf",
        "--topo_file",
        type=str,
        default=topo_file,
        help="Output file for topology.",
    )
    parser.add_argument(
        "-ff",
        "--flow_file",
        type=str,
        default=flow_file,
        help="Output file for flow.",
    )

    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="Clean up output files before generating.",
    )
    parser.add_argument(
        "--spine",
        type=int,
        default=SPINE_SWITCHES,
        help="Number of spine switches.",
    )
    parser.add_argument(
        "--leaf",
        type=int,
        default=LEAF_SWITCHES,
        help="Number of leaf switches.",
    )
    parser.add_argument(
        "--host",
        type=int,
        default=HOSTS_PER_LEAF,
        help="Number of hosts per leaf switch.",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=FAT_TREE_K,
        help="Fat-Tree parameter k.",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=BCUBE_N,
        help="BCube parameter n.",
    )

    args = parser.parse_args()

    if args.clean:
        clean_files()
        exit()

    print(f"Generating {args.topology} topology...")

    topo_file = output_strategy.FileOutputStrategy(args.topo_file)
    flow_file = output_strategy.FileOutputStrategy(args.flow_file)
    flow = flow_strategy.DefaultFlowStrategy(flow_file)
    link = link_strategy.DefaultLinkStrategy(topo_file)

    if args.topology == "spine_leaf":
        generate_spine_leaf(link, flow, args.spine, args.leaf, args.host)
    elif args.topology == "fat_tree":
        generate_fat_tree(link, flow, args.k, args.host)
    elif args.topology == "bcube":
        generate_bcube(link, flow, args.n)
    else:
        print("Invalid topology.")
