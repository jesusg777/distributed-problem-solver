from problem_factory_method.i_problem_solver import IProblemSolver

class FizzBuzz(IProblemSolver):

    def solve_problem(self, data: list) -> list:
        result = []
        for element in data:
            line = self.__fizz_buzz(int(element))
            result.append(f"{line}")
        return result

    def __fizz_buzz(self, number: int) -> str:
        result = ""
        if number % 3 == 0:
            result += "Fizz"
        if number % 5 == 0:
            result += "Buzz"
        return result or str(number)