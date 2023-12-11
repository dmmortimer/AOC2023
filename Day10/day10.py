from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path
from collections import deque

day=10
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input-7.txt')).read()
else:
    data = get_data(year=year,day=day)


tiles = []  # | - L J 7 F .
start = None
for x,line in enumerate(data.splitlines()):
    tiles.append(line)
    for y,c in enumerate(line):
        if c == 'S':
            start = (x,y)

max_x = len(tiles)-1
max_y = len(tiles[0])-1

# find the tile in the loop that is farthest from the starting position

# is there a pipe going up from this position
def connected_up(pos):
    (x,y) = pos
    if x>0:
        if tiles[x-1][y] in ('|','7','F'):
            return True
    return False

def connected_down(pos):
    (x,y) = pos
    if x<max_x:
        if tiles[x+1][y] in ('|','L','J'):
            return True
    return False

def connected_left(pos):
    (x,y) = pos
    if y>0:
        if tiles[x][y-1] in ('-','L','F'):
            return True
    return False

def connected_right(pos):
    (x,y) = pos
    if y<max_y:
        if tiles[x][y+1] in ('-','J','7'):
            return True
    return False

# figure out what kind of tile we're starting on
# start tile always has exactly two ways out
def get_start_tile_pipe(pos):
    (x,y) = start
    if connected_up(pos) and connected_down(pos):
        return '|'
    if connected_left(pos) and connected_right(pos):
        return '-'
    if connected_up(pos) and connected_right(pos):
        return 'L'
    if connected_up(pos) and connected_left(pos):
        return 'J'
    if connected_left(pos) and connected_down(pos):
        return '7'
    if connected_right(pos) and connected_down(pos):
        return 'F'
    return None

# guaranteed only one way out of here given how we got in, return that
def get_next_tile(pos,prev_pos):
    (x,y) = pos
    pipe = tiles[x][y]
    match pipe:
        case '|':
            # up
            if connected_up(pos) and (x-1,y) != prev_pos:
                return((x-1,y))
            # down
            if connected_down(pos) and (x+1,y) != prev_pos:
                return((x+1,y))
        case '-':
            # left
            if connected_left(pos) and (x,y-1) != prev_pos:
                return((x,y-1))
            # right
            if connected_right(pos) and (x,y+1) != prev_pos:
                return((x,y+1))
        case 'L':
            # up
            if connected_up(pos) and (x-1,y) != prev_pos:
                return((x-1,y))
            # right
            if connected_right(pos) and (x,y+1) != prev_pos:
                return((x,y+1))
        case 'J':
            # up
            if connected_up(pos) and (x-1,y) != prev_pos:
                return((x-1,y))
            # left
            if connected_left(pos) and (x,y-1) != prev_pos:
                return((x,y-1))
        case '7':
            # left
            if connected_left(pos) and (x,y-1) != prev_pos:
                return((x,y-1))
            # down
            if connected_down(pos) and (x+1,y) != prev_pos:
                return((x+1,y))
        case 'F':
            # right
            if connected_right(pos) and (x,y+1) != prev_pos:
                return((x,y+1))
            # down
            if connected_down(pos) and (x+1,y) != prev_pos:
                return((x+1,y))
    # unexpected
    assert(False)

# part a
# fill in type of start tile
tiles[start[0]] = tiles[start[0]].replace('S',get_start_tile_pipe(start))

# for part b
# mark all tiles with ? don't know, O outside, or the tile type |-7LjF if it's part of the loop
marked_tiles = [['?' for y in range(max_y+1)] for x in range(max_x+1)]

curr_pos = start
prev_pos = None
returned_to_start = False
steps = 0
while not returned_to_start:
    # step to next tile - doesn't matter which direction as long as we never go backwards
    next_pos = None
    # has to be exactly two possible paths out - find one and go there if we haven't gone there before
    next_pos = get_next_tile(curr_pos,prev_pos)

    prev_pos = curr_pos
    curr_pos = next_pos
    marked_tiles[curr_pos[0]][curr_pos[1]] = tiles[curr_pos[0]][curr_pos[1]]    # part of the loop
    steps += 1
    if curr_pos == start:
        returned_to_start = True

assert steps % 2 == 0   # otherwise we might need to mess with rounding
ans = int(steps/2)
print('steps from starting position to farthest tile in loop',ans)

# part b
# how many (ground or junk pipe) tiles are contained within the loop
# mark all tiles with ? don't know, O outside, |-LJ7F  loop
# when we can't add any more O then all the ? are inside

# start at a spot known to be outside - by visual inspection
# this could change with each set of data, ugh
assert(marked_tiles[0][0] == '?')   # guard against a loop that goes through this tile
marked_tiles[0][0] = 'O'

# round 1 mark the obviously-outside tiles, not considering squeezing
while True:
    marked_another_outside = False
    for x,tile in enumerate(tiles):
        for y,t in enumerate(tile):
            if marked_tiles[x][y] == 'O':
                # mark any adjacent outside tiles - not blocked by a pipe that's part of the loop
                # up
                if x>0 and marked_tiles[x-1][y] == '?':
                    marked_tiles[x-1][y] = 'O'
                    marked_another_outside = True
                # down
                if x<max_x and marked_tiles[x+1][y] == '?':
                    marked_tiles[x+1][y] = 'O'
                    marked_another_outside = True
                # left
                if y>0 and marked_tiles[x][y-1] == '?':
                    marked_tiles[x][y-1] = 'O'
                    marked_another_outside = True
                # right
                if y<max_y and marked_tiles[x][y+1] == '?':
                    marked_tiles[x][y+1] = 'O'
                    marked_another_outside = True

    if not marked_another_outside:
        break

# we now have marked_tiles where O = known outside tile, |-7LJF = loop pipe tile, and ? = suspected inside tile

# count remaining ? tiles, couldn't reach them from outside (without considering squeezing)
ans = 0
for tile in marked_tiles:
    for t in tile:
        if t == '?':
            ans += 1

print('number of tiles inside the loop, ignoring squeezing',ans)

# round 2 consider squeezing
# repeat a similar algorithm but with quadrants instead of tiles

# quadrants with z index 0=top left 1=top right 2=bottom left 3=bottom right
# each tile has four quadrants
marked_quadrants = [[['?' for z in range(4)] for y in range(max_y+1)] for x in range(max_x+1)]

# first, if we already know it's outside, mark all 4 quadrants
for x,tile in enumerate(marked_tiles):
    for y,t in enumerate(tile):
        if t == 'O':
            for z in range(4):
                marked_quadrants[x][y][z] = 'O'

def mark_quadrant(x,y,z):
    marked_quadrants[x][y][z] = 'O'

# now explore to mark adjacent quadrants as outside
while True:
    marked_another_outside = False
    for x,tile in enumerate(marked_tiles):
        for y,t in enumerate(tile):
            # top left quadrant z = 0
            if marked_quadrants[x][y][0] == 'O':
                # mark any adjacent outside quadrants, watching for loop pipes blocking the way
                # up
                if x>0 and marked_quadrants[x-1][y][2] == '?':
                    mark_quadrant(x-1,y,2)
                    marked_another_outside = True
                # down, same tile
                if t not in '-J7' and marked_quadrants[x][y][2] == '?':
                    mark_quadrant(x,y,2)
                    marked_another_outside = True
                # left
                if y>0 and marked_quadrants[x][y-1][1] == '?':
                    mark_quadrant(x,y-1,1)
                    marked_another_outside = True
                # right, same tile
                if t not in '|LJ' and marked_quadrants[x][y][1] == '?':
                    mark_quadrant(x,y,1)
                    marked_another_outside = True
            # top right quadrant z = 1
            if marked_quadrants[x][y][1] == 'O':
                # mark any adjacent outside quadrants, watching for loop pipes blocking the way
                # up
                if x>0 and marked_quadrants[x-1][y][3] == '?':
                    mark_quadrant(x-1,y,3)
                    marked_another_outside = True
                # down, same tile
                if t not in '-LF' and marked_quadrants[x][y][3] == '?':
                    mark_quadrant(x,y,3)
                    marked_another_outside = True
                # left, same tile
                if t not in '|LJ' and marked_quadrants[x][y][0] == '?':
                    mark_quadrant(x,y,0)
                    marked_another_outside = True
                # right
                if y<max_y and marked_quadrants[x][y+1][0] == '?':
                    mark_quadrant(x,y+1,0)
                    marked_another_outside = True
            # bottom left quadrant z = 2
            if marked_quadrants[x][y][2] == 'O':
                # mark any adjacent outside quadrants, watching for loop pipes blocking the way
                # up, same tile
                if t not in '7J-' and marked_quadrants[x][y][0] == '?':
                    mark_quadrant(x,y,0)
                    marked_another_outside = True
                # down
                if x<max_x and marked_quadrants[x+1][y][0] == '?':
                    mark_quadrant(x+1,y,0)
                    marked_another_outside = True
                # left
                if y>0 and marked_quadrants[x][y-1][3] == '?':
                    mark_quadrant(x,y-1,3)
                    marked_another_outside = True
                # right, same tile
                if t not in '|7F' and marked_quadrants[x][y][3] == '?':
                    mark_quadrant(x,y,3)
                    marked_another_outside = True
            # bottom right quadrant z = 3
            if marked_quadrants[x][y][3] == 'O':
                # mark any adjacent outside quadrants, watching for loop pipes blocking the way
                # up, same tile
                if t not in '-LF' and marked_quadrants[x][y][1] == '?':
                    mark_quadrant(x,y,1)
                    marked_another_outside = True
                # down
                if x<max_x and marked_quadrants[x+1][y][1] == '?':
                    mark_quadrant(x+1,y,1)
                    marked_another_outside = True
                # left, same tile
                if t not in '|7F' and marked_quadrants[x][y][2] == '?':
                    mark_quadrant(x,y,2)
                    marked_another_outside = True
                # right
                if y<max_y and marked_quadrants[x][y+1][2] == '?':
                    mark_quadrant(x,y+1,2)
                    marked_another_outside = True
    if not marked_another_outside:
        break

# now we can update marked_tiles with the newly discovered outside tiles
for x,tile in enumerate(marked_tiles):
    for y,t in enumerate(tile):
        if t == '?':
            # if all quadrants are still unreached, then this tile is not reachable
            # also if one is marked they all must be marked since this is not a loop tile
            if marked_quadrants[x][y][0] == 'O':
                assert marked_quadrants[x][y][1] == 'O'
                assert marked_quadrants[x][y][2] == 'O'
                assert marked_quadrants[x][y][3] == 'O'
                marked_tiles[x][y] = 'O'

# count again
ans = 0
for tile in marked_tiles:
    for t in tile:
        if t == '?':
            ans += 1

print('number of tiles inside the loop, considering squeezing',ans)