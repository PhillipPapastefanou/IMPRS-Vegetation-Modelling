import os
import sys
sys.path.append("../")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

x = np.arange(0, 1, 0.01)
y = np.exp(x)
plt.scatter(x,y)
plt.show()