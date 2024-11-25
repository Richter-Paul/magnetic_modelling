import numpy as np
import matplotlib.pyplot as plt
import magnets as m


# Heatmap Test
northpos = np.array([2, 10, 10])
southpos = np.array([-2, -10, -10])

lats = np.linspace(-np.pi/2, np.pi/2, 100)
longs = np.linspace(0, 2*np.pi, 100)
cart = np.zeros((len(lats), len(longs), 3))
sph = np.zeros((len(lats), len(longs), 2))
TMI = np.zeros((len(lats), len(longs)))


for i in range(len(lats)):
    for j in range(len(longs)):
        point = np.array([m.EARTH_RAD, lats[i], longs[j]])
        cart[i, j] = m.magnetic_field_cart(northpos, southpos, point)
        TMI[i, j] = m.TMI(cart[i, j])


# This just flips the y-axis (latitudes) for plotting
flipTMI = np.zeros((len(longs), len(lats)))
for i in range(len(TMI[0])):
    for j in range(len(TMI[1])):
        flipTMI[i, j] = TMI[i, len(TMI[1]) - 1 - j]


plt.imshow(flipTMI, interpolation='nearest')

cs = plt.contour(flipTMI, levels=[1e-26, 1.2e-26, 1.4e-26, 1.6e-26, 1.66e-26],
    colors=['#808080', '#A0A0A0', '#C0C0C0'], extend='both')
cs.cmap.set_over('red')
cs.cmap.set_under('blue')
cs.changed()
plt.show()
