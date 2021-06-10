'''classes.hex

This module contains the hex class
'''
from collections import namedtuple
import numpy as np

class Hex(namedtuple('Hex',['x','y','z'])):
    # Member variables
    x: int
    y: int
    z: int

    def __new__(cls, x, y, z, color='#96f97b'):
        self = super(Hex, cls).__new__(cls, x, y, z)
        self.color = color
        return self

    @property
    def rect_coords(self):
        return Hex.hex_to_rect(self.x, self.y, self.z)

    @staticmethod
    def cube_to_axial(x, y, z):
        return (x, z)
    
    @staticmethod
    def axial_to_cube(q, r):
        return (q, -q - r, r)

    @staticmethod
    def hex_to_rect(x,y,z):
        q, r = Hex.cube_to_axial(x,y,z)
        return(
            (np.sqrt(3) * q) + (np.sqrt(3) * r) / 2.0,
            3.0 * r / 2
        )

    @staticmethod
    def rect_to_hex(rect_x, rect_y):
        q = np.sqrt(3) * rect_x / 3.0 - rect_y / 3.0
        r = 2.0 * rect_y / 3.0
        return(Hex.axial_to_cube(q, r))

    @staticmethod
    def cube_distance(hex1, hex2):
        return (abs(hex1.x - hex2.x) + abs(hex1.y - hex2.y) + abs(hex1.z - hex2.z)) / 2

    @staticmethod
    def cube_round(x, y, z):
        '''
        This method rounds the input coordinates to the nearest cubic coordinate
        '''
        rx = round(x)
        ry = round(y)
        rz = round(z)

        dx = abs(rx - x)
        dy = abs(ry - y)
        dz = abs(rz - z)

        if(dx > dy and dx > dz):
            rx = -ry - rz
        elif(dy > dz):
            ry = -rx - rz
        else:
            rz = -rx - ry

        return (rx, ry, rz)

    @staticmethod
    def hex_range(hex, radius):
        '''
        This method returns all hexes within the radius of the specified hex
        '''
        retval = []
        # Move through x values, we have to increase radius by 1 for inclusivity
        for x in range(-radius, radius+1):
            # Only specific Y values will work with the given x and be in radius
            for y in range(max(-radius, -x - radius), min(radius+1, -x + radius + 1)):
                # We can calculate the z that works for this x,y
                z = -x - y
                retval.append((hex.x + x, hex.y + y, hex.z + z))

        return retval
