from abc import ABC, abstractmethod
from link_generator import log_write


class LevelConnector(ABC):
    def __init__(
        self,
        link_generator,
        higher_level_nodes,
        lower_level_nodes,
        start_id,
    ):
        self.link_generator = link_generator

        self.higher_level_nodes = higher_level_nodes
        self.lower_level_nodes = lower_level_nodes
        self.start_id = start_id

    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def finished(self):
        pass


"""
upper level: connected by all nodes
lower level: connected step by step, step is divided by group
"""


class FullOverStepConnector(LevelConnector):
    def __init__(
        self, link_generator, higher_level_nodes, lower_level_nodes, start_id, group
    ):
        super().__init__(
            link_generator, higher_level_nodes, lower_level_nodes, start_id
        )
        self.group = group

        self.lower_level_nodes_per_group = self.lower_level_nodes // self.group
        self.higher_level_nodes_per_group = (
            self.higher_level_nodes // self.lower_level_nodes_per_group
        )
        self.higher_level_nodes_group = self.lower_level_nodes_per_group

    def connect(self, **kwargs):

        last_id = self.start_id + self.higher_level_nodes

        for higher_node_group in range(self.higher_level_nodes_group):
            for higher_node in range(self.higher_level_nodes_per_group):
                higher_node_index = (
                    self.start_id
                    + higher_node_group * self.higher_level_nodes_per_group
                    + higher_node
                )
                for group in range(self.group):
                    lower_node_index = (
                        last_id
                        + group * self.lower_level_nodes_per_group
                        + higher_node_group
                    )

                    self.link_generator.link(
                        higher_node_index,
                        lower_node_index,
                        **kwargs,
                    )

        self.finished()

        return last_id

    @log_write
    def finished(self):
        return f"Core and Agg links generated.\n"


"""
upper level: connected one by one
lower level: connected group by group
"""


class OneOverGroupConnector(LevelConnector):
    def __init__(
        self,
        link_generator,
        higher_level_nodes,
        lower_level_nodes,
        start_id,
    ):
        super().__init__(
            link_generator, higher_level_nodes, lower_level_nodes, start_id
        )
        self.host_per_leaf = self.lower_level_nodes // self.higher_level_nodes
        self.host_leftover = self.lower_level_nodes % self.higher_level_nodes

    def connect(self, **kwargs):
        start_id = self.start_id
        link_id = self.start_id + self.higher_level_nodes

        for leaf in range(self.higher_level_nodes):
            for host in range(self.host_per_leaf):
                self.link_generator.link(
                    start_id,
                    link_id,
                    **kwargs,
                )
                link_id += 1
            start_id += 1

            self.finished()

        return start_id

    @log_write
    def finished(self):
        return f"Leaf and Host links generated.\n"


"""
upper level: connected group by group
lower level: connected group by group
"""


class GroupOverGroupConnector(LevelConnector):
    def __init__(
        self,
        link_generator,
        higher_level_nodes,
        lower_level_nodes,
        start_id,
        group,
    ):
        super().__init__(
            link_generator, higher_level_nodes, lower_level_nodes, start_id
        )

        self.group = group
        self.higher_level_nodes_per_group = self.higher_level_nodes // self.group
        self.lower_level_nodes_per_group = self.lower_level_nodes // self.group

    def connect(self, **kwargs):
        last_id = self.start_id + self.higher_level_nodes

        for group in range(self.group):
            higher_node_index = (
                self.start_id + group * self.higher_level_nodes_per_group
            )
            for higher_node in range(self.higher_level_nodes_per_group):
                lower_node_index = self.higher_level_nodes + higher_node_index
                for lower_node in range(self.lower_level_nodes_per_group):
                    self.link_generator.link(
                        higher_node_index + higher_node,
                        lower_node_index + lower_node,
                        **kwargs,
                    )

        self.finished()

        return last_id

    @log_write
    def finished(self):
        return f"Spine and Leaf links generated.\n"


class FullMeshConnectionLevel(LevelConnector):
    def __init__(
        self, link_generator, higher_level_nodes, lower_level_nodes, start_id, group=1
    ):
        super().__init__(
            link_generator, higher_level_nodes, lower_level_nodes, start_id, group
        )

    def connect(self, **kwargs):
        last_id = self.start_id + self.higher_level_nodes

        for group in range(self.group):
            higher_node_index = (
                self.start_id + group * self.higher_level_nodes_per_group
            )
            for higher_node in range(self.higher_level_nodes_per_group):
                lower_node_index = self.higher_level_nodes + higher_node_index
                for lower_node in range(self.lower_level_nodes_per_group):
                    self.link_generator.link(
                        higher_node_index + higher_node,
                        lower_node_index + lower_node,
                        **kwargs,
                    )

        self.finished()

        return last_id

    @log_write
    def finished(self):
        return f"Spine and Leaf links generated.\n"
