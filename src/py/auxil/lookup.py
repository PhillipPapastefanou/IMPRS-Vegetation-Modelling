import numpy as np

class LookupTable:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        if x.shape[0] != y.shape[0]:
            print("Lookup arrays do not match in size...")
            exit(99)

        self.xmin = np.min(self.x)
        self.xmax = np.max(self.x)

        size = x.shape[0]

        self.m = (size - 1) / (self.xmax - self.xmin)
        self.b = - (size - 1) / (self.xmax - self.xmin) * self.xmin

    def Get(self, x):
        if x > self.xmax:
            return self.y[-1]
        if x < self.xmin:
            return self.y[0]
        index = int(self.m*x + self.b)
        return self.y[index]

class LookupQ10:

    def __init__(self, q10, base25):
        n_data = int(140/0.01 + 1.5)
        self.x = np.arange(n_data)
        self.y = base25 * np.power(q10, (-70.0 + self.x * 0.01 - 25) / 10.0)

    def Get(self, x):
        return self.y[int((x + 70)/0.01 + 0.5)]