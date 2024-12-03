import numpy as np
import matplotlib.pyplot as plt
import magnets as m


# Heatmap Test
northpos1 = np.array([1, 0, 1])
southpos1 = np.array([-1, 0, -1])
m1 = 3e31
northpos2 = np.array([0, -0.5, 1])
southpos2 = np.array([0, 0.5, -1])
m2 = 0
#m2 = 2e22

lats = np.linspace(-np.pi/2, np.pi/2, 100)
longs = np.linspace(0, 2*np.pi, 100)
cart = np.zeros((len(lats), len(longs), 3))
sph = np.zeros((len(lats), len(longs), 2))
TMI = np.zeros((len(lats), len(longs)))


for i in range(len(lats)):
    for j in range(len(longs)):
        point = np.array([m.EARTH_RAD, lats[i], longs[j]])
        cart[i, j] = m.magnetic_field_cart(northpos1, southpos1, m1, point) + m.magnetic_field_cart(northpos2, southpos2, m2, point)
        TMI[i, j] = m.TMI(cart[i, j])


# This flips the x-axis (latitudes) because imshow plots upside down :(
flipTMI = np.zeros((len(lats), len(longs)))
for i in range(len(TMI[0])):
    for j in range(len(TMI[1])):
        flipTMI[i, j] = TMI[len(TMI[0]) - 1 - i, j]





#plt.imshow(flipTMI, interpolation='nearest')

img = plt.imread("mercator.jpeg")
x = range(100)

fig, ax = plt.subplots()
ax.imshow(img, extent=[0, 100, 0, 100])
cs = ax.contour(flipTMI, levels=[2e4, 4e4, 5e4, 6e4],
    colors=['#FF0000'], extend='both')
ax.clabel(cs, fontsize=10)
plt.show()