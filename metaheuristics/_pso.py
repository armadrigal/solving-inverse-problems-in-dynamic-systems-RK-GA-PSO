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

    def _initialize_swarm(self):

        self._positions = np.random.normal(
            self.interval[0], self.interval[1], (self.n_particles, self._dimension)
        )
        self._velocities = np.random.normal(
            -1.0, 1.0, (self.n_particles, self._dimension)
        )
        self._fitness = np.zeros(self.n_particles)

    def _calculate_fitnnes(self):

        for i in range(self.n_particles):
            self._fitness[i] = self.objetive_fun(*list(self._positions[i]))

    def _initialize_best_positions(self):

        self._p_best = self._positions
        self._fitness_p_best = self._fitness

        index_max = np.argmax(self._fitness)
        self._g_best = self._positions[index_max]
        self._fitness_g_best = self._fitness[index_max]

    def _update_p_best(self):

        for i, fitness in enumerate(self._fitness):
            if fitness > self._fitness_p_best[i]:
                self._fitness_p_best[i] = fitness
                self._p_best = self._positions[i]

    def _update_g_best(self):

        index_max = np.argmax(self._fitness)
        if self._fitness[index_max] > self._fitness_g_best:
            self._fitness_g_best = self._fitness[index_max]
            self._g_best = self._positions[index_max]

    def _update_velocities(self):

        vel = self.w*self._velocities +\
            self.c_1*np.random.rand()*(self._p_best - self._positions) +\
            self.c_2*np.random.rand()*(self._g_best - self._positions)

        self._velocities = vel

    def _update_positions(self):

        self._positions += self._velocities

    def fit(self, n_iterations=10):

        self._initialize_swarm()
        self._calculate_fitnnes()
        self._initialize_best_positions()

        for i in range(1,n_iterations+1):
            self._update_velocities()
            self._update_positions()
            self._calculate_fitnnes()
            self._update_p_best()
            self._update_g_best()

            print('Iteration: ', i, 'Gbest: ', self._g_best, 'Fitness:', self._fitness_g_best)
