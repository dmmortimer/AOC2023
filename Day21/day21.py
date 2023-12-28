# PART TWO NOT STARTED
#from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path

day=21
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = open(os.path.join(os.path.dirname(__file__),'input.txt')).read()
    #data = get_data(year=year,day=day)

map = []

for line in data.splitlines():
	map.append(list(line.strip()))

num_rows = len(map)
num_cols = len(map[0])

print('Land dimensions',num_rows,'by',num_cols)

start_x = 0
start_y = 0

# find start and mark it as a garden plot
for x in range(num_rows):
	for y in range(num_cols):
		if map[x][y] == 'S':
			start_x = x
			start_y = y
			map[x][y] = '.'

print('Start at',start_x,start_y)

# garden plots reachable in exactly idx+1 steps
# list of sets containing plots identified by x,y
reachable_plots = []

num_steps = 6	# test
if not test:
	num_steps = 64

for i in range(num_steps):
	# find spots we can get to in one step from spots we could get to in the previous step
	# up/down/left/right if within map boundaries and not a rock
	previous_plots = []
	if i == 0:
		previous_plots = [(start_x,start_y)]
	else:
		previous_plots = reachable_plots[i-1]
	next_plots = set()
	for (x,y) in previous_plots:
		# up
		if x>0 and map[x-1][y] == '.':
			next_plots.add((x-1,y))
		# down
		if x<num_rows+1 and map[x+1][y] == '.':
			next_plots.add((x+1,y))
		# left
		if y>0 and map[x][y-1] == '.':
			next_plots.add((x,y-1))
		# right
		if y<num_cols+1 and map[x][y+1] == '.':
			next_plots.add((x,y+1))
	reachable_plots.append(next_plots)
	#print('After exactly',i+1,'steps, can reach',len(reachable_plots[i]),'garden plots')
	#print(reachable_plots[i])

print('After exactly',num_steps,'steps, can reach',len(reachable_plots[-1]),'garden plots')
