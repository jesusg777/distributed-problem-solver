from problem_factory_method.i_problem_creator import IProblemCreator
from problem_factory_method.i_problem_solver import IProblemSolver
from problem_factory_method.fibonacciVerifier import FibonacciVerifier

class CreatorFibonacciVerifier(IProblemCreator):

    def factory_method(self) -> IProblemSolver:
        return FibonacciVerifier()