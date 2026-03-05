from abc import ABC, abstractmethod
from problem_factory_method.i_problem_solver import IProblemSolver

class IProblemCreator(ABC):
    
    @abstractmethod
    def factory_method(self) -> IProblemSolver:
        pass

    def solve_problem(self, data) -> list:
        problem = self.factory_method()
        result = problem.solve_problem(data)
        return result