from abc import ABC, abstractmethod


class OutputStrategy(ABC):
    @abstractmethod
    def write(self, data: str):
        pass


class FileOutputStrategy(OutputStrategy):
    def __init__(self, file_name: str = "output.txt"):
        # open the file in write mode
        self.file = open(file_name, "w")

    def write(self, data):
        self.file.write(data)

    # close the file when the object is deleted
    def __del__(self):
        self.file.close()


class ConsoleOutputStrategy(OutputStrategy):
    def write(self, data: str):
        # print the data to the console
        print(data)
