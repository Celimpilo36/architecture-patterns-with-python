from abc import ABC, abstractmethod


# Abstraction
class Worker(ABC):
    @abstractmethod
    def work(self) -> None:
        pass


# Low level modules
class Developer(Worker):
    def work(self) -> None:
        print("Developer is writing code")


class Designer(Worker):
    def work(self) -> None:
        print("Designer is designing fireWorks")


# high level modules
class Mananger:
    def __init__(self, worker: Worker):
        self.worker = worker

    def manange(self):
        self.worker.work()


dev = Developer()
designer = Designer()

mananger1 = Mananger(dev)
mananger2 = Mananger(designer)
mananger1.manange()
mananger2.manange()
