from src.py.framework.parameters import Parameters
from src.py.framework.output import Output

from src.py.modules.forcing import Forcing
from src.py.modules.soil import Soil
from src.py.modules.vegetation import Vegetation

import matplotlib.pyplot as plt
import numpy as np

class Model:
    NDAYS_PER_YEAR = 365
    def __init__(self, parameters: Parameters):

        self.params = parameters
        # Create instances of model components
        self.forcing = Forcing(self.params)
        self.soil = Soil(self.params)
        self.vegetation = Vegetation(self.params)

        self.output = Output(self.params,self.soil, self.vegetation)

    def setup(self):
        self.forcing.generate()

    def run(self):
        for t in range(int(self.params.nyears * self.NDAYS_PER_YEAR )):
            # For each day...
            ##############################
            # Climate forcing
            ##############################
            df_clim = self.forcing.get_day(t)

            # Shortwave radiation [W m-2]
            sw_rad = df_clim['sw_rad']
            # Vapor pressure deficit [Pa]
            vpd = df_clim['vpd']
            # Precipitation [mm d-1]
            precip = df_clim['precip']
            # Atmospheric co2 concentration [ppm]
            co2 = df_clim['co2']
            # Surface temperature [Degree C]
            temp = df_clim['temp']

            ##############################
            # Main model routines
            ##############################

            self.vegetation.Update(co2, temp, sw_rad, vpd, self.soil.soil_water)

            self.soil.Update(precip, self.vegetation.transpiration)

            ##############################
            # Update output
            ##############################
            self.output.Update(t)

    def plot(self):
        df = self.output.data_frame
        fig = plt.figure(figsize=(8, 8))
        vars = ['biomass', 'transpiration', 'soil_water', 'npp', 'gs', 'beta']
        units = ['[g m-2]', '[mm m-2 d-1]',
                 '[% m-2]', '[g m-2 d-1]', '[mol m-2 s-1]', '[-]']

        for id, var, unit in zip(np.arange(1,len(vars) + 1), vars, units):
            ax = fig.add_subplot(3, 2, id)
            ax.plot(df[var])
            ax.set_ylabel(f"{var} {unit}")
            ax.set_title(var)

        plt.subplots_adjust(wspace=0.4, hspace=0.3)
        plt.show()

