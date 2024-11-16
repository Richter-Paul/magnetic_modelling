import numpy as np
import matplotlib.pyplot as plt

MAG_PERM = 1.256E-6
EARTH_RAD = 6.371E6
DIPOLE = 1
#7.89e22
DIPOLE_VEC = np.array([0, -DIPOLE])
EMP_DATA = np.array([6.3E-5, 5.9E-5, 5.6E-5, 5E-5, 3.7E-5, 3.5E-5, 
                     3.4E-5, 4E-5, 5E-5, 5.9E-5, 6.3E-5])

ANGLES_ARR = np.array([-np.pi/2, -np.pi/3, -np.pi/4, -np.pi/6, -np.pi/12, 
                      0, np.pi/12, np.pi/6, np.pi/4, np.pi/3, np.pi/2])


def rhat(azimuth):
    return np.array([np.round(np.cos(azimuth), decimals=10), 
                     np.round(np.sin(azimuth), decimals=10)])


def thetahat(azimuth):
    return np.array([np.round(-np.sin(azimuth), decimals=10), 
                     np.round(np.cos(azimuth), decimals=10)])


def mag_field_cartesian(azimuth):

    Rhat = rhat(azimuth)

    return ((MAG_PERM/(4 * np.pi * EARTH_RAD**3)) * 
            (3*Rhat*np.dot(DIPOLE_VEC, Rhat) - DIPOLE_VEC))


def mag_field_polar(azimuth):

    Rhat = rhat(azimuth)
    Thetahat = thetahat(azimuth)

    cartmag = mag_field_cartesian(azimuth)

    return np.array([np.dot(cartmag, Rhat), np.dot(cartmag, Thetahat)])


def inclination(azimuth):
    return -np.arcsin(mag_field_polar(azimuth)[0] / np.linalg.norm(mag_field_cartesian(azimuth)))


mod_data = np.zeros(11)
for i in range(len(mod_data)):
    mod_data[i] = np.linalg.norm(mag_field_cartesian(ANGLES_ARR[i]))

m, x = np.polyfit(mod_data, EMP_DATA, 1)

print(m, x)

# Plotting
fig, axs = plt.subplots(1)
axs.plot(mod_data, EMP_DATA, 'ro', mod_data, mod_data*m + x)
plt.xlabel("Modelled Data")
plt.ylabel("Empirical Data")
plt.show()

# https://stackoverflow.com/questions/34458251/plot-over-an-image-background-in-python