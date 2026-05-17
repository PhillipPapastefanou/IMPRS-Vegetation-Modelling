#
# Exercise  0
#

# Apply the model with standard conditions
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, os.pardir, os.pardir))
sys.path.append(project_root)

from src.py.framework.model import Model
from src.py.framework.parameters import Parameters

if __name__ == "__main__":

    parameters = Parameters()
    
    parameters.nyears = 10

    model = Model(parameters)

    model.setup()

    model.run()

    model.plot()

