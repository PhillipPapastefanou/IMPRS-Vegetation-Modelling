from src.py.framework.parameters import Parameters
from src.py.modules.soil import Soil
from src.py.modules.vegetation import Vegetation

import numpy as np
import pandas as pd

class Output:
    def __init__(self, parameters: Parameters,
                 soil: Soil,
                 vegetation: Vegetation):
        self.parameters = parameters
        self.soil = soil
        self.vegetation = vegetation

        self.columns = ['soil_water', 'beta', 'anet', 'biomass', 'gs']

        self.data_frame = pd.DataFrame(index=np.arange(parameters.nyears*365), columns=self.columns)

    def Update(self, t):
        self.data_frame.loc[t, 'soil_water'] = self.soil.soil_water
        self.data_frame.loc[t, 'beta'] = self.vegetation.beta
        self.data_frame.loc[t, 'biomass'] = self.vegetation.biomass
        self.data_frame.loc[t, 'gs'] = self.vegetation.gs
        self.data_frame.loc[t, 'transpiration'] = self.vegetation.transpiration
        self.data_frame.loc[t, 'npp'] = self.vegetation.npp