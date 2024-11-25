import numpy as np
import astropy.coordinates as coords

EARTH_RAD = 6.3e6
MAG_PERM = 1.26e-6
M = 1
CENTRE = np.zeros(3)


'''
NOTE on vectors:

Throughout this code, there are cartesian vectors, 'vec', and spherical vectors, 'sphvec'.
vec are simple [x, y, z], sphvec are [modulus (or r), latitude, longitude].

It's worth noting that sphvec doesn't actually follow the math OR physics conventions for
spherical vectors; math would normally use [modulus, longitude, colatitude], 
and physics would use [modulus, colatitude, longitude].
'''


def magnitude(vec):
    '''
    Returns the magnitude/modulus of a cartesian vector, vec. 
    '''
    return np.sqrt(np.dot(vec, vec))


def change_origin(vec, o1, o2):
    '''
    Returns a vector from a new 'origin' (o2) to the tip of the original vector (vec).
    This is all for cartesian. 

    vec: Vector having its basis changed.
    o1: The old 'origin' of vec.
    o2: The new 'origin' of vec 
    '''

    return vec + o1 - o2


def cartesian_to_spherical(vec):

    r = magnitude(vec)
    latitude = np.arcsin(vec[2]/r)
    longitude = np.sign(vec[1])*np.arccos(vec[0]/(np.sqrt(vec[0]**2 + vec[1]**2)))

    return np.array([r, latitude, longitude])


def spherical_to_cartesian(sphvec):
    
    return np.array([
        sphvec[0]*np.cos(sphvec[1])*np.cos(sphvec[2]),
        sphvec[0]*np.cos(sphvec[1])*np.sin(sphvec[2]),
        sphvec[0]*np.sin(sphvec[1])
        ])


def rhat(latitude, longitude):
    '''
    Returns the unit vector pointing away from center of spherical system
    '''

    return np.array([np.cos(latitude)*np.cos(longitude),
                     np.cos(latitude)*np.sin(longitude),
                     np.sin(latitude)
                     ])


# I know that this function name is awful. I'm sorry. 
def latitudehat(latitude, longitude):
    '''
    Unit vector of latitude on surface of sphere by day,
    derivative of position w.r.t latitude by night.
    '''

    return np.array([-np.sin(latitude)*np.cos(longitude), 
                     -np.sin(latitude)*np.sin(longitude),
                     np.cos(latitude)
                     ])


def monopole(sphvec):
    '''
    Returns the force of a magnetic monopole at a longitude and latitude
    relative to the monopole center.
    '''

    return MAG_PERM/(4*(np.pi)) * M/(sphvec[0]**2) * rhat(sphvec[1], sphvec[2])


def magnetic_field_cart(northpos, southpos, sphvec):
    '''
    Converts the effect of two monopoles at arbitrary locations to their net
    effect at the given latitude and longitude ("the point") on the Earth's surface.

    1. Converts the point to a cartesian coordinate
    2. Finds the cartesian position of the point relative to the poles
    3. Finds the spherical position of the point relative to the poles
    4. Finds the magnetic fields from the poles
    
    Finally, returns the vector sum of the fields. 
    '''

    # 1.
    vec = spherical_to_cartesian(sphvec)
    # 2.
    northpole_pos_cart = change_origin(vec, CENTRE, northpos)
    southpole_pos_cart = change_origin(vec, CENTRE, southpos)
    # 3.
    northpole_pos_sph = cartesian_to_spherical(northpole_pos_cart)
    southpole_pos_sph = cartesian_to_spherical(southpole_pos_cart)
    # 4.
    northpole = monopole(northpole_pos_sph)
    southpole = -monopole(southpole_pos_sph)

    return northpole + southpole


def magnetic_field_sph(northpos, southpos, sphvec):
    '''
    Returns the magnetic field in radial and latitude basis vectors.
    '''
    Rhat = rhat(sphvec[1], sphvec[2])
    Latitudehat = latitudehat(sphvec[1], sphvec[2])
    cartmag = magnetic_field_cart(northpos, southpos, sphvec)

    return np.array([np.dot(cartmag, Rhat), -np.dot(cartmag, Latitudehat)])


def TMI(magfield):
    return magnitude(magfield)


def inclination(magfieldsph):
    return np.arctan(magfieldsph[0]/magfieldsph[1])