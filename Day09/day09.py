from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path
from collections import deque

day=9
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

histories = []

for line in data.splitlines():
    histories.append(list(map(int,line.split())))

ans = 0

for history in histories:
    sequences = []
    sequences.append(history)
    curr_sequence = history
    not_done = True # possible problem if the line starts out all 0s but none do
    while not_done:
        not_done = False
        next_sequence = []
        for idx in range(0,len(curr_sequence)-1):
            next_val = curr_sequence[idx+1]-curr_sequence[idx]
            next_sequence.append(next_val)
            if next_val != 0:
                not_done = True
        sequences.append(next_sequence)
        curr_sequence = next_sequence

    sequences[-1].append(0)
    for idx in range(len(sequences)-1,0,-1):
        sequences[idx-1].append(sequences[idx][-1]+sequences[idx-1][-1])
    #print('history with extrapolated value',sequences[0])
    ans += sequences[0][-1]

print('sum of extrapolated values',ans)

# part b
# rather than adding a zero to the end and filling in the next values of each previous sequence, 
# you should instead add a zero to the beginning of your sequence of zeroes, then fill in new first values for each previous sequence.

ans = 0

for history in histories:
    sequences = []
    sequences.append(deque(history))
    curr_sequence = history
    not_done = True # possible problem if the line starts out all 0s but none do
    while not_done:
        not_done = False
        next_sequence = [] 
        for idx in range(0,len(curr_sequence)-1):
            next_val = curr_sequence[idx+1]-curr_sequence[idx]
            next_sequence.append(next_val)
            if next_val != 0:
                not_done = True
        sequences.append(deque(next_sequence))
        curr_sequence = next_sequence

    sequences[-1].appendleft(0)
    for idx in range(len(sequences)-1,0,-1):
        sequences[idx-1].appendleft(sequences[idx-1][0]-sequences[idx][0])
    #print('history with extrapolated previous value',sequences[0])
    ans += sequences[0][0]

print('sum of extrapolated previous values',ans)