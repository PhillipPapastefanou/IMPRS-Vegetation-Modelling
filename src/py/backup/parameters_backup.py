class Parameters:
    def __init__(self):

        # Number of years to simulate
        self.nyears = 10

        # Number of sunshine hours per day [h]
        self.day_length = 10

        ################################
        # Soil water based parameters
        ################################

        # Maximum water content [mm]
        self.max_sw_content = 100

        # Runoff water content [mm day-1]
        self.runoff = 0.2

        # Soil perculation rate [-]
        self.percolation_rate = 0.98

        ################################
        # Vegetation based parameters
        ################################

        # Water content with inducing mortality [mm]
        self.deadly_sw_content = 10

        # Medlyn model g1 parameter [-]
        self.g1 = 5.5

        # Medlyn model g0 parameter
        # (Minimal water loss) [mol s-1 m-2]
        self.g0 = 0.005

        # Soil water content at which stomates close 50% [mm]
        self.sw_content_closure_50 = 50

        # Shape parameter of stomatal closure [-]
        self.sw_response_shape  = 5

        # Respiration fraction. How much of GPP is respired
        # The rest is NPP [-]
        self.resp_frac = 0.7



