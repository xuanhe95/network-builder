from abc import ABC, abstractmethod

"""
OutputStrategy is an abstraction for data output.
We can implement different output strategies for writing data to a file or console.
"""


class OutputStrategy(ABC):
    @abstractmethod
    def write(self, data: str):
        pass


"""
FileOutputStrategy is for writing data to a file.
"""


class FileOutputStrategy(OutputStrategy):
    def __init__(self, file_name: str = "output.txt"):
        # open the file in write mode
        self.file = open(file_name, "w")

    def write(self, data):
        self.file.write(data)

    # close the file when the object is deleted
    def __del__(self):
        self.file.close()


"""
ConsoleOutputStrategy is for writing data to the console.
"""


class ConsoleOutputStrategy(OutputStrategy):
    def write(self, data: str):
        # print the data to the console
        print(data)
