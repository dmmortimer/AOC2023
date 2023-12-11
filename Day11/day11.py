from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path

day=11
year=2023
test=False

expansion_factor = 2    # part a
#expansion_factor = 10    # part b with test input expected answer 1030
#expansion_factor = 100    # part b with test input expected answer 8410

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

universe = []

# universe consisting of galaxies # and empty space .
for line in data.splitlines():
    universe.append(line)

row_expanded_universe = []

# expand the empty rows and columns
# rows are easier
empty_rows = []     # part b keep a list of empty rows indexes
for x,row in enumerate(universe):
    if '#' not in row:
        for i in range(expansion_factor):
            row_expanded_universe.append(row)
        empty_rows.append(x)
    else:
        row_expanded_universe.append(row)

# columns - first find indexes of empty columns
empty_columns = []
for y in range(len(universe[0])):
    col = [ row[y] for row in universe]
    if '#' not in col:
        empty_columns.append(y)

expanded_universe = []

# now insert empty column(s) at each spot
for row in row_expanded_universe:
    expanded_row = []
    for idx,c in enumerate(row):
        expanded_row.append(c)
        if idx in empty_columns:
            for i in range(expansion_factor-1):
                expanded_row.append('.')
    expanded_universe.append(expanded_row)

max_row = len(expanded_universe)
max_col = len(expanded_universe[0])

# galaxies
# instructions use numbers starting from 1 so add 1 to index if displaying galaxy number
galaxies = []
for x in range(max_row):
    for y in range(max_col):
        if expanded_universe[x][y] == '#':
            galaxies.append((x,y))

# find the shortest path between every pair of galaxies
# distance = |x2 - x1| + |y2 - y1|
def sum_galaxy_distances(galaxies):
    ans = 0

    num_galaxies = len(galaxies)
    print(num_galaxies,'galaxies')

    for g1 in range(num_galaxies):
        for g2 in range(g1+1,num_galaxies):
            d = abs(galaxies[g1][0] - galaxies[g2][0]) + \
            abs(galaxies[g1][1] - galaxies[g2][1])
            #print('Between galaxy',g1+1,'and galaxy',g2+1,':',d)
            ans += d
    return ans

print('sum of shortest path between every pair of galaxies, expansion factor',expansion_factor, ':',sum_galaxy_distances(galaxies))

# part b need a different way to find and store galaxy location
galaxies = []

# have indices of empty rows and columns
# use these to adjust the x and y coordinates of the galaxies we find

expansion_factor = 1000000
max_row = len(universe)
max_col = len(universe[0])

for x in range(max_row):
    for y in range(max_col):
        if universe[x][y] == '#':
            # how many empty rows above us?
            n = sum(1 for r in empty_rows if r < x)
            expanded_x = x + n*(expansion_factor-1)
            # how many empty columns left of us?
            n = sum(1 for r in empty_columns if r < y)
            expanded_y = y + n*(expansion_factor-1)
            galaxies.append((expanded_x,expanded_y))

print('sum of shortest path between every pair of galaxies, expansion factor',expansion_factor, ':',sum_galaxy_distances(galaxies))