# PART TWO NOT STARTED
from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path

day=14
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

platform = []
for line in data.splitlines():
    platform.append(list(line))

# Tilt the lever so all of the rocks will slide north as far as they will go
# Rounded rocks move up until they reach another rock
# Work top down, eliminating spaces
num_rows = len(platform)
num_cols = len(platform[0])
for y in range(num_cols):
    for x in range(num_rows):
        if platform[x][y] == 'O':
            # move up as far as possible turning spaces to rocks and emptying previous space
            # stop when we find find first rock or wall above this spot
            if x>0:
                new_location = x
                for idx in range(x-1,-1,-1):
                    if platform[idx][y] == '.':
                        new_location = idx
                    else:
                        break
                if new_location != x:
                    # we're moving
                    platform[new_location][y] = 'O'
                    platform[x][y] = '.'
pass

# The total load is the sum of the load caused by all of the rounded rocks
def calculate_load(platform):
    load = 0
    num_rows = len(platform)
    for idx,row in enumerate(platform):
        for rock in row:
            if rock == 'O':
                load += (num_rows-idx)
    return load

print('total load on north support beams',calculate_load(platform))

# part two
# spin cycle tilts the platform north, then west, then south, then east
# do 1 million spin cycles
# seems like a given rock ends up settling. can we find each rock's final resting place?