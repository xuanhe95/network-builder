from abc import ABC, abstractmethod
import random
from logger import log_write

"""
FlowStrategy is the abstraction for creating flows between two nodes.
We can implement different flow strategies for different flow generation logic.
"""


class FlowStrategy(ABC):
    def __init__(self, output):
        self.output = output

    @abstractmethod
    def flow(self, **kwargs):
        pass

    def get_output(self):
        return self.output


class DefaultFlowStrategy(FlowStrategy):
    @log_write
    def flow(self, src, dst, **kwargs):
        pfc_priority = kwargs.get("pfc_priority", 0)
        port = kwargs.get("port", 0)
        payload = kwargs.get("payload", 0)
        initial_time = kwargs.get("initial_time", 0)
        output = f"{src} {dst} {pfc_priority} {port} {payload} {initial_time}\n"

        self.output.write(output)

        return f"Flow from {src} to {dst} with PFC priority {pfc_priority}, port {port}, payload {payload}, and initial time {initial_time}.\n"
