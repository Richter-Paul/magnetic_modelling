import numpy as np

EARTH_RAD = 6.3e6
MAG_PERM = 1
M = 1


def change_basis(vec, o1, o2):
    '''
    Changes the basis of a vector from its location to some objective origin

    vec: Vector having its basis changed.
    o1: The old 'origin' of vec.
    o2: The new 'origin' of vec 
    '''
    return vec + o1 - o2


def magnitude(vec):
    '''
    Returns the magnitude of a cartesian vector, vec. 
    '''
    return np.sqrt(np.dot(vec, vec))


def cartesian_to_spherical(vec):
    r = magnitude(vec)
    latitude = np.arcsin(vec[2]/r)
    longitude = np.sign(vec[0])*np.arccos(vec[0]/(np.sqrt(vec[0]**2 + vec[1]**2)))

    return np.array([r, latitude, longitude])


def spherical_to_cartesian(r, latitude, longitude):
    
    return np.array([
        r*np.cos(latitude)*np.cos(longitude),
        r*np.cos(latitude)*np.sin(longitude),
        r*np.sin(latitude)
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


def monopole_field(sphvec):
    return MAG_PERM/(4*(np.pi)) * M/(sphvec[0]**2) * rhat(sphvec[1], sphvec[2])


def northpole(pos, latitude, longitude):
    '''
    
    '''
    
    centre = np.array([0, 0, 0])

    # 1.
    earth_cart = spherical_to_cartesian(EARTH_RAD, latitude, longitude)
    # 2.
    monopole_position_cart = change_basis(earth_cart, centre, pos)
    # 3.
    monopole_position_sph = cartesian_to_spherical(monopole_position_cart)
    # 4.
    monopole_f = monopole_field(monopole_position_sph)

    return monopole_f


def southpole(pos, latitude, longitude):
    '''
    Same as northpole, but with a minus sign.
    '''
    
    centre = np.array([0, 0, 0])

    # 1.
    earth_cart = spherical_to_cartesian(EARTH_RAD, latitude, longitude)
    # 2.
    monopole_cart = change_basis(earth_cart, centre, pos)
    # 3.
    monopole_sph = cartesian_to_spherical(monopole_cart)
    # 4.
    monopole_f = monopole_field(monopole_sph)

    return -monopole_f


def magnetic_field_cart(northpos, southpos, latitude, longitude):
    return northpole(northpos, latitude, longitude) + southpole(southpos, latitude, longitude)


def magnetic_field_sph(northpos, southpos, latitude, longitude):
    Rhat = rhat(latitude, longitude)
    Latitudehat = latitudehat(latitude, longitude)

    cartmag = magnetic_field_cart(northpos, southpos, latitude, longitude)

    return np.array([np.dot(cartmag, Rhat), np.dot(cartmag, Latitudehat)])