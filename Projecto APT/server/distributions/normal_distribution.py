import random
from distributions.i_distribution_solver import IDistributionRandomSolver

class NormalDistribution(IDistributionRandomSolver):

    def generate_numbers(self, min, max, count):
        media = (min+max)/2
        sigma = (max - min)/3
        numbers = [round(random.gauss(media, sigma)) for _ in range(count)]
        distribution = 'normal'
        
        return numbers, distribution


