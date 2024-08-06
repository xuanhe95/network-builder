import argparse
from datetime import datetime
from network_builder import FatTreeBuilder


SPINE_SWITCHES = 2
LEAF_SWITCHES = 3
HOSTS_PER_LEAF = 3
FILENAME = "topology.txt"
SWITCH_TO_SWITCH_BANDWIDTH = "100Gbps"
SWITCH_TO_SWITCH_DELAY = "0.001ms"
SWITCH_TO_SWITCH_ERROR_RATE = "0"
SWITCH_TO_HOST_BANDWIDTH = "100Gbps"
SWITCH_TO_HOST_DELAY = "0.001ms"
SWITCH_TO_HOST_ERROR_RATE = "0"


def generate_switches(f, total_switches):
    output = ""
    for i in range(total_switches):
        output += f"{i} "
    output += "\n"
    f.write(output)
    return f"Switches: {output}"


def generate_fat_file():
    FatTreeBuilder(
        6, bandwidth="100Gbps", delay="0.001ms", error_rate="0"
    ).link_construct()
    FatTreeBuilder(6, bandwidth="100Gbps", delay="0.001ms", error_rate="0").construct()


if __name__ == "__main__":

    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    default_filename = f"topology_{current_time}.txt"

    parser = argparse.ArgumentParser(
        description="Generate a Leaf-Spine topology file for NS3."
    )
    parser.add_argument(
        "-s",
        "--spine",
        type=int,
        default=SPINE_SWITCHES,
        help="Number of spine switches",
    )
    parser.add_argument(
        "-l", "--leaf", type=int, default=LEAF_SWITCHES, help="Number of leaf switches"
    )
    parser.add_argument(
        "-n",
        "--host",
        type=int,
        default=HOSTS_PER_LEAF,
        help="Number of hosts per leaf switch",
    )
    parser.add_argument(
        "-f",
        "--filename",
        type=str,
        default=FILENAME,
        help="Output filename prefix",
    )
    parser.add_argument(
        "-ssb",
        "--switch_to_switch_bandwidth",
        type=str,
        default=SWITCH_TO_SWITCH_BANDWIDTH,
        help="Bandwidth between switches",
    )
    parser.add_argument(
        "-ssd",
        "--switch_to_switch_delay",
        type=str,
        default=SWITCH_TO_SWITCH_DELAY,
        help="Delay between switches",
    )
    parser.add_argument(
        "-sse",
        "--switch_to_switch_error_rate",
        type=str,
        default=SWITCH_TO_SWITCH_ERROR_RATE,
        help="Error rate between switches",
    )
    parser.add_argument(
        "-shb",
        "--switch_to_host_bandwidth",
        type=str,
        default=SWITCH_TO_HOST_BANDWIDTH,
        help="Bandwidth between switch and host",
    )
    parser.add_argument(
        "-shd",
        "--switch_to_host_delay",
        type=str,
        default=SWITCH_TO_HOST_DELAY,
        help="Delay between switch and host",
    )
    parser.add_argument(
        "-she",
        "--switch_to_host_error_rate",
        type=str,
        default=SWITCH_TO_HOST_ERROR_RATE,
        help="Error rate between switch and host",
    )

    args = parser.parse_args()

    # generate_topology_file(
    #     args.spine,
    #     args.leaf,
    #     args.host,
    #     args.filename,
    #     args.switch_to_switch_bandwidth,
    #     args.switch_to_switch_delay,
    #     args.switch_to_switch_error_rate,
    #     args.switch_to_host_bandwidth,
    #     args.switch_to_host_delay,
    #     args.switch_to_host_error_rate,
    # )

    generate_fat_file()
