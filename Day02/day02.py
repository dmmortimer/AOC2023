from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path

day=2
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'day02-test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

# part a: bag contains only 12 red cubes, 13 green cubes, and 14 blue cubes
fact = [12,13,14]

# store input as a dict game id -> (r,g,b),(r,g,b),(r,g,b)
# (r,g,b) is a three-element list aka game draw
# dictionary key is game id and value is three lists or how every many game draws there were
games = {}

for line in data.splitlines():
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

    # game id
    game_id = int(line.split(':')[0].replace('Game ',''))
    game_draws = []

    # Split the rest of the string into draws
    for draw_s in line.split(':')[1].split(';'):
        # 3 blue, 4 red
        nr = 0
        ng = 0
        nb = 0
        n = 0

        # assume format is valid, always number then color
        for token in draw_s.split():
            if token.isdigit():
                n = int(token)
            else:
                match token.replace(',',''):
                    case 'blue':
                        nb = n
                    case 'red':
                        nr = n
                    case 'green':
                        ng = n
                    case _:
                        print('unexpected color',token)
            
        rgb = [nr,ng,nb]
        game_draws.append(rgb)

    games[game_id] = game_draws

def is_possible_draw(draw,fact):
   return draw[0]<=fact[0] and draw[1]<=fact[1] and draw[2]<=fact[2]

def is_possible_game(game_draws,fact):
    for draw in game_draws:
        if not is_possible_draw(draw,fact):
            return False
    return True

ans = 0

for game_id in games:
    if is_possible_game(games[game_id],fact):
        ans += game_id

print("Sum of IDs of games that would have been possible", ans)

# part b
# in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible
# it'll be the max seen in each draw for each color
def minimum_set(game_draws):
    max_red = 0
    max_green = 0
    max_blue = 0

    for draw in game_draws:
        if draw[0]>max_red:
            max_red = draw[0]
        if draw[1]>max_green:
            max_green = draw[1]
        if draw[2]>max_blue:
            max_blue = draw[2]
    return (max_red,max_green,max_blue)
    
# The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together
def power(cubes):
    return cubes[0]*cubes[1]*cubes[2]

ans = 0
for game_id in games:
    ans += power(minimum_set(games[game_id]))

print("Sum of power of minimum set of cubes that must have been present for each game",ans)