from abc import ABC, abstractmethod

class IProblemSolver(ABC):
    
    @abstractmethod
    def solve_problem(self, data: list) -> list:
        pass