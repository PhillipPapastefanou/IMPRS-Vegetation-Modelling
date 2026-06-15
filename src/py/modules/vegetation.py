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
        
        
        # Phenology [0.0: No leaves, 1.0 full leaves]
        self.phenology = 1.0


        # Stand level heart wood [g C m-2] 
        self.heart_wood = 0.0
        # Stand level sap wood [g C m-2]         
        self.sap_wood = 0.0
        
        # Stem diameter at breast height [m]
        self.dbh = 0.0
        # Tree trunk height [m]
        self.height  = 0.0


    def Update(self, co2, temp, sw_rad, vpd, soil_water, t):

        


        # Max gross primary productivity [g C m-2 day-1]
        self.gpp_max = self.photosynthesis.Update(co2 = co2,
                                   temp= temp,
                                   sw_rad= sw_rad,
                                   daylength= self.parameters.day_length,
                                   fpar = 0.5,
                                   chi = 0.7)

        # Max net primary productivity [g C m-2 day-1]
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
        #self.biomass = self.biomass + self.npp
        
        # e.g., 0.05 trees/m2 = 500 trees per hectare
        stem_density_trees_m2 = 0.05
        
        # Fraction of sapwood that turns into heartwood per year
        turnover_rate_annual = 0.1 
        turnover_rate_daily = turnover_rate_annual / 365.0
        
        sap_allocation_frac = 0.45  # Fraction of npp that goes into sapwood
        wood_dens_g_m3 = 578000.0   # wood density
        form_factor = 0.8           # Paraboloid stem
        k1 = 35.0                   # Allometric multiplier
        k2 = 0.6                    # Allometric exponent

        # Turnover: Sapwood to Heartwood (All pools in g m-2 ground)
        sap_turnover = self.sap_wood * turnover_rate_daily
        self.sap_wood = self.sap_wood - sap_turnover
        self.heart_wood += sap_turnover
        
        # Allocation: Direct addition since both NPP and pools are per m2 ground
        self.sap_wood += self.npp * sap_allocation_frac
        
        # Total stand-level structural mass (g m-2 ground)
        stand_woody_mass_g_m2 = self.sap_wood + self.heart_wood 
        
        # Convert the mass toa single average tree (g / tree)
        individual_tree_mass_g = stand_woody_mass_g_m2 / stem_density_trees_m2
        
        # Calculate DBH of that representative tree (in meters)
        self.dbh = ((individual_tree_mass_g * 4.0) / 
                    (wood_dens_g_m3 * form_factor * np.pi * k1)) ** (1.0 / (2.0 + k2))      
        
        # Height comes directly from the allometric relationship
        self.height = k1 * (self.dbh ** k2)    

    def calc_beta(self, soil_water):
        return 1 / (1 + np.exp( - self.parameters.plant_sw_alpha*(soil_water - self.parameters.plant_sw_close_50)))



