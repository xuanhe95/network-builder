from abc import ABC, abstractmethod
import random
from logger import log_write


class FlowStrategy(ABC):
    def __init__(self, output):
        self.output = output

    @abstractmethod
    def next(self, **kwargs):
        pass


class DefaultFlowStrategy(FlowStrategy):
    def next(self, src, dst, **kwargs):
        pfc_priority = kwargs.get("pfc_priority", 0)
        port = kwargs.get("port", 0)
        payload = kwargs.get("payload", 0)
        initial_time = kwargs.get("initial_time", 0)

        self.output.write(
            f"{src} {dst} {pfc_priority} {port} {payload} {initial_time}\n"
        )

        return f"Flow from {src} to {dst} created.\n"


class RandomFlowStrategy(FlowStrategy):
    def next(self, src, dst, **kwargs):

        pfc_priority = kwargs.get("pfc_priority", 0)
        port = kwargs.get("port", 0)
        payload = kwargs.get("payload", 0)
        initial_time = kwargs.get("initial_time", 0)

        payload = random.randint(0, payload)

        self.output.write(
            f"{src} {dst} {pfc_priority} {port} {payload} {initial_time}\n"
        )

        return f"Flow from {src} to {dst} created.\n"


class HalfFlowStrategy(FlowStrategy):
    def __init__(self, output):
        super().__init__(output)
        self.id = 0

    @log_write
    def next(self, src, dst, **kwargs):
        if self.id % 2 == 0:
            self.id += 1
            return f"Flow from {src} to {dst} not created.\n"
        self.id += 1

        pfc_priority = kwargs.get("pfc_priority", 0)
        port = kwargs.get("port", 0)
        payload = kwargs.get("payload", 0)
        initial_time = kwargs.get("initial_time", 0)

        self.output.write(
            f"{src} {dst} {pfc_priority} {port} {payload} {initial_time}\n"
        )

        return f"Flow from {src} to {dst} created.\n"
