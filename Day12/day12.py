# PART TWO NOT FINISHED
from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path
from copy import deepcopy

day=12
year=2023
test=True

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

conditions = []  # . operational # damaged ? unknown
criteria = []           # size of each contiguous group of damaged springs in the condition
unknowns = []           # index of each ? in the condition

for line in data.splitlines():
    conditions.append(line.split(' ')[0])
    criteria.append(list(map(int,line.split(' ')[1].split(','))))

for condition in conditions:
    unknown = []
    for idx,c in enumerate(condition):
        if c == '?':
            unknown.append(idx)
    unknowns.append(unknown)

# utility function
# ways to partition integer X into n integers that add up to X
# x0+x1+...+xn-1 = X
def parts(X,n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    ans = 0
    for i in range(X-n+1):
        ans += parts(X-i-1,n-1)
    return ans

# ???.### 1,1,3

# brute force
# a ? can be either . or #
# then check to see if it meets criteria

# calculate damaged spring groups for given complete condition with no ?
def damaged_spring_groups(condition):
    groups = []
    n = 0
    for s in condition:
        if s == '#':
            n += 1
        elif s == '.':
            # wrap up group
            if n>0:
                groups.append(n)
                n = 0
        else:
            assert (False)  # can't happen, must be # or .
    # trailing group
    if condition[-1] == '#':
        groups.append(n)
    return groups

# check whether given complete condition meets the criteria
def meets_criteria(condition,criteria):
    groups = damaged_spring_groups(condition)
    if len(groups) != len(criteria):
        return False
    for idx,g in enumerate(groups):
        if g != criteria[idx]:
            return False
    return True

def num_arrangements_meeting_criteria(condition,unknown,criteria):
    # brute force compare every possible complete condition
    candidates = []

    # how to get every possible list? each ? can be either # or .
    # so depending on the number of ? we have that many permutations, two raised to the power n
    # binary number, each 1 turns the ? to # and each 0 turns it to .
    n = len(unknown)

    if n == 0:
        # no ? so only one arrangement and we assume it meets the criteria
        return 1

    num_combinations = 2 ** n

    combinations = []

    for x in range(num_combinations):
        # there has to be a better way to get a binary string of fixed length
        bits = bin(x)[2:]  # strip leading 0b
        # prepend 0s to get to desired length
        while len(bits)<n:
            bits = '0'+bits

        # starting string, we're going to replace each ? with # or . depending which combination this is
        candidate = list(condition)
        for idx,bit in enumerate(bits):
            if bit == '0':
                candidate[unknown[idx]] = '.'
            else:
                candidate[unknown[idx]] = '#'
        candidates.append(candidate)
        
    n = 0
    for c in candidates:
        if meets_criteria(c,criteria):
            n += 1

    return n

# returns possibly updated condition
def check_remove_leading_group(condition,criteria):
    group_size = criteria[0]

    # always remove leading . we don't care about them
    while condition.find('.') == 0:
        condition = condition.replace('.','',1)

    # if it starts with # we have the start of our group
    if condition[0] == '#':
        # condition starts with our group, it must continue for group length
        # and first char after must be .
        # we can strip all these off
        condition = condition[group_size+1:]
        criteria.pop(0)
        return condition

    # if here, condition starts with ?

    # only handling any number of ? followed by #
    # the only case we want to handle is where we find an exact match for our group
    # next char after the group must be . and we skip it
    # limit the number of ? we'll skip over to our group size, so we know the # is in our group
    # all other cases, return condition without removing first criteria

    # count number of ? until next dot or #
    num_q = 0
    next_char = ''
    for c in condition:
        if c == '?':
            num_q += 1
        else:
            next_char = c
            break
    if num_q>group_size:
        # not handling this case yet
        return condition

    if next_char != '#':
        # not handling this case yet
        return condition

    # if here, condition starts with between 1 and group_size ?s and then has a #

    # is this in fact the group we're looking for? check for exact match
    group = ''.join(['#' for x in range(group_size)])
    start = condition.find(group)
    if start == condition.find('#'):
        # now strip what we've counted
        condition = condition[num_q+group_size+1:]
        criteria.pop(0)
        return condition

    # todo there're probably other cases to check here
    return condition

def check_remove_trailing_group(condition,criteria):
    # reverse condition
    rcondition = condition[::-1]
    rcriteria = list(reversed(criteria))
    rcondition = check_remove_leading_group(rcondition,rcriteria)
    # remove last element
    if len(criteria) > len(rcriteria):
        criteria.pop()
    condition = rcondition[::-1]
    return condition

def get_arrangements_all_q(condition,criteria):
    # all question marks
    # number of ways to fit # and . with the correct group sizes
    n = len(condition)  # total number of springs in sequence
    n_broken_groups = len(criteria) # number of groups of broken springs
    n_working = n - sum(criteria)  # these are the number of dots we need to arrange around the groups

    if n_working == 0:
        # no dots to arrange
        return 1

    ways = 0
    ways = parts(n_working, n_broken_groups-1)  # broken groups at head and tail
    ways += 2*parts(n_working, n_broken_groups)   # have to multiply this by 2 because the separator could be at head or tail for each combo
    ways += parts(n_working, n_broken_groups+1) # separators at head and tail
    return ways

def num_arrangements_meeting_criteria_b(condition,criteria):
    input = condition

    while True:
        old_condition = condition
        condition = check_remove_leading_group(condition,criteria)
        if old_condition == condition:
            condition = check_remove_trailing_group(condition,criteria)
        if old_condition == condition:
            print('---------------------------------')
            print(input)
            print('reached a dead end, stopping here')
            print(condition,criteria)
            return 0

        if len(condition) == 0 or len(criteria) == 0:
            return 1

        # if only ? remains we can handle it
        if len(condition)>0 and len(criteria)>0 and '#' not in condition and '.' not in condition:
            return get_arrangements_all_q(condition,criteria)

        if False and condition.count('?')<5:
            # Brute force it from here
            unknown = []
            for idx,c in enumerate(condition):
                if c == '?':
                    unknown.append(idx)
            return num_arrangements_meeting_criteria(condition,unknown,criteria)

    return 1

print('there are',len(conditions),'to examine')
ans = 0
for i in range(len(conditions)):
    #print(conditions[i],criteria[i])
    n = num_arrangements_meeting_criteria_b(conditions[i],criteria[i])
    #print(n,'arrangements')
    ans += n

print('sum of counts of different arrangements that meet the criteria',ans)
# that ran pretty slow in part a

# part b
# unfold the input
# do we know something from the folding? for now, just unfold and forget about it
# need a much faster way to count valid arrangements

if False:

    unfolded_conditions = conditions.copy() # list of strings
    unfolded_criteria = deepcopy(criteria) # list of list of integers
    unfolded_unknowns = []  # list of list of integers

    # unfold each record
    num_copies = 5
    for idx,condition in enumerate(conditions):
        for x in range(num_copies-1):
            unfolded_conditions[idx] += '?' + conditions[idx]
            for y in range(len(criteria[idx])):
                unfolded_criteria[idx].append(criteria[idx][y])

        # best to just rediscover the unknowns - might not need them though
        unknown = []
        for idx,c in enumerate(unfolded_conditions[idx]):
            if c == '?':
                unknown.append(idx)
        unfolded_unknowns.append(unknown)

    ans = 0
    for i in range(len(conditions)):
        n = num_arrangements_meeting_criteria_b(unfolded_conditions[i],unfolded_criteria[i])
        #print('Unfolded condition',i+1,'has',n,'arrangements')
        ans += n

    print('after unfolding to',num_copies,'copies, sum of counts of different arrangements that meet the criteria',ans)
    # even the test input is too slow for the part a approach
    # we'll need a new and improved way to find arrangements