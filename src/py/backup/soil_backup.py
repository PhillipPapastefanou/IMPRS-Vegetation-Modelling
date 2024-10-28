from src.py.framework.parameters import Parameters

class Soil:

    def __init__(self, parameters: Parameters):

        # Obtain parameters
        self.max_sw_content = parameters.max_sw_content
        self.runoff_min = parameters.runoff
        self.perculation_rate = parameters.percolation_rate

        # Initial soil water content
        self.soil_water = 100


    def Update(self, precip, transpiration):

        self.runoff = self.runoff_min
        self.soil_water += (precip - transpiration - self.runoff)
        self.soil_water *= self.perculation_rate

        if self.soil_water < 0:
            self.soil_water = 0.0

        if self.soil_water > self.max_sw_content:
            # Put excess water to runoff
            self.runoff += self.soil_water - self.max_sw_content
            self.soil_water = self.max_sw_content


