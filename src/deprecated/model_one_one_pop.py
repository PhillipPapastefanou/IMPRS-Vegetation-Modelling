import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Parameters

# Timestep [t/dt]
DT = 0.1
# Start time point [t]
T0   = 0
# End time point [t]
TMAX = 100

# Number of births per time point [t]
BIRTH_RATE = 0.05

# Maximum number of Individuals
INDIV_MAX = 10000

# Transform to rate per step
BIRTH_RATE *= DT

# Setup
# Initial number of observations
y0 = 100

# Create timepoints
timepoints = np.arange(T0, TMAX + DT, DT)


df = pd.DataFrame(timepoints, columns=['t'])
df['y'] = np.zeros(len(timepoints))

yt = y0
for t, i in zip(timepoints, np.arange(len(timepoints))):

    # Save data
    df.loc[i, 'y'] = yt

    # Calculate rate of change
    dyt = BIRTH_RATE * yt

    # Update current population
    yt += dyt

plt.plot(df['t'], df['y'], color='tab:blue')
plt.axis
plt.show()
