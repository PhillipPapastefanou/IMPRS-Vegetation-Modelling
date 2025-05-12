#
# Exercise  2
#

# Apply the model and perform some climate manipulations

# 2.1: What happens if you increase CO2 by a factor of 2 or 3? What would you expect?

# 2.2: What happens if you decrease precipitation by 30,50,70 or even 90% over some years?

# 2.3: What happens if you increase VPD by a factor of 2 to 10 (extremely dry)?

# 2.4: What happens if you apply multiple of these changes at the same time? Can some effects balance each others out?

# Bonus: Why does a strong reduction in precipitation makes the annual pattern almost disappear?
import os
import sys
sys.path.append("../")
from src.py.framework.model import Model
from src.py.framework.parameters import Parameters
import numpy as np

parameters = Parameters()

parameters.nyears = 5

model = Model(parameters = parameters)
# We have to call model setup first to generate the climate
model.setup()

start_day = 365 * 2
end_day   = 365 * 5

# No we can induce some abrupt changes to the forcing...
model.forcing.df.loc[start_day:end_day, 'precip'] *= 1.0
model.forcing.df.loc[start_day:end_day, 'co2'] *= 1.0
#model.forcing.df.loc[start_day:end_day, 'vpd'] *= 1.0

#...or some gradual changes
model.forcing.df.loc[start_day: + end_day, 'co2'] *= np.linspace(1.0, 4.0 ,end_day-start_day)
model.forcing.df.loc[start_day: + end_day, 'precip'] *= np.linspace(1.0, 0.2 ,end_day-start_day)
# model.forcing.df.loc[start_day: + end_day, 'precip'] *= np.linspace(1.0, 0.1 ,end_day-start_day)


model.run()
model.plot()


