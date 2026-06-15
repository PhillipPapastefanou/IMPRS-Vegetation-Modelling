from src.py.framework.parameters import Parameters
from src.py.framework.output import Output

from src.py.modules.forcing import Forcing
from src.py.modules.soil import Soil
from src.py.modules.vegetation import Vegetation

import os

script_dir = os.path.dirname(os.path.abspath(__file__))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

            self.vegetation.Update(co2, temp, sw_rad, vpd, self.soil.soil_water, t)

            self.soil.Update(precip, self.vegetation.transpiration)

            ##############################
            # Update output
            ##############################
            self.output.Update(t)

    def plot(self):
        df = self.output.data_frame
        fig = plt.figure(figsize=(10, 10))
        vars = ['biomass', 'transpiration', 'soil_water', 'npp', 'gs', 'beta', 'phenology', 'height', 'dbh']
        units = ['[g m-2]', '[mm m-2 d-1]',
                 '[% m-2]', '[g m-2 d-1]', '[mol m-2 s-1]', '[-]', '[-]', '[m]', '[m]']

        for id, var, unit in zip(np.arange(1,len(vars) + 1), vars, units):
            ax = fig.add_subplot(3, 3, id)
     
            ax.set_ylabel(f"{var} {unit}")
            ax.set_title(var)
            
            if var == 'phenology':
                ax.set_ylim(0.0,1.05)
                df_obs = pd.read_csv(os.path.join(script_dir, os.pardir, os.pardir, os.pardir, 'data', 'phen_avg.csv'))
                ax.plot(df_obs['phenology'], c='black', label='obs')
                
                # 365 day average phenology from obs
                obs_365 = df_obs['phenology'].values
                
                # Change dimensionalty of modelled timeseries (1 -> 2) 
                mod_series = np.split(self.output.data_frame['phenology'], self.params.nyears)
                # 365 day average phenology from model
                mod_365 = np.mean(mod_series, axis=0)
                
                # Mean squared error
                mse = 1/365*np.sum((mod_365-obs_365)**2)
                
                ax.plot(np.arange(0,365.0), mod_365, c = 'tab:blue', label = 'mod', alpha = 0.7)
                ax.text(400, 0.9, f"MSE: {mse}")

                ax.legend()
                
            else:
                ax.plot(df[var])
                
        plt.subplots_adjust(wspace=0.4, hspace=0.3)
        plt.show()

