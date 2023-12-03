from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path

day=3
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

# any number adjacent to a symbol, even diagonally, is a "part number"
# symbol - anything that's not a digit or a period
"""
467..114..
...*......
..35..633.
"""

# make the list of symbol locations first then step through parsing numbers and check adjacent cells in list of symbol locations
symbol_locations = []
symbols = set()

# is digit adjacent to a symbol? is there a symbol left/right or on row above or below number including diagonally
def has_adjacent_symbol(x,y,symbol_locations):
    return (x-1,y) in symbol_locations or \
            (x+1,y) in symbol_locations or \
            (x,y-1) in symbol_locations or \
            (x,y+1) in symbol_locations or \
            (x+1,y+1) in symbol_locations or \
            (x-1,y-1) in symbol_locations or \
            (x+1,y-1) in symbol_locations or \
            (x-1,y+1) in symbol_locations

# part b list of gears and their adjacent part numbers
gear_locations = []
gear_adjacent_parts = dict()    # (x,y) -> n1, n2, n3

# part b return list of adjacent gear locations
def get_adjacent_gears(x,y,gear_locations):
    a = set()
    if (x-1,y) in gear_locations:
        a.add((x-1,y))
    if (x+1,y) in gear_locations:
        a.add((x+1,y))
    if (x,y-1) in gear_locations:
        a.add((x,y-1))
    if (x,y+1) in gear_locations:
        a.add((x,y+1))
    if (x+1,y+1) in gear_locations:
        a.add((x+1,y+1))
    if (x-1,y-1) in gear_locations:
        a.add((x-1,y-1))
    if (x+1,y-1) in gear_locations:
        a.add((x+1,y-1))
    if (x-1,y+1) in gear_locations:
        a.add((x-1,y+1))
    return a

for y,line in enumerate(data.splitlines()):
    for x,c in enumerate(line):
        if not c.isdigit() and c!='.':
            symbols.add(c)  # might want to see a list of possible symbols
            symbol_locations.append((x,y))
            # part b care about gear locations
            if c == '*':
                gear_locations.append((x,y))

print ('fyi symbols are',symbols)

ans = 0

for y,line in enumerate(data.splitlines()):
    number = ''    # accumulate digits of the number here
    adjacent_symbol = False # was any digit adjacent to a symbol
    adjacent_gears = set()
    for x,c in enumerate(line+'.'): # hack add a trailing dot so that we process a line that ends in a number
        if c.isdigit():
            number += c
            if has_adjacent_symbol(x,y,symbol_locations):
                adjacent_symbol = True
                # part b also keep a list of gear symbols adjacent to this number
                adjacent_gears = adjacent_gears | get_adjacent_gears(x,y,gear_locations)
        elif len(number)>0:
            if adjacent_symbol:
                # found a part number
                ans += int(number)
                # part b if number is adjacent to a gear, add it to that gear's list of adjacent part numbers
                for gear in adjacent_gears:
                    if gear in gear_adjacent_parts:
                        gear_adjacent_parts[gear].append(int(number))
                    else:
                        gear_adjacent_parts[gear] = [int(number)]
            else:
                #print('not a part number, skipping',int(number))
                pass
            number = ''
            adjacent_symbol = False
            adjacent_gears = set()
            
print("Sum of all the part numbers", ans)

# part b
# A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

ans = 0
for gear in gear_adjacent_parts:
    if len(gear_adjacent_parts[gear]) == 2:
        ans += gear_adjacent_parts[gear][0]*gear_adjacent_parts[gear][1]

print("Sum of all the gear ratios", ans)