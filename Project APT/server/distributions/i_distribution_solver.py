from abc import ABC, abstractmethod

class IDistributionRandomSolver(ABC):
    
    @abstractmethod
    def generate_numbers(self, min, max, count):
        pass

