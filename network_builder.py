from abc import ABC, abstractmethod
from output_strategy import FileOutputStrategy
from link_generator import log_write, DefaultLinkStrategy

from level_connector import *


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


# class SpineLeafConnector(Connector):
#     def __init__(
#         self,
#         link_generator,
#         num_spine_switches,
#         num_leaf_switches,
#         host_per_leaf,
#     ):
#         self.link_generator = link_generator
#         self.num_spine_switches = num_spine_switches
#         self.num_leaf_switches = num_leaf_switches
#         self.host_per_leaf = host_per_leaf

#     @log_write
#     def build_nodes(self, **kwargs):
#         pass

#     @log_write
#     def build_links(self, **kwargs):
#         level0 = FullMeshConnectionLevel(
#             self.link_generator,
#             self.num_spine_switches,
#             self.num_leaf_switches,
#             0,
#         )

#         id = level0.connect(**kwargs)

#         level1 = GroupConnectionLevel(
#             self.link_generator,
#             self.num_leaf_switches,
#             self.num_leaf_switches * self.host_per_leaf,
#             id,
#         )

#         level1.connect(**kwargs)


class FatTreeBuilder(NetworkBuilder):
    def __init__(
        self,
        k=4,
        host_per_edge=3,
        output_strategy=FileOutputStrategy(),
        **kwargs,
    ):
        self.output = output_strategy
        self.link_generator = DefaultLinkStrategy(output_strategy)
        self.num_core_switches = k**2 // 4
        self.num_agg_switches = k**2 // 2
        self.num_edge_switches = k**2 // 2
        self.host_per_edge = host_per_edge
        self.k = k

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
        level0 = FullOverStepConnector(
            self.link_generator,
            self.num_core_switches,
            self.num_agg_switches,
            0,
            self.k,
        )

        id = level0.connect(**kwargs)

        level1 = GroupOverGroupConnector(
            self.link_generator,
            self.num_agg_switches,
            self.num_edge_switches,
            id,
            self.k,
        )

        id = level1.connect(**kwargs)

        level2 = OneOverGroupConnector(
            self.link_generator,
            self.num_edge_switches,
            self.num_edge_switches * self.host_per_edge,
            id,
        )

        level2.connect(**kwargs)

        return f"Links generated.\n"
