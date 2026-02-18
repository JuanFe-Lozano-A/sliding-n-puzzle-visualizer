from abc import ABC, abstractmethod

class BaseSolver(ABC):
    def __init__(self, board):
        self.board = board

    @abstractmethod
    def solve(self):
        pass

    @abstractmethod
    def get_decision_basis(self):
        pass

    @abstractmethod
    def get_metrics(self):
        pass
