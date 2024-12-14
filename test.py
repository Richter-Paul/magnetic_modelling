import numpy as np
import matplotlib.pyplot as plt
import magnets as m


northpos1 = np.array([0, -0.5, 1])
southpos1 = np.array([0, 0.5, -1])
m1 = 1.75e31
northpos2 = np.array([1e6, 1e6, 1])
southpos2 = np.array([1e6, 1e6, -1])
m2 = 2e31

lats = np.linspace(-np.pi/2, np.pi/2, 100)
longs = np.linspace(0, 2*np.pi, 100)
cart = np.zeros((len(lats), len(longs), 3))
sph = np.zeros((len(lats), len(longs), 2))
TMI = np.zeros((len(lats), len(longs)))


for i in range(len(lats)):
    for j in range(len(longs)):
        point = np.array([m.EARTH_RAD, lats[i], longs[j]])
        cart[i, j] = m.magnetic_field_cart(northpos1, southpos1, m1, point) + m.magnetic_field_cart(northpos2, southpos2, m2, point)
        sph[i, j] = m.magnetic_field_sph(northpos1, southpos1, m1, point) + m.magnetic_field_sph(northpos2, southpos2, m2, point)
        TMI[i, j] = m.TMI(cart[i, j])


# This flips the y-axis (longitudes) because imshow plots upside down :(
flipTMI = np.zeros((len(lats), len(longs)))
for i in range(len(TMI[0])):
    for j in range(len(TMI[1])):
        flipTMI[i, j] = TMI[i, len(TMI[1]) - 1 - j]

flipsph = np.zeros((len(lats), len(longs), 2))
for i in range(len(sph[0])):
    for j in range(len(sph[1])):
        flipsph[i, j] = sph[i, len(sph[1]) - 1 - j]




#plt.imshow(flipTMI, interpolation='nearest')

img = plt.imread("mercator.jpeg")
x = range(100)

lev = np.arange(0, 1e6, 5000)

fig, ax = plt.subplots()
ax.imshow(img, extent=[0, 100, 0, 100])
cs = ax.contour(flipTMI, levels=lev,
    colors=['#FF0000'], extend='both')
ax.clabel(cs, fontsize=10)



img = plt.imread("mercator.jpeg")
x = range(100)

lev = np.arange(-1e6, 1e6, 5000)

fig, ax = plt.subplots()
ax.imshow(img, extent=[0, 100, 0, 100])
cs = ax.contour(flipsph[:, :, 0], levels=lev,
    colors=['#FF0000'], extend='both')
ax.clabel(cs, fontsize=10)
plt.show()