'''classes.grid

This module contains grid classes
'''
from .hex import Hex
from math import pow, sqrt
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np


class Hexgrid():
    def __init__(self, radius, x=0, y=0, z=0):
        self.radius = radius
        self.x = x
        self.y = y
        self.z = z
        self.hexes = {}
        self._deltas = [[1,0,-1],[0,1,-1],[-1,1,0],[-1,0,1],[0,-1,1],[1,-1,0]]

        # https://stackoverflow.com/a/2049640
        for r in range(self.radius):
            x = self.x
            y = self.y - r
            z = self.z + r
            num_deltas = len(self._deltas)
            self.hexes[x,y,z] = Hex(x, y, z)

            for j in range(num_deltas):
                if(j == num_deltas-1):
                    num_hex_in_edge = r - 1
                else:
                    num_hex_in_edge = r

                for i in range(num_hex_in_edge):
                    x = x + self._deltas[j][0]
                    y = y + self._deltas[j][1]
                    z = z + self._deltas[j][2]
                    self.hexes[x,y,z] = Hex(x, y, z)

    def print_grid(self):
        fig, ax = plt.subplots(1)
        ax.set_aspect('equal')
        xcoords = []
        ycoords = []
        for i,j,k in self.hexes:
            cur_hex = self.hexes[i,j,k]
            x,y = cur_hex.rect_coords
            xcoords.append(x)
            ycoords.append(y)

            hex = RegularPolygon((x,y), numVertices=6, radius=1,
                                 orientation=np.radians(60), edgecolor='k',
                                 facecolor=cur_hex.color)
            ax.add_patch(hex)

        ax.scatter(xcoords, ycoords, c='k', alpha=0.5)
        plt.show()

    def set_axis(self, ax):
        ax.set_aspect('equal')
        xcoords = []
        ycoords = []
        for i,j,k in self.hexes:
            cur_hex = self.hexes[i,j,k]
            x,y = cur_hex.rect_coords
            xcoords.append(x)
            ycoords.append(y)

            hex = RegularPolygon((x,y), numVertices=6, radius=1,
                                 orientation=np.radians(60), edgecolor='k',
                                 facecolor=cur_hex.color)
            ax.add_patch(hex)

        ax.scatter(xcoords, ycoords, c='k', alpha=0.5)
        return ax
