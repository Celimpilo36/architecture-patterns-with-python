from abc import ABC, abstractmethod


# Abstraction
class Worker(ABC):
    @abstractmethod
    def work(self) -> None:
        pass


# Low-level modules
class Developer(Worker):
    def work(self) -> None:
        print("Developer is writing code")


class Designer(Worker):
    def work(self) -> None:
        print("Designer is designing...")


# High-level module
class Manager:
    def __init__(self, worker: Worker):
        self.worker = worker

    def manage(self):
        self.worker.work()


# Example usage
if __name__ == "__main__":
    dev = Developer()
    des = Designer()

    manager1 = Manager(dev)
    manager2 = Manager(des)

    manager1.manage()  # Output: Developer is writing code
    manager2.manage()  # Output: Designer is designing...
