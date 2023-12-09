from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path
import math

day=8
year=2023
test=False
partb=True

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

instructions = None
nodes = {}  # node -> (left,right)

for line in data.splitlines():
    if instructions == None:
        instructions = line.strip()
        continue
    if len(line.strip())>0:
        # AAA = (BBB, CCC)
        node = line.split('=')[0].strip()
        left = line.split('=')[1].replace('(','').replace(',','').replace(')','').split()[0]
        right = line.split('=')[1].replace('(','').replace(',','').replace(')','').split()[1]
        nodes[node] = [left,right]

ans = 0

def get_next_node(curr_node,instruction):
    next_node = None
    match instruction:
        case 'L':
            next_node = nodes[curr_node][0]
        case 'R':
            next_node = nodes[curr_node][1]
        case _:
            print('illegal instruction, ignoring',instruction)
    return next_node

if not partb:
    curr_node = 'AAA'
    instruction_idx = 0
    while curr_node != 'ZZZ':
        curr_node = get_next_node(curr_node,instructions[instruction_idx])
        ans += 1
        instruction_idx = (instruction_idx+1) % len(instructions)

    print('steps to reach ZZZ',ans)

# part b Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes that end with Z
# brute force does not work - even ate dinner while it was running, it did not finish

# a given start node gets to a znode after x steps and the cycle repeats every x steps
# each start node has its own period - number of steps to reach znode
# so we have to find the first time they are all multiples of each other
# raw multiply gives 2 times 10^25, seems too big
# does math.gcd greatest common divisor help us?
# yep, through trial and error with the zperiods, the answer is each zperiod divided by gcd, all multipled together, then multiplied by gcd

def get_steps_to_z(node):
    steps = 0
    instruction_idx = 0
    curr_node = node
    while curr_node[2] != 'Z':
        curr_node = get_next_node(curr_node,instructions[instruction_idx])
        steps += 1
        instruction_idx = (instruction_idx+1) % len(instructions)
    return steps

if partb:
    z_periods = []  # one for each start node
    # all nodes ending in A
    for node in nodes:
        if node[2] == 'A':
            z_periods.append(get_steps_to_z(node))

    gcd = math.gcd(*z_periods)

    ans = 1
    for z_period in z_periods:
        ans *= z_period/gcd

    ans *= gcd

    print('steps for all ghosts to be on nodes ending with Z',int(ans))