from abc import ABC, abstractmethod
from logger import log_write


"""
LevelConnector is the abstraction for connecting nodes in different levels of the topology.
The abstract method connect will connect the nodes between the levels.

We can implement different connection strategies for different topologies.
"""


class LevelConnector(ABC):
    def __init__(
        self,
        link_strategy,
        higher_level_nodes,
        lower_level_nodes,
        start_id,
        **kwargs,
    ):
        self.link_strategy = link_strategy
        self.higher_level_nodes = higher_level_nodes
        self.lower_level_nodes = lower_level_nodes
        self.start_id = start_id
        self.kwargs = kwargs

    def __del__(self):
        self.final_info()

    """
    This method is the connection logic for the nodes between two levels.
    It will return the first index of the lower level nodes for the next level connection.
    """

    @abstractmethod
    def connect(self):
        pass

    @log_write
    def final_info(self):
        name = self.__class__.__name__
        return f"{name} level connected.\n"

    """
    This method is for method chaining.
    """

    def connectTo(self, cls, next_level_nodes, group=1):
        next_id = self.connect()
        typeof = cls.__name__

        instance = cls(
            self.link_strategy,
            self.lower_level_nodes,
            next_level_nodes,
            next_id,
            group,
            **self.kwargs,
        )

        return instance

    @staticmethod
    def START(link_strategy, nodes, **kwargs):
        return BaseConnector(
            link_strategy,
            nodes,
            **kwargs,
        )

    def END(self):
        self.connect()


"""
This class is used for method chaining.
Do not use this class directly.
"""


class BaseConnector(LevelConnector):
    def __init__(
        self,
        link_strategy,
        nodes,
        **kwargs,
    ):
        super().__init__(link_strategy, nodes, nodes, 0, **kwargs)

    def connect(self):
        return 0


"""
upper level: connected by all nodes
lower level: connected step by step, step is divided by group
"""


class OneOverStepConnector(LevelConnector):
    def __init__(
        self,
        link_strategy,
        higher_level_nodes,
        lower_level_nodes,
        start_id,
        group=1,
        **kwargs,
    ):
        super().__init__(
            link_strategy, higher_level_nodes, lower_level_nodes, start_id, **kwargs
        )
        self.group = group

        self.lower_level_nodes_per_group = self.lower_level_nodes // self.group
        self.higher_level_nodes_per_group = (
            self.higher_level_nodes // self.lower_level_nodes_per_group
        )
        self.higher_level_nodes_group = self.lower_level_nodes_per_group

    def connect(self):

        lower_level_first_index = self.start_id + self.higher_level_nodes

        for higher_node_group in range(self.higher_level_nodes_group):
            for higher_node in range(self.higher_level_nodes_per_group):
                higher_node_index = (
                    self.start_id
                    + higher_node_group * self.higher_level_nodes_per_group
                    + higher_node
                )
                for group in range(self.group):
                    lower_node_index = (
                        lower_level_first_index
                        + group * self.lower_level_nodes_per_group
                        + higher_node_group
                    )

                    self.link_strategy.link(
                        higher_node_index,
                        lower_node_index,
                        **self.kwargs,
                    )

        return lower_level_first_index


"""
upper level: connected one by one
lower level: connected group by group
"""


class OneOverGroupConnector(LevelConnector):
    def __init__(
        self,
        link_strategy,
        higher_level_nodes,
        lower_level_nodes,
        start_id,
        group=1,
        **kwargs,
    ):
        super().__init__(
            link_strategy, higher_level_nodes, lower_level_nodes, start_id, **kwargs
        )
        self.host_per_leaf = self.lower_level_nodes // self.higher_level_nodes
        self.host_leftover = self.lower_level_nodes % self.higher_level_nodes

    def connect(self):
        lower_level_first_index = self.start_id + self.higher_level_nodes

        for higher_node in range(self.higher_level_nodes):
            higher_node_index = self.start_id + higher_node
            for lower_node in range(self.host_per_leaf):
                lower_node_index = (
                    lower_level_first_index
                    + higher_node * self.host_per_leaf
                    + lower_node
                )
                self.link_strategy.link(
                    higher_node_index,
                    lower_node_index,
                    **self.kwargs,
                )

        return lower_level_first_index


"""
upper level: connected group by group
lower level: connected group by group
"""


class GroupOverGroupConnector(LevelConnector):
    def __init__(
        self,
        link_strategy,
        higher_level_nodes,
        lower_level_nodes,
        start_id,
        group=1,
        **kwargs,
    ):
        super().__init__(
            link_strategy, higher_level_nodes, lower_level_nodes, start_id, **kwargs
        )

        self.group = group
        self.higher_level_nodes_per_group = self.higher_level_nodes // self.group
        self.lower_level_nodes_per_group = self.lower_level_nodes // self.group

    def connect(self):
        lower_level_first_index = self.start_id + self.higher_level_nodes

        for group in range(self.group):
            higher_node_index = (
                self.start_id + group * self.higher_level_nodes_per_group
            )
            for higher_node in range(self.higher_level_nodes_per_group):
                lower_node_index = self.higher_level_nodes + higher_node_index
                for lower_node in range(self.lower_level_nodes_per_group):
                    self.link_strategy.link(
                        higher_node_index + higher_node,
                        lower_node_index + lower_node,
                        **self.kwargs,
                    )

        return lower_level_first_index


"""
upper level: connected all nodes
lower level: connected all nodes
"""


class FullMeshConnector(LevelConnector):
    def __init__(
        self,
        link_strategy,
        higher_level_nodes,
        lower_level_nodes,
        start_id,
        group=1,
        **kwargs,
    ):
        super().__init__(
            link_strategy, higher_level_nodes, lower_level_nodes, start_id, **kwargs
        )

    def connect(self):
        lower_level_first_index = self.start_id + self.higher_level_nodes

        for higher_node in range(self.higher_level_nodes):
            higher_node_index = self.start_id + higher_node
            for lower_node in range(self.lower_level_nodes):
                lower_node_index = lower_level_first_index + lower_node
                self.link_strategy.link(
                    higher_node_index,
                    lower_node_index,
                    **self.kwargs,
                )

        return lower_level_first_index


"""
upper level: connected group by group
lower level: connected one by one
"""


class GroupOverOneConnector(LevelConnector):
    def __init__(
        self,
        link_strategy,
        higher_level_nodes,
        lower_level_nodes,
        start_id,
        group=1,
        **kwargs,
    ):
        super().__init__(
            link_strategy, higher_level_nodes, lower_level_nodes, start_id, **kwargs
        )
        self.group = group
        self.higher_level_nodes_per_group = self.higher_level_nodes // self.group

    def connect(self):
        lower_level_first_index = self.start_id + self.higher_level_nodes

        for group in range(self.group):
            for higher_node in range(self.higher_level_nodes_per_group):
                higher_node_index = (
                    self.start_id
                    + group * self.higher_level_nodes_per_group
                    + higher_node
                )
                lower_node_index = lower_level_first_index + group
                self.link_strategy.link(
                    higher_node_index,
                    lower_node_index,
                    **self.kwargs,
                )

        return lower_level_first_index
