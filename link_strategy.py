from logger import *
from abc import ABC, abstractmethod

"""
LinkStrategy is the abstraction for creating links between two nodes.
The link method will create a link relation between src and dst nodes.
"""


class LinkStrategy(ABC):
    def __init__(
        self,
        output,
    ):
        self.output = output

    @abstractmethod
    def link(self, **kwargs):
        pass

    def get_output(self):
        return self.output


"""
DefaultLinkStrategy is the default strategy for creating links between nodes.
It will create a link with the given bandwidth, delay, and error rate.
"""


class DefaultLinkStrategy(LinkStrategy):

    @log_write
    def link(self, src, dst, **kwargs):
        bandwidth = kwargs.get("bandwidth", "0Gbps")
        delay = kwargs.get("delay", "0ms")
        error_rate = kwargs.get("error_rate", 0)

        output = f"{src} {dst} {bandwidth} {delay} {error_rate}\n"

        self.output.write(output)

        return f"Connected {src} to {dst} with {bandwidth} bandwidth, {delay} delay, and {error_rate} error rate.\n"


class HalfLinkStrategy(LinkStrategy):

    def __init__(
        self,
        output,
        flow_strategy,
    ):
        self.output = output
        self.flow_strategy = flow_strategy
        self.id = 0

    @log_write
    def link(self, src, dst, **kwargs):

        bandwidth = kwargs.get("bandwidth", "0Gbps")
        delay = kwargs.get("delay", "0ms")
        error_rate = kwargs.get("error_rate", 0)

        # skip every other link
        if self.id % 2 == 0:
            error_rate = 0.5
            delay = "10ms"
            bandwidth = "5Gbps"
        self.id += 1

        output = f"{src} {dst} {bandwidth} {delay} {error_rate}\n"
        self.output.write(output)

        return f"Connected {src} to {dst} with {bandwidth} bandwidth, {delay} delay, and {error_rate} error rate.\n"
