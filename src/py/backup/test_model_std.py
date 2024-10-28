from src.py.framework.model import Model
from src.py.framework.parameters import Parameters
import matplotlib.pyplot as plt

params = Parameters()

params.nyears = 2

model = Model(params)

model.setup()

model.run()

model.plot()