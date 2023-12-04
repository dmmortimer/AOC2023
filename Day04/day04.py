from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path

day=4
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53

# list of winning numbers, then list of numbers you have
ans = 0

for line in data.splitlines():

    # parse line to get card numbers
    winning = line.split(':')[1].split('|')[0].split()
    have = line.split(':')[1].split('|')[1].split()

    # how many winning numbers on this line
    matches = 0
    for n in have:
        if n in winning:
            matches += 1

    # how much is this card worth
    points=0
    if matches>0:
        points = pow(2,matches-1)
    #print(line)
    #print(points, 'points')
    ans += points

print('Total points', ans)

# part b
# you win copies of the scratchcards below the winning card equal to the number of matches

# scores a card by adding won cards to the list
# luckily you don't go back and win copies of cards you've already processed
def score_card(card_index):

    global cards
    global card_counts

    # this card
    winning = cards[card_index][0]
    have = cards[card_index][1]

    # how many copies of this card do we have
    num_copies = card_counts[card_index]

    matches = 0
    for n in have:
        if n in winning:
            matches += 1

    # each copy of this card wins copies of the next 'matches' cards
    for i in range(card_index+1,card_index+matches+1):
        card_counts[i] += num_copies

    return

# read in all the cards
# don't need to store card number, they are in order and strictly incrementing, just use the index
cards = []  # each card is two lists, of winning numbers and numbers you have

for line in data.splitlines():

    # parse line to get card numbers
    winning = line.split(':')[1].split('|')[0].split()
    have = line.split(':')[1].split('|')[1].split()

    cards.append([winning, have])

card_counts = [1 for x in range(len(cards))]    # how many of each card we have - start with one of each

for i in range(len(cards)):
    score_card(i)

ans = sum(card_counts)

print('Total cards', ans)