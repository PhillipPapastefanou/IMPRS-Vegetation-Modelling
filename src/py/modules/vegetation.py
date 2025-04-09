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

        self.parameters = parameters

        self.photosynthesis = Photosynthesis()

        # Variables
        # Maximum net photosythesis rate
        self.npp_max = 0.0
        # Photsynthesis rate
        self.npp = 0.0
        # Stomatal closure parameter
        self.beta = 1.0
        # Stomatal conductance [mol m-2 s-1]
        self.gs = 0.5
        # Transpiration [mm  m-2 s-1]
        self.transpiration = 0.0
        # Biomass [g C m-2]
        self.biomass = 0.0



    def Update(self, co2, temp, sw_rad, vpd, soil_water):

        # Max gross primary productivity [g C m-2 day-1]
        self.gpp_max = self.photosynthesis.Update(co2 = co2,
                                   temp= temp,
                                   sw_rad= sw_rad,
                                   daylength= self.parameters.day_length,
                                   fpar = 0.5,
                                   chi = 0.7)

        # Maxn net primary productivity [g C m-2 day-1]
        self.npp_max = self.gpp_max * (1.0 - self.parameters.resp_frac)


        # Calculate stomatal closure [-]
        self.beta = self.calc_beta(soil_water)

        # Calculate stomatal conductance based on Medyln 2011 [mol s-1 m-2]
        self.gs = self.parameters.g0 + self.beta * (1.0 + self.parameters.g1 / np.sqrt(vpd)) * self.npp_max / co2 * self.STOM_CONV

        # Calculate transpiration [mm day-1 m-2]
        self.transpiration = self.gs * vpd * self.H2O_CO2_DIFFUSIVITY * self.SECONDS_PER_DAY / self.MOL_TO_MM_H2O

        # Rescale transpiration to sunshine hours
        self.transpiration = self.transpiration * self.parameters.day_length / self.HOURS_PER_DAY

        # Calculate net productivity [g day-1 m-2]
        self.npp = self.npp_max * self.beta

        # Growth
        self.biomass = self.biomass + self.npp


    def calc_beta(self, soil_water):
        return 1 / (1 + np.exp( - self.parameters.plant_sw_alpha*(soil_water - self.parameters.plant_sw_close_50)))



