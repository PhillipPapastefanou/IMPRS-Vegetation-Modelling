import numpy as np
from jupyter_client.adapter import adapt

from src.py.auxil.lookup import LookupTable
from src.py.auxil.lookup import LookupQ10

PSTEMPMIN = 2
PSTEMPMAX = 55
PSTEMPHIGH = 30
PSTEMPLOW = 25
K1 = (PSTEMPMIN + PSTEMPLOW) / 2.0
ALPHA_A = 0.6
CMASS = 12
CO2CONV = 1E-6
THETA = 0.7
K2DEGC = 273.15
ALPHAC3 = 0.08
BC3 = 0.015
CQ = 4.6 * 1E-6
PATMSOS = 1E5
PO2 =  20900
SECONDS_PER_DAY = 86400

class Photosynthesis:
    def __init__(self):

        temps = np.arange(-5.0, 50.0, 0.1)
        tscals = self.t_scal(temps)
        self.tscal_lt = LookupTable(x = temps, y = tscals)

        self.tau_q10 = LookupQ10(base25=2600.0, q10= 0.57)
        self.ko_q10 = LookupQ10(base25=30000.0, q10= 1.2)
        self.kc_q10 = LookupQ10(base25=30.0, q10= 2.1)

    def t_scal(self, temp):
        enum = 1.0 - 0.01 * np.exp(4.6*(-PSTEMPHIGH + temp)/(-PSTEMPHIGH + PSTEMPMAX))
        denom = 1.0 + np.exp(4.6*(-temp + K1)/(-PSTEMPMIN + K1))
        return enum / denom

    def Update(self, co2, temp, sw_rad, daylength, fpar, chi):

        par = sw_rad * SECONDS_PER_DAY

        apar =  par * fpar * ALPHA_A

        gamma_star = PO2 / 2.0 / self.tau_q10.Get(temp)

        ca = co2 * PATMSOS * CO2CONV

        ci = ca * chi

        keff = self.kc_q10.Get(temp) * (1.0 + PO2/ self.ko_q10.Get(temp))

        c1 = (ci - gamma_star)/(ci + 2*gamma_star) * ALPHAC3

        c2 = (ci - gamma_star)/(ci + keff)

        b = BC3

        # For now, we do not consider n limitation
        vm = 200

        rdg = vm*b
        je = c1 * self.tscal_lt.Get(temp) *apar * CMASS * CQ / daylength

        jc = c2 * vm / 24.0

        agd_g = 1.0 / 2.0 / THETA * daylength * (jc + je -
            np.sqrt(-4.0 *THETA * jc * je + (jc + je)**2))

        return agd_g