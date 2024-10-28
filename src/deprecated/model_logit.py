import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Timestep
DT = 0.1
# Start time point
T0   = 0
# End time point
TMAX = 75

# Initial number of observations
y0 = 10

kappa = 10000.0

rate = 0.02

timepoints = np.arange(T0, TMAX + DT, DT)



df = pd.DataFrame(timepoints, columns=['t'])
df['y'] = np.zeros(len(timepoints))

yt = y0
for t, i in zip(timepoints, np.arange(len(timepoints))):

    df.loc[i, 'y'] = yt

    dyt = rate* yt * (1 - yt/kappa)

    yt += dyt

plt.plot(df['t'], df['y'], color='blue')
plt.show()

