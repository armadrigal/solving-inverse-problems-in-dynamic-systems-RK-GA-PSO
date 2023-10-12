import numpy as np

class RungeKutta4:

    def __init__(self,f):
        self.f = f
    
    def _calculate_slope(self, t, x, h):
        
        k_1 = np.array(self.f(t,*x))
        k_2 = np.array(self.f(t + (1/2)*h, *list(x + (1/2)*h*k_1)))
        k_3 = np.array(self.f(t + (1/2)*h, *list(x + (1/2)*h*k_2)))
        k_4 = np.array(self.f(t + h, *list(x + h*k_3)))
        
        return (h/6)*(k_1 + 2*k_2 + 2*k_3 + k_4)

    def solve(self, interval, initial_conditions, time_step):

        t = np.arange(interval[0], interval[1], time_step)
        x = np.zeros((len(initial_conditions), len(t)))
        x[:,0] = np.array(initial_conditions)

        for i in range(len(t)-1):
            slope = self._calculate_slope(t[i], x[:,i], time_step)
            x[:,i+1] = x[:,i] + slope

        sol = [t] + [x_ for x_ in x]

        return sol