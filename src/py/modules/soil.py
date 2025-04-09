from src.py.framework.parameters import Parameters

class Soil:

    def __init__(self, parameters: Parameters):

        # Obtain parameters
        self.runoff_rate = parameters.runoff_rate
        self.perc_frac = parameters.prec_frac
        self.max_water_content = parameters.max_water_content

        # Initialise variables
        # Soil water content [mm]
        self.soil_water = 100

    def Update(self, rain, transpiration):

        # Update soil water [mm]
        self.soil_water = self.soil_water * self.perc_frac + rain - transpiration - self.runoff_rate

        if self.soil_water < 0:
            self.soil_water = 0

        elif self.soil_water > self.max_water_content:
            self.soil_water = self.max_water_content