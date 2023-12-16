from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path
import pandas

day=13
year=2023
test=False
part_two = True

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

# compare mismatched rows to see if they are almost-match
def differs_by_one(a,b):
    # already know they are not identical
    # count how many mismatched elements, allowed exactly one
    found_mismatch = False
    for idx,x in enumerate(a):
        if (a[idx] != b[idx]):
            if not found_mismatch:
                found_mismatch = True
            else:
                # more than one mismatch
                return False
    return True

# returns the number of rows above the first horizontal line of reflection
# 0 means nothing found
def find_reflection(terrain):

    ret = 0
    num_rows = len(terrain)
    # find adjacent identical rows then check
    for idx,row in enumerate(terrain):
        smudge = False
        # adjacent matching rows
        if idx<num_rows-1 and (row == terrain[idx+1] or (part_two and not smudge and differs_by_one(row,terrain[idx+1]))):
            if row != terrain[idx+1]:
                # we're here because we applied a smudge
                smudge = True
            # a line of reflection has identical rows above and below all the way to the end
            mirror = True   # until proven otherwise
            num_lines_to_compare = min(idx+1,num_rows-idx-1)
            for i in range(1,num_lines_to_compare):
                if terrain[idx-i] != terrain[idx+1+i]:
                    if part_two and not smudge and differs_by_one(terrain[idx-i],terrain[idx+1+i]):
                        smudge = True
                    else:
                        mirror = False
                        break
            if part_two:
                if mirror and smudge:
                    ret = idx+1
                    break
            else:
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
            #print('horizontal reflection found, rows above',rows_above)
            ans += 100*rows_above
        else:
            terrain = pandas.DataFrame(terrain).transpose().values.tolist()
            rows_above = find_reflection(terrain)
            if rows_above>0:
                #print('vertical reflection found, columns left',rows_above)
                ans += rows_above
            else:
                print('unexpected - no lines of reflection - ignoring this pattern')
        terrain = []

print('answer',ans)