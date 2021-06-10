'''utils.funcs

This module contains util functions
'''
from classes.hex import Hex
import numpy as np


def face_hex_to_cube(face, hex, hexes_per_face):
    # Faces 1 and 4 have max of |z|
    # Faces 2 and 5 have max of |x|
    # Faces 3 and 6 have max of |y|
    x = 0
    y = 0
    z = 0
    if(face == 0 or face == 3):
        multiplier = 1 if face == 3 else -1
        z = (hexes_per_face - 1) * multiplier
        y = (hexes_per_face - 1 - hex) * -multiplier
        x = hex * -multiplier
    elif(face == 1 or face == 4):
        multiplier = 1 if face == 1 else -1
        x = (hexes_per_face - 1) * multiplier
        z = (hexes_per_face - 1 - hex) * -multiplier
        y = hex * -multiplier
    else:
        multiplier = 1 if face == 5 else -1
        y = (hexes_per_face - 1) * multiplier
        x = (hexes_per_face - 1 - hex) * -multiplier
        z = hex * -multiplier

    return (x,y,z)


def cube_line(hex1, hex2):
    '''
    This function returns all hexes between two input hexes in a line.

    Parameters:
        :param hex1: (Hex) A hex object
        :param hex2: (Hex) A hex object

    Returns:
        list: A list containing all coordinates in the line
    '''
    distance = int(Hex.cube_distance(hex1, hex2))
    dx = hex2.x - hex1.x
    dy = hex2.y - hex1.y
    dz = hex2.z - hex1.z
    interval = 1.0 / distance
    curr_offset = 0.0
    retval = []

    # We need to add one for i to be [0,distance]
    for i in range(distance+1):
        retval.append(Hex.cube_round(
            hex1.x + (dx * curr_offset),
            hex1.y + (dy * curr_offset),
            hex1.z + (dz * curr_offset)
        ))

        curr_offset += interval

    return retval

def wedge_hex(wedge, row, index, max_rows):
    '''
    This method returns the cubic coordinates of a hex in the specified
    wedge, row, and index.

    row is 0-indexed
    '''
    print('{} {} {}'.format(row, max_rows, row % max_rows))
    row = row % max_rows
    # This loop may be complicated
    x = 0
    y = 0
    z = 0

    if(wedge == 0):
        # Z is maximal and negative
        # Starting off x is the opposite of z and y is 0
        z = -row
        x = row
    elif(wedge == 1):
        # X is maximal and positive
        # Starting off y is the opposite of x and z is 0
        x = row
        y = -row
    elif(wedge == 2):
        # Y is maximal and negative
        # Starting off z is the opposite of y and x is 0
        y = -row
        z = row
    elif(wedge == 3):
        # Opposite of Wedge 0
        z = row
        x = -row
    elif(wedge == 4):
        # Opposite of Wedge 1
        x = -row
        y = row
    else:
        # Opposite of Wedge 2
        y = row
        z = -row

    # Dear god it is going to be
    print('Start: {} {} {}'.format(x, y, z))
    for step in range(index):
        # Step along row
        if(wedge == 0 or wedge == 3):
            # Increment y/x and decrement the other
            if(wedge == 0):
                x -= 1
                y += 1
            else:
                x += 1
                y -= 1
        elif(wedge == 1 or wedge == 4):
            # Increment y/z and decrement the other
            if(wedge == 1):
                y += 1
                z -= 1
            else:
                y -= 1
                z += 1
        else:
            # Increment x/z and decrement the other
            if(wedge == 2):
                x += 1
                z -= 1
            else:
                x -= 1
                z += 1
        
        print('Cur: {} {} {}'.format(x, y, z))

        # Now check to see if we overstepped
        overstepped = False
        if(wedge == 0 or wedge == 3):
            if(max(abs(x),abs(y)) > abs(z)):
                overstepped = True
        elif(wedge == 1 or wedge == 4):
            if(max(abs(z),abs(y)) > abs(x)):
                overstepped = True
        else:
            if(max(abs(x),abs(z)) > abs(y)):
                overstepped = True

        if(overstepped):
            # We did, up the row and reset
            if(wedge == 0):
                z -= 1
                if(abs(z) == max_rows):
                    z = 0
                x = -z
                y = 0
            elif(wedge == 1):
                x += 1
                if(abs(x) == max_rows):
                    x = 0
                y = -x
                z = 0
            elif(wedge == 2):
                y += 1
                if(abs(y) == max_rows):
                    y = 0
                z = -y
                x = 0
            elif(wedge == 3):
                z += 1
                if(abs(z) == max_rows):
                    z = 0
                x = -z
                y = 0
            elif(wedge == 4):
                x -= 1
                if(abs(x) == max_rows):
                    x = 0
                y = -x
                z = 0
            else:
                y -= 1
                if(abs(y) == max_rows):
                    y = 0
                z = -y
                x = 0
            print('  Overstep {} {} {}'.format(x, y, z))

    return (x, y, z)