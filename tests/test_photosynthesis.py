from src.py.modules.photosynthesis import Photosynthesis

phot = Photosynthesis()

gpp = phot.Update(co2 =278.05,temp = 26.659326553344727, sw_rad = 6327564.7170410156/86400.0,
                  daylength= 12.170114357698058, fpar = 1.0, chi = 0.8 )

print(gpp)