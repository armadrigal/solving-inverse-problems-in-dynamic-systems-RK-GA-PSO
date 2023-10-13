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

    def crossover(self, selection):

        random = np.random.permutation(np.arange(self._selection_size))
        #print('llego hasta aqui')
        #print(random)
        for i in range(int(self._selection_size/2)):
            parent_1 = selection[random[i]]
            parent_2 = selection[random[i+int(self._selection_size/2)]]
            son_1, son_2 = self.single_point_crossover(parent_1, parent_2)
            selection[random[i]] = son_1
            selection[random[i+int(self._selection_size/2)]] = son_2

        return selection

    def mutation(self, population, mutation_fraction):

        for i, individual in enumerate(population):
            for j, _ in enumerate(individual):
                if np.random.rand() < mutation_fraction:
                    population[i,j] = np.random.uniform(self.ecosystem[0], self.ecosystem[1])
        
        return population

    def evolve(self, n_generations = 1):

        if self._initiated_population == False:
            population = self.initialize_population()
            self._initiated_population = True

        fitness = self.calculate_fitness(population)
        best_fitness = np.max(fitness)
        best_optimum = population[np.argmax(fitness)]
        for i in range(n_generations):
            selection = self.roulette_selection(population, fitness)
            crossover = self.crossover(selection)
            #reemplazar
            fitness_order = np.argsort(fitness)
            population[fitness_order[-self._selection_size:]] = crossover
            ##########
            population = self.mutation(population, self._mutation_fraction)
            fitness = self.calculate_fitness(population)
            max_index = np.argmax(fitness)

            optimum = population[max_index]
            fitness_optimum = fitness[max_index]

            if fitness_optimum > best_fitness:
                best_optimum = optimum
                best_fitness = fitness_optimum

                print('Generation: ', i , 'Optimum: ', optimum, 'Fitness', fitness_optimum)

        return best_optimum, best_fitness