# PART TWO NOT STARTED
from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path

day=16
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

layout = []
for line in data.splitlines():
    layout.append(line.strip())


num_rows = len(layout)
num_cols = len(layout[0])

print('layout has',num_rows,'rows',num_cols,'columns')
energized = [[0 for y in range(num_cols)] for x in range(num_rows)]

# keep track of which direction the light shone at this tile - to prevent light bouncing back and forth forever
energize_directions = [[[] for y in range(num_cols)] for x in range(num_rows)]

# recursive function that shines from this location, with a beam initially in this direction
# beam direction is one of (l)eft, (r)ight, (u)p, (d)own
def shine(x,y,direction):

    # first check if we've gone outside the boundaries
    if x not in range(num_rows) or y not in range(num_cols):
        return

    # then check if we've shone from this tile in the same direction already
    if energized[x][y]:
        #print('been here before',x,y, 'from directions',energize_directions[x][y])
        if direction in energize_directions[x][y]:
            #print('current direction',direction,'already explored, nothing to do')
            return

    # energize in this direction
    energize_directions[x][y].append(direction)

    # move, energizing and checking boundaries, until the beam splits
    while True:

        energized[x][y] = 1

        next_x = x
        next_y = y
        next_direction = direction

        match layout[x][y]:
            case '.':
                match direction:
                    case 'l':
                        next_y = y-1
                    case 'r':
                        next_y = y+1
                    case 'u':
                        next_x = x-1
                    case 'd':
                        next_x = x+1
            case '|':
                match direction:
                    case 'l' | 'r':
                        shine(x-1,y,'u')
                        shine(x+1,y,'d')
                        break
                    case 'u':
                        next_x = x-1
                    case 'd':
                        next_x = x+1
            case '-':
                match direction:
                    case 'u' | 'd':
                        shine(x,y-1,'l')
                        shine(x,y+1,'r')
                        break
                    case 'l':
                        next_y = y-1
                    case 'r':
                        next_y = y+1
            case '/':
                match direction:
                    case 'l':
                        next_x = x+1
                        next_direction = 'd'
                    case 'r':
                        next_x = x-1
                        next_direction = 'u'
                    case 'u':
                        next_y = y+1
                        next_direction = 'r'
                    case 'd':
                        next_y = y-1
                        next_direction = 'l'
            case '\\':
                match direction:
                    case 'l':
                        next_x = x-1
                        next_direction = 'u'
                    case 'r':
                        next_x = x+1
                        next_direction = 'd'
                    case 'u':
                        next_y = y-1
                        next_direction = 'l'
                    case 'd':
                        next_y = y+1
                        next_direction = 'r'

        if next_x not in range(num_rows) or next_y not in range(num_cols):
            # next move takes us out of bounds, nothing more to follow
            return
        # keep going
        x = next_x
        y = next_y
        direction = next_direction
        
shine(0,0,'r')

ans = 0
for row in energized:
    ans += sum(row)

print('number of energized tiles:',ans)