import numpy as np

EARTH_RAD = 6.371E6
MAG_PERM = 1.256E-6
DIPOLE = 1
DIPOLE_VEC = np.array([0, -DIPOLE])

HE = 1


def rhat(azimuth):
    return np.array([np.round(np.cos(azimuth), decimals=10), 
                     np.round(np.sin(azimuth), decimals=10)])


def thetahat(azimuth):
    return np.array([np.round(-np.sin(azimuth), decimals=10), 
                     np.round(np.cos(azimuth), decimals=10)])

def N(Npos, r):
    

    return N