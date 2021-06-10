from classes.grid import Hexgrid
from classes.hex import Hex
from utils.funcs import face_hex_to_cube, cube_line, wedge_hex
import numpy as np
import matplotlib.pyplot as plt

grid_size = 5
grids = []
num_grids = 16
num_cols = 4
num_rows = 4

num_rivers = 1
num_mountains = 2
num_forests = 1
forest_radius = 1

# generate some grids
for i in range(num_grids):
    grid = Hexgrid(grid_size)

    # Generate rivers
    for river in range(num_rivers):
        river_loop = True
        start_coords = None
        end_coords = None
        while(river_loop):
            # Try these out
            start_face = np.random.randint(0, 6)
            start_hex = np.random.randint(0, grid_size)
            end_face = np.random.randint(0, 6)
            end_hex = np.random.randint(0, grid_size)

            if(start_face is end_face):
                continue

            # Check if we ended up picking the same hex
            # This would happen if the cubic distance between them is 0
            start_coords = face_hex_to_cube(start_face, start_hex, grid_size)
            end_coords = face_hex_to_cube(end_face, end_hex, grid_size)
            if(Hex.cube_distance(Hex(*start_coords), Hex(*end_coords)) < 1):
                continue

            # If we are here, we are good
            river_loop = False

        # Get all hexes in the line
        river_hexes = cube_line(Hex(*start_coords), Hex(*end_coords))

        # Change the colors of these hexes to be river colored
        for hex in river_hexes:
            grid.hexes[hex].color = '#0343df'

    # Generate Mountains
    for mountain in range(num_mountains):
        # First pick a wedge, row, and index
        wedge = np.random.randint(0, 6)
        row = np.random.randint(0, 6)
        index = np.random.randint(0, 6)

        # Get coordinates
        mountain_coords = wedge_hex(wedge, row, index, grid_size)
        print('{} {} {} - {}'.format(wedge, row, index, mountain_coords))

        grid.hexes[mountain_coords].color = '#ad8150'

    # Generate Forests
    for forest in range(num_forests):
        # First pick a wedge, row, and index
        wedge = np.random.randint(0, 6)
        row = np.random.randint(0, 6)
        index = np.random.randint(0, 6)

        # Get forest center coordinates
        forest_coords = wedge_hex(wedge, row, index, grid_size)

        # Get all hexes within range of this
        forest_hexes = Hex.hex_range(Hex(*forest_coords), forest_radius)

        # Loop through them to add them!
        for hex in forest_hexes:
            # Derefernce for convience
            x,y,z = hex

            # Check to see if this hex is outside our area
            if(max(abs(x), abs(y), abs(z)) >= grid_size):
                # Yep
                continue

            grid.hexes[hex].color = '#15b01a'


    # Add this grid
    grid.hexes[0,0,0].color = '#ffff14'
    grids.append(grid)
    
# Lets make the plot and add everything to it
fig, axes = plt.subplots(num_rows, num_cols)
fig.suptitle('Example Maps')
cur_plot = 0
for cur_row in range(num_rows):
    for cur_col in range(num_cols):
        ax = axes[cur_row, cur_col]
        ax = grids[cur_plot].set_axis(ax)
        cur_plot += 1

plt.show()