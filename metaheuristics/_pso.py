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