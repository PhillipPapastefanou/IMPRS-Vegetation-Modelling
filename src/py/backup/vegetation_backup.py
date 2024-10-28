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
        # Vegetation biomass per unit area [kg m-2]
        self.biomass = 0.0
        # Stomatal conductance [mol m-2 s-1]
        self.gs = 1.0
        # Transpiration [mm m-2 d-1]
        self.transpiration = 0.0
        # Stomatal closure parameter [-]
        self.beta = 1.0
        # Photosynthesis component
        self.photosynthesis = Photosynthesis()


    def Update(self, soil_water, vpd, sw_rad, co2, temp):

        # Calculate the maximum photosynthesis rate [g C m-2]
        gpp_max = self.photosynthesis.Update(co2=co2,
                                   temp= temp,
                                   sw_rad=sw_rad,
                                   daylength= self.params.day_length,
                                   fpar = 0.5,
                                   chi = 0.7)

        # Get NPP based on GPP and the respiration fraction [g C m-2 day-1]
        npp_max = gpp_max * (1.0 - self.params.resp_frac)


        # Calculate stomatal downregulation
        self.beta = self.calc_stom_closure(soil_water,
                                           self.params.sw_content_closure_50,
                                           self.params.sw_response_shape)

        # Calculate stomatal conductance based on Medlyn et al. 2011
        # gs in mol m-2 s-1
        self.gs = self.params.g0 +  self.beta * (1.0 + self.params.g1/np.sqrt(vpd)) * npp_max / co2 * self.STOM_CONV

        # fractions of sunshine hours per day
        frac_of_day = self.params.day_length / self.HOURS_PER_DAY

        # Update transpiration mm H20 day-1
        self.transpiration = self.gs * vpd * self.H2O_CO2_DIFFUSIVITY * self.SECONDS_PER_DAY / self.MOL_TO_MM_H2O

        # Rescale transpiration to only the sunny part of the day
        self.transpiration*= frac_of_day

        # Update productivity
        self.npp = npp_max * self.beta

        # Growth
        # Update biomass
        self.biomass += self.npp

    def calc_stom_closure(self, sw_content, closure_50, shape):
        return (1.0 - 1.0/(1.0 + (sw_content / closure_50)**shape))




