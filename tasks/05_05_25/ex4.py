#
# Exercise  4
#

# 4.1 Think about some processes that would require some change.
# For example. Biomass in the current implementation is steadly increasing
# What are processes that could make biomass reach an equilibrium?
# Think about some ways to implement that.

# 4.2 (Bonus) Why is it much more difficult to run the model on monthly timescales?

# 4.3 (Bonus) What is the major problem when using the Medlyn 2011 model and the Collatz 1991 scheme?


import os
import sys
sys.path.append("../")
from src.py.framework.model import Model
from src.py.framework.parameters import Parameters

parameters = Parameters()

model = Model(parameters = parameters)

model.setup()

model.run()

model.plot()


