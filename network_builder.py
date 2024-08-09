from abc import ABC, abstractmethod
from output_strategy import FileOutputStrategy
from link_strategy import *

from level_connector import *

"""
NetworkBuilder is an abstract class that defines the methods that will be used to build the topology.
It will direct the construction of the whole topology.

The construct method will build the nodes, switches, and links by combining the LevelConnector.
It also in charge of building the flows via FlowStrategy.
"""


class NetworkBuilder(ABC):
    @abstractmethod
    def construct(self, **kwargs):
        pass

    @abstractmethod
    def build_nodes(self, **kwargs):
        pass

    @abstractmethod
    def build_switches(self, **kwargs):
        pass

    @abstractmethod
    def build_links(self, **kwargs):
        pass

    def build_flow(self, **kwargs):
        pass

    def build_flow_header(self, **kwargs):
        pass


"""
SpineLeafBuilder will build a Spine-Leaf topology.
We can specify the number of spine switches, leaf switches, and hosts per leaf to generate the topology.
"""


class SpineLeafBuilder(NetworkBuilder):
    def __init__(self, link_strategy, spine=2, leaf=3, host_per_leaf=3, **kwargs):
        self.output = link_strategy.get_output()
        self.link_strategy = link_strategy
        self.num_spine_switches = spine
        self.num_leaf_switches = leaf
        self.host_per_leaf = host_per_leaf
        self.kwargs = kwargs

    @log_write
    def construct(self, **kwargs):
        self.build_nodes()
        self.build_switches()
        self.build_links(**kwargs)
        return f"Spine-Leaf topology generated.\n"

    @log_write
    def build_nodes(self, **kwargs):
        total_switches = self.num_spine_switches + self.num_leaf_switches
        total_hosts = self.num_leaf_switches * self.host_per_leaf

        total_nodes = total_switches + total_hosts

        self.output.write(f"{total_nodes} {total_switches} {total_hosts}\n")

        return f"Total nodes: {total_nodes}, Total switches: {total_switches}, Total hosts: {total_hosts}\n"

    @log_write
    def build_switches(self, **kwargs):
        total_switches = self.num_spine_switches + self.num_leaf_switches

        for switch in range(total_switches):
            self.output.write(f"{switch} ")

        self.output.write("\n")

        return f"Switches generated.\n"

    @log_write
    def build_links(self, **kwargs):
        LevelConnector.START(
            self.link_strategy,
            self.num_spine_switches,
            **kwargs,
        ).connectTo(
            FullMeshConnector,
            self.num_leaf_switches,
        ).connectTo(
            OneOverGroupConnector,
            self.num_leaf_switches * self.host_per_leaf,
        ).END()

        return f"Spine leaf links generated.\n"


"""
FatTreeBuilder will build a Fat-Tree topology.
We can specify the number of k, which is the number of switches per pod,
and host per edge switches to generate the topology.
"""


class FatTreeBuilder(NetworkBuilder):
    def __init__(
        self,
        link_strategy,
        k=4,
        host_per_edge=3,
        **kwargs,
    ):
        self.output = link_strategy.get_output()
        self.link_strategy = link_strategy
        self.num_core_switches = k**2 // 4
        self.num_agg_switches = k**2 // 2
        self.num_edge_switches = k**2 // 2
        self.host_per_edge = host_per_edge
        self.k = k
        self.kwargs = kwargs

    @log_write
    def construct(self, **kwargs):
        self.build_nodes()
        self.build_switches()
        self.build_links(**kwargs)
        return f"Fat Tree topology generated.\n"

    @log_write
    def build_nodes(self, **kwargs):
        total_switches = (
            self.num_core_switches + self.num_agg_switches + self.num_edge_switches
        )
        total_hosts = self.num_edge_switches * self.host_per_edge

        total_nodes = total_switches + total_hosts

        self.output.write(f"{total_nodes} {total_switches} {total_hosts}\n")

        return f"Total nodes: {total_nodes}, Total switches: {total_switches}, Total hosts: {total_hosts}\n"

    @log_write
    def build_switches(self, **kwargs):
        total_switches = (
            self.num_core_switches + self.num_agg_switches + self.num_edge_switches
        )

        for switch in range(total_switches):
            self.output.write(f"{switch} ")

        self.output.write("\n")

        return f"Switches generated.\n"

    @log_write
    def build_links(self, **kwargs):
        LevelConnector.START(
            self.link_strategy,
            self.num_core_switches,
            **kwargs,
        ).connectTo(
            OneOverStepConnector,
            self.num_agg_switches,
            self.k,
        ).connectTo(
            GroupOverGroupConnector,
            self.num_edge_switches,
            self.k,
        ).connectTo(
            OneOverGroupConnector,
            self.num_edge_switches * self.host_per_edge,
        ).END()

        return f"Links generated.\n"


"""
BCubeBuilder will build a BCube topology.
We can specify the number of n, which is the number of switches per level to generate the topology,
to generate the topology.
"""


class BCubeBuilder(NetworkBuilder):
    def __init__(self, link_strategy, n=4, **kwargs):
        self.output = link_strategy.get_output()
        self.link_strategy = link_strategy
        self.n = n
        self.kwargs = kwargs

        self.one_level_switches = n
        self.total_switches = n * 2
        self.total_hosts = n**2

    @log_write
    def construct(self, **kwargs):
        self.build_nodes()
        self.build_switches()
        self.build_links(**kwargs)
        return f"BCube topology generated.\n"

    @log_write
    def build_nodes(self, **kwargs):
        total_switches = self.n * 2
        total_hosts = self.n**2

        total_nodes = total_switches + total_hosts

        self.output.write(f"{total_nodes} {total_switches} {total_hosts}\n")

        return f"Total nodes: {total_nodes}, Total switches: {total_switches}, Total hosts: {total_hosts}\n"

    @log_write
    def build_switches(self, **kwargs):
        top_level_switches = self.n
        total_hosts = self.n**2
        bottom_level_switches = self.n

        top_and_hosts = top_level_switches + total_hosts
        total_nodes = top_and_hosts + bottom_level_switches

        for switch in range(top_level_switches):
            self.output.write(f"{switch} ")

        for switch in range(top_and_hosts, total_nodes):
            self.output.write(f"{switch} ")

        self.output.write("\n")

        return f"Switches generated.\n"

    @log_write
    def build_links(self, **kwargs):
        LevelConnector.START(
            self.link_strategy,
            self.one_level_switches,
            **kwargs,
        ).connectTo(
            OneOverStepConnector,
            self.total_hosts,
            self.n,
        ).connectTo(
            GroupOverOneConnector,
            self.one_level_switches,
            self.n,
        ).END()
        return f"Links generated.\n"
