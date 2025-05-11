class Parameters:
    def __init__(self):

        # Number of years to simulate
        self.nyears = 10

        # Number of sunshine hours per day [h]
        self.day_length = 10

        ################################
        # Soil water based parameters
        ################################

        # Surface runoff [mm m-2]
        self.runoff_rate = 0.3

        # Percolation fraction [-]
        self.prec_frac = 0.98

        # Maximum water conetent [mm]
        self.max_water_content = 100

        ################################
        # Vegetation based parameters
        ################################

        # Respiration fraction [-]
        self.resp_frac = 0.5

        # Medyln 2011 g0 parameter
        # Minimum stomatal conductance [mol m-2 s-1]
        self.g0  = 0.005

        # Medlyn 2011 g1 parameter [-]
        self.g1 = 4.5

        # Soil water content at which plants close their stomatal 50% [mm]
        self.plant_sw_close_50 = 40

        # Shape parameter of stomatal closure function [-]
        self.plant_sw_alpha = 0.4

