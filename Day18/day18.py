# PART TWO NOT STARTED YET
from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path

day=18
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

# part one ignore the colors just count cubic meters
# R 6 (#70c710)

# first let's determine the size of the terrain
max_x = 0
max_y = 0
min_x = 0
min_y = 0

# start at 0,0
curr_x = 0
curr_y = 0
for line in data.splitlines():
    (direction,meters,color) = line.split()
    meters = int(meters)
    match direction:
        case 'R':
            curr_y += meters
            if curr_y>max_y:
                max_y = curr_y
        case 'L':
            curr_y -= meters
            if curr_y<min_y:
                min_y = curr_y
        case 'U':
            curr_x -= meters
            if curr_x<min_x:
                min_x = curr_x
        case 'D':
            curr_x += meters
            if curr_x>max_x:
                max_x = curr_x

num_rows = max_x+1 + abs(min_x)
num_cols = max_y+1 + abs(min_y)
terrain = [['.' for y in range(num_cols)] for x in range(num_rows)]

# is the origin 0,0?
# no we have to normalize all x,y values to start indexing at 0

# moves x from its range of negative numbers into purely positive range
# returns an index that can be used with terrain
def normalized_x(x):
    return x+abs(min_x)

def normalized_y(y):
    return y+abs(min_y)

# now dig the trench boundary
curr_x = normalized_x(0)
curr_y = normalized_y(0)

terrain[curr_x][curr_y] = '#'
for line in data.splitlines():
    (direction,meters,color) = line.split()
    meters = int(meters)
    match direction:
        case 'R':
            for i in range(meters):
                curr_y += 1
                terrain[curr_x][curr_y] = '#'
        case 'L':
            for i in range(meters):
                curr_y -= 1
                terrain[curr_x][curr_y] = '#'
        case 'U':
            for i in range(meters):
                curr_x -= 1
                terrain[curr_x][curr_y] = '#'
        case 'D':
            for i in range(meters):
                curr_x += 1
                terrain[curr_x][curr_y] = '#'

# print out the terrain for visualization
if False:
    for x in range(num_rows):
        s = ''
        for y in range(num_cols):
            s += terrain[x][y]
        print(s)

# now count size of trench including interior
# repurpose the flood fill algorithm from day 10

# mark all . tiles with ? don't know if it's inside or outside
for x in range(num_rows):
    for y in range(num_cols):
        if terrain[x][y] == '.':
            terrain[x][y] = '?'

# start at a spot known to be inside - by visual inspection (ugh)
if test:
    terrain[1][1] = '.'
else:
    terrain[1][229] = '.'

# roam around until have marked all adjacent ? with . as known inside
while True:
    marked_another_inside = False
    for x in range(num_rows):
        for y in range(num_cols):
            if terrain[x][y] == '.':
                # mark any adjacent unknown tiles
                # up
                if x>0 and terrain[x-1][y] == '?':
                    terrain[x-1][y] = '.'
                    marked_another_inside = True
                # down
                if x<num_rows and terrain[x+1][y] == '?':
                    terrain[x+1][y] = '.'
                    marked_another_inside = True
                # left
                if y>0 and terrain[x][y-1] == '?':
                    terrain[x][y-1] = '.'
                    marked_another_inside = True
                # right
                if y<num_cols and terrain[x][y+1] == '?':
                    terrain[x][y+1] = '.'
                    marked_another_inside = True

    if not marked_another_inside:
        break

# now we can count # and .
num_cubes = 0

for row in terrain:
    num_cubes_in_row = 0
    for c in row:
        if c in ('#','.'):
            num_cubes_in_row += 1
    num_cubes += num_cubes_in_row
    #print('size of row in cubic meters',num_cubes_in_row)
    pass

print('size of trench in cubic meters',num_cubes)