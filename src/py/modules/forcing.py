import numpy as np
import pandas as pd
from src.py.framework.parameters import Parameters

class Forcing:
    def __init__(self, parameters: Parameters):
        self.nyears = parameters.nyears

        # Atmospheric pressure [Pa]
        self.PRESSURE = 101300

        # Max radiation per square meter
        self.MAX_RAD = 600
        # Min radiation per square meter
        self.MIN_RAD = 100

        # Max precipitation per square meter
        self.MAX_PRECIP = 200
        # Max precipitation per square meter
        self.MIN_PRECIP = 50

        # Max temperature per square meter
        self.MAX_TEMP = 26
        # Max temperature per square meter
        self.MIN_TEMP = 5

        # Vapor pressure deficit max (kPa)
        self.MAX_VPD = 2.5
        # Vapor pressure deficit min (kPa)
        self.MIN_VPD = 0.1

        self.DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def generate(self):

        np.random.seed(123456789)

        self.sw_rad = []
        for i in range(self.nyears):
            sw_rad = (((self.MAX_RAD - self.MIN_RAD)*
                               (np.sin(2*np.pi/365 *(np.arange(365) - 150))+1)/2) + self.MIN_RAD)
            sw_rad += np.random.uniform(-50, 100, 365)

            self.sw_rad.append(sw_rad)

        self.sw_rad= np.concatenate(self.sw_rad, axis=0)


        self.precip = []
        for i in range(self.nyears):
            prec_per_month = (((self.MAX_PRECIP - self.MIN_PRECIP)*
                               (np.sin(2*np.pi/12 *(np.arange(12) - 5))+1)/2) + self.MIN_PRECIP)
            prec_per_month += np.random.uniform(-20, 50, 12)

            prec_per_month[prec_per_month < 0] = 0.0

            for m in range(12):
                ndays = self.DAYS_IN_MONTH[m]

                prec_m = prec_per_month[m]

                if prec_m > 60:
                    nrainy_days = np.random.randint(10,20)
                else:
                    nrainy_days = np.random.randint(2,10)

                indexes = np.random.choice(ndays, nrainy_days)

                prec_per_day = np.zeros(ndays)
                prec_per_day[indexes] = prec_m/nrainy_days
                self.precip.append(prec_per_day)

        self.precip= np.concatenate(self.precip, axis=0)


        self.temp = []
        for i in range(self.nyears):
            temp_per_month = (((self.MAX_TEMP - self.MIN_TEMP)*
                               (np.sin(2*np.pi/365 *(np.arange(365) - 150))+1)/2) + self.MIN_TEMP)
            temp_per_month += np.random.uniform(-4, 4, 365)

            self.temp.append(temp_per_month)
        self.temp= np.concatenate(self.temp, axis=0)


        self.vpd = []
        for i in range(self.nyears):
            vpd_per_month = (((self.MAX_VPD - self.MIN_VPD)*
                               (np.sin(2*np.pi/365 *(np.arange(365) - 150))+1)/2) + self.MIN_VPD)
            vpd_per_month += np.random.uniform(-0.1, 0.25, 365)
            vpd_per_month[vpd_per_month < 0] = 0.00001
            self.vpd.append(vpd_per_month)
        self.vpd = np.concatenate(self.vpd, axis=0)
        self.vpd *= 1000.0/self.PRESSURE

        self.df = pd.DataFrame(self.sw_rad, columns=['sw_rad'])
        self.df['precip'] = self.precip
        self.df['temp'] = self.temp
        self.df['vpd'] = self.vpd
        self.df['co2'] = np.zeros(self.nyears * 365) + 400

    def get_day(self, timestep):
        return self.df.loc[timestep, :]




