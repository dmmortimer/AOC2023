# PART TWO NOT FINISHED
from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path
import pandas

day=13
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

data += '\n\n' # add a blank line at the end to simplify parsing

"""
To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection; 
to that, also add 100 multiplied by the number of rows above each horizontal line of reflection.
"""
# see if there's a horizontal line of reflection
# if not, turn the columns in to rows and use the same search to get a vertical line of reflection

ans = 0

# returns the number of rows above the first horizontal line of reflection
# 0 means nothing found
def find_reflection(terrain):

    ret = 0
    num_rows = len(terrain)
    # find adjacent identical rows then check
    for idx,row in enumerate(terrain):
        # adjacent matching rows
        if idx<num_rows-1 and row == terrain[idx+1]:
            # a line of reflection has identical rows above and below all the way to the end
            mirror = True   # until proven otherwise
            num_lines_to_compare = min(idx+1,num_rows-idx-1)
            for i in range(1,num_lines_to_compare):
                if terrain[idx-i] != terrain[idx+1+i]:
                    mirror = False
                    break
            if mirror:
                ret = idx+1
                break
    return ret

terrain = []

for line in data.splitlines():
    if len(line)>0:
        terrain.append(list(line.strip()))
    else:
        # blank line, we have a complete pattern, process it
        rows_above = find_reflection(terrain)
        if rows_above>0:
            ans += 100*rows_above
        else:
            terrain = pandas.DataFrame(terrain).transpose().values.tolist()
            rows_above = find_reflection(terrain)
            if rows_above>0:
                ans += rows_above
            else:
                print('unexpected - no lines of reflection - ignoring this pattern')
        terrain = []

print('answer',ans)