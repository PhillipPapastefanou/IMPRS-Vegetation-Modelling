from src.py.modules.forcing import Forcing

from matplotlib import pyplot as plt

from src.py.framework.parameters import Parameters

params = Parameters()



climate = Forcing(params)
climate.generate()

#plt.plot(climate.precip)
plt.plot(climate.vpd)
#plt.plot(climate.sw_rad)
plt.show()