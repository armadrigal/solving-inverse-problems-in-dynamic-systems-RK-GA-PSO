import numpy as np
import inspect

class genetic_algorithm:

    def __init__(
        self, fitness_function, population_size=10, ecosystem=(-1,1),
        selection=0.1, mutation_fraction=0.1, target='maximize'
        ):
        self.fitness_function = fitness_function
        self.target = target
        self.population_size = population_size
        self.ecosystem = ecosystem
        self._dimension = len(inspect.getargspec(self.fitness_function).args)
        self._selection_size = int(np.round((selection/2)*population_size))*2
        self._mutation_fraction = mutation_fraction
        self._initiated_population = False