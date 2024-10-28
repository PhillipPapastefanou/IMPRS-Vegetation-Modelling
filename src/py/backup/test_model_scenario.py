import numpy as np

from src.py.framework.model import Model
from src.py.framework.parameters import Parameters

params = Parameters()

params.nyears = 6

model = Model(params)
model.setup()


start_day = 365 * 2
end_day   = 365 * 6

model.forcing.df.loc[start_day:end_day, 'precip'] *= 1.0
model.forcing.df.loc[start_day:end_day, 'co2'] *= 1.0
model.forcing.df.loc[start_day:end_day, 'vpd'] *= 1.0


# model.climate.df.loc[start_day: + end_day, 'co2'] *= np.linspace(1.0, 3.0 ,end_day-start_day)
# model.climate.df.loc[start_day: + end_day, 'precip'] *= np.linspace(1.0, 0.1 ,end_day-start_day)

model.run()
model.plot()