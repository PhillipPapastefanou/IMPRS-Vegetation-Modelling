#
# Exercise  0
#

# Apply the model with standard conditions
import sys
sys.path.append("../")

from src.py.framework.model import Model
from src.py.framework.parameters import Parameters

if __name__ == "__main__":

    parameters = Parameters()
    parameters.nyears = 10

    model = Model(parameters)

    model.setup()

    model.run()

    model.plot()

