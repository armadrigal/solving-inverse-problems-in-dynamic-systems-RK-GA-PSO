import numpy as np
import inspect

class PSO:
    def __init__(self, objetive_fun, n_particles=10, w=0.5, c_1=0.5, c_2=0.5, interval=(-1.0,1.0)):
        self.objetive_fun = objetive_fun
        self.n_particles = n_particles
        self.w = w
        self.c_1 = c_1
        self.c_2 = c_2
        self.interval = interval
        self._dimension = len(inspect.getargspec(self.objetive_fun).args)

    def initialize_swarm(self):

        self._positions = np.random.normal(
            self.interval[0], self.interval[1], (self.n_particles, self._dimension)
        )
        self._velocities = np.random.normal(
            -1.0, 1.0, (self.n_particles, self._dimension)
        )
        self._fitness = np.zeros(self.n_particles)

    def calculate_fitnnes(self):

        for i in range(self.n_particles):
            self._fitness[i] = self.objetive_fun(*list(self._positions[i]))

    def initialize_best_positions(self):

        self._p_best = self._positions
        self._fitness_p_best = self._fitness

        index_max = np.argmax(self._fitness)
        self._g_best = self._positions[index_max]
        self._fitness_g_best = self._fitness[index_max]

    def update_p_best(self):

        for i, fitness in enumerate(self._fitness):
            if fitness > self._fitness_p_best[i]:
                self._fitness_p_best[i] = fitness
                self._p_best = self._positions[i]