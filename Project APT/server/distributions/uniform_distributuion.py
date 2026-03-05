import random
from distributions.i_distribution_solver import IDistributionRandomSolver

class UniformDistribution(IDistributionRandomSolver):
    def generate_numbers(self, min, max, count):
        numbers = [round(random.uniform(min, max)) for _ in range(count)]
        distribution = 'uniform'
        
        return numbers, distribution