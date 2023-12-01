from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path

day=1
year=2023

test=False
part_b=True

spelled_digits = ['zero','one','two','three','four','five','six','seven','eight','nine']

data = None

if test:
    data = open(os.path.join(os.path.dirname(__file__),'day01b-test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

# 1abc2
ans = 0

d1 = None   # first digit
d2 = None   # last seen digit

def see_digit(c):
    #print('see',c)
    global d1
    global d2
    if d1 == None:
        d1 = c
        d2 = c
    else:
        # keep overwriting with the latest digit
        d2 = c

for line in data.splitlines():
    #print(line)
    s = ''  # accumulated letters
    d1 = None
    d2 = None
    for c in line.strip():
        if c.isdigit():
            see_digit(c)
            s = ''
        elif part_b:
            # letter, accumulate into potential spelled-out number
            s += c
            # now check if our word so far contains any of the spelled-out digits
            for n,w in enumerate(spelled_digits):
                idx = s.find(w)
                if idx>=0:
                    d = str(n)
                    see_digit(d)
                    # strip up to and including first letter so this word doesn't match any more
                    # handle scenarios like eightwo
                    s = s[idx+1:]
            pass
        else:
            # part a, skip letters
            pass
            
    if d1 == None:
        print('Line has no digits at all! Skipping',line)
        pass
    else:
        val = int(d1+d2)
        ans += val

print("Sum of calibration values", ans)