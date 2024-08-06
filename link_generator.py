from logger import log_write
from abc import ABC, abstractmethod
import output_strategy


class LinkStrategy(ABC):
    @abstractmethod
    def link(self, **kwargs):
        pass


class DefaultLinkStrategy(LinkStrategy):
    def __init__(self, output=output_strategy.FileOutputStrategy()):
        self.output = output

    @log_write
    def link(self, src, dst, **kwargs):
        bandwidth = kwargs.get("bandwidth", 0)
        delay = kwargs.get("delay", 0)
        error_rate = kwargs.get("error_rate", 0)

        output = f"{src} {dst} {bandwidth} {delay} {error_rate}\n"

        self.output.write(output)
        return f"Connected {src} to {dst} with {bandwidth} bandwidth, {delay} delay, and {error_rate} error rate.\n"
