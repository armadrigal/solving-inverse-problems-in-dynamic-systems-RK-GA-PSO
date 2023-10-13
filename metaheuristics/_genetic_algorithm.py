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

    def initialize_population(self):
        population = np.random.uniform(
            self.ecosystem[0], self.ecosystem[1], 
            (self.population_size,self._dimension)
        )
        return population

    def calculate_fitness(self, population):
        fitness = np.zeros(len(population))
        for i in range(len(population)):
            fitness[i] = self.fitness_function(*list(population[i,:]))
        return fitness

    def roulette_selection(self, population, fitness):
        selection = np.zeros((self._selection_size,self._dimension))
        probability = np.exp(fitness)/np.sum(np.exp(fitness))
        
        for i, random in enumerate(np.random.rand(self._selection_size)):
            for j in range(len(probability)):
                sum_proba = np.sum(probability[0:j])
                if random >= sum_proba and random < sum_proba + probability[j]:
                    selection[i,:] = population[j,:]

        return selection

    def single_point_crossover(self, parent_1, parent_2):

        son_1 = np.zeros(self._dimension)
        son_2 = np.zeros(self._dimension)

        crossover_point = np.random.randint(self._dimension)

        son_1[0:crossover_point] = parent_1[0:crossover_point] 
        son_1[crossover_point:self._dimension] = parent_2[crossover_point:self._dimension]
        son_2[0:crossover_point] = parent_2[0:crossover_point] 
        son_2[crossover_point:self._dimension] = parent_1[crossover_point:self._dimension] 

        return son_1, son_2