from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path
import math

day=6
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

'''
Time:      7  15   30
Distance:  9  40  200
'''
race_times = []
best_distances = []

for line in data.splitlines():
    match line.split(':')[0]:
        case 'Time':
            race_times = list(map(int,line.split(':')[1].split()))
        case 'Distance':
            best_distances= list(map(int,line.split(':')[1].split()))

print('part a',len(race_times),'races')

# returns how far you'll go if you hold the button for h units of the race duration t
def distance(h,t):
    # hold for h units gives a speed h for the remaining time
    # distance = speed*time
    return 0 if t==h else h*(t-h)

# ways to win this race that lasts t units and has record distance d
def ways_to_win(t,d):
    n=0
    # x is how long we hold the button for - from 0 to the duration of the race
    # maybe could exclude 0 and duration, but leave for now
    for x in range(0,t+1):
        if distance(x,t)>d:
            n += 1
    return n

# part b needs to be more efficient
def ways_to_win_quadratic(t,d):
    # find the smallest way to win and the largest way to win
    # need to go at least d - means speed * remaining time needs to be at least d
    # h * (t-h) > d
    # the two solutions to a quadratic equation h*(t-h) - d = 0
    # commonly written as ax^2 + bx + c = 0
    # solve for x - here x is h, how long to hold the button
    a = -1
    b = t
    c = -d

    # quadratic formula, assume no complex numbers
    x1 = (-b + math.sqrt(b**2-4*a*c))/(2*a)
    x2 = (-b - math.sqrt(b**2-4*a*c))/(2*a)

    lower = min(x1,x2)
    upper = max(x1,x2)

    ways_to_win = math.floor(upper)-math.ceil(lower)+1
    # want to win, not tie
    if float.is_integer(lower):
        ways_to_win -= 1
    if float.is_integer(upper):
        ways_to_win -= 1
    return ways_to_win

ans = 1
ans_b = 1
for idx,t in enumerate(race_times):
    d = best_distances[idx]
    ans *= ways_to_win(t,d)
    ans_b *= ways_to_win_quadratic(t,d)

print('product of ways you can beat the record',ans)
print('part a calculated using part b formula',ans_b)

# part b there's only one race with a lot of milliseconds in it

race_time = 0
best_distance = 0

for line in data.splitlines():
    match line.split(':')[0]:
        case 'Time':
            race_time = int(line.split(':')[1].strip().replace(' ',''))
        case 'Distance':
            best_distance = int(line.split(':')[1].strip().replace(' ',''))

print('part b time',race_time,'best distance',best_distance)

ways_to_win = ways_to_win_quadratic(race_time,best_distance)

print('ways to beat the record',ways_to_win)