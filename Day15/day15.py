# PART TWO NOT STARTED
from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path

day=15
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

def holiday_helper(s):
    ret = 0
    for c in s:
        ret += ord(c)
        ret *= 17
        ret = ret%256
    return ret

ans = 0
for line in data.splitlines():
    for s in line.split(','):
        ans += holiday_helper(s)
    pass

print('part one:',ans)