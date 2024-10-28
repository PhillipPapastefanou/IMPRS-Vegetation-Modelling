#
# Exercise  1
#

# Apply the model and changes some of the standard parameters

# 1.1: What happens if we increase/decrease the g0 parameter?

# 1.2: What happens if we increase/decrease the g1 parameter?

# 1.3: What happens if we increase/decrease the percolation_rate parameter?

import os
import sys
sys.path.append("../")

from src.py.framework.model import Model
from src.py.framework.parameters import Parameters

parameters = Parameters()

# This is an example how the parameters can be changes
# Increase g0 by 50%...
parameters.g0 *= 1.5
# ... or set it to some fixed value
parameters.g0 = 0.01

model = Model(parameters = parameters)
model.setup()
model.run()
model.plot()


