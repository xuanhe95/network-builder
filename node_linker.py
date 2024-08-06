from logger import log_write
from abc import ABC, abstractmethod
import output_strategy
import flow_strategy


class NodeLinker(ABC):
    def __init__(
        self,
        output,
        flow_strategy,
    ):
        self.output = output
        self.flow_strategy = flow_strategy

    @abstractmethod
    def link(self, **kwargs):
        pass

    def get_output(self):
        return self.output


class DefaultNodeLinker(NodeLinker):

    @log_write
    def link(self, src, dst, **kwargs):
        bandwidth = kwargs.get("bandwidth", "10Gbps")
        delay = kwargs.get("delay", "0ms")
        error_rate = kwargs.get("error_rate", 0)

        output = f"{src} {dst} {bandwidth} {delay} {error_rate}\n"

        self.output.write(output)

        self.create_flow(src, dst, **kwargs)

        return f"Connected {src} to {dst} with {bandwidth} bandwidth, {delay} delay, and {error_rate} error rate.\n"

    def create_flow(self, src, dst, **kwargs):
        return self.flow_strategy.next(src, dst, **kwargs)


class HalfNodeLinker(NodeLinker):

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

        bandwidth = kwargs.get("bandwidth", "10Gbps")
        delay = kwargs.get("delay", "0ms")
        error_rate = kwargs.get("error_rate", 0)

        if self.id % 2 == 0:
            error_rate = 0.5
            delay = "10ms"
            bandwidth = "5Gbps"
        self.id += 1

        output = f"{src} {dst} {bandwidth} {delay} {error_rate}\n"

        self.output.write(output)

        self.create_flow(src, dst, **kwargs)

        return f"Connected {src} to {dst} with {bandwidth} bandwidth, {delay} delay, and {error_rate} error rate.\n"

    def create_flow(self, src, dst, **kwargs):
        return self.flow_strategy.next(src, dst, **kwargs)
