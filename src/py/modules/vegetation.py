import numpy as np
from src.py.framework.parameters import Parameters
from src.py.modules.soil import Soil
from src.py.modules.photosynthesis import Photosynthesis


class Vegetation:
    MOL_TO_MM_H2O = 1000.0 / 18.0
    SECONDS_PER_DAY = 86400.0
    MICRO_G_TO_G = 1.0E6
    HOURS_PER_DAY = 24.0
    H2O_CO2_DIFFUSIVITY = 1.6
    STOM_CONV = SECONDS_PER_DAY / MICRO_G_TO_G * 12.0 * 0.13

    def __init__(self, parameters: Parameters):
        self.params = parameters