from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path

day=7
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

# uses index to link them all together
hands = []  # input data
bids = []   # input data
hand_types = [] # calculated
ranks = []      # calculated

ordered_hand_types =  ['5K','4K','FH','3K','2P','1P','HC']   # best to worst
ordered_hand_types.reverse()    # worst to best

ordered_card_types = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']  # best to worst
ordered_card_types.reverse()   # worst to best

# part b J cards are now the weakest individual cards, weaker even than 2
ordered_card_types_joker = ['A','K','Q','T','9','8','7','6','5','4','3','2','J']  # best to worst
ordered_card_types_joker.reverse()   # worst to best

# give each card a character that is easier to sort
def card_sortable(c):
    if c=='T':
        return 'A'
    if c=='J':
        return 'B'
    if c=='Q':
        return 'C'
    if c=='K':
        return 'D'
    if c=='A':
        return 'E'
    return c

# part b
def card_sortable_joker(c):
    if c=='J':
        return '1'
    return card_sortable(c)

for line in data.splitlines():
    hand = line.split()[0]
    bid = int(line.split()[1])
    hands.append(hand)
    bids.append(bid)

hands_sortable = []
for h in hands:
    h_sortable = ''
    for c in h:
        h_sortable += card_sortable(c)
    hands_sortable.append(h_sortable)

# Returns hand type, one of: 5K, 4K, FH, 3K, 2P, 1P, HC
def get_hand_type(h):
    # let's count how many of each character are in the hand
    counts = {}
    for c in h:
        if c in counts:
            counts[c] += 1
        else:
            counts[c] = 1
    
    if 5 in counts.values():
        return '5K'
    if 4 in counts.values():
        return '4K'
    if 3 in counts.values() and 2 in counts.values():
        return 'FH'
    if 3 in counts.values():
        return '3K'
    if list(counts.values()).count(2) == 2:
        return '2P'
    if 2 in counts.values():
        return '1P'
    return 'HC'

for h in hands:
    ht = get_hand_type(h)
    #print(h,'->',ht)
    hand_types.append(ht)

ranks = [None for x in range(len(hands))]

# figure out ranks lowest to highest
def fill_ranks():
    curr_rank = 1
    for oht in ordered_hand_types:
        hands_of_this_type_sortable = [] # list of (idx,hand)
        # find hands with this type
        for idx,h in enumerate(hands_sortable):
            if hand_types[idx] == oht:
                hands_of_this_type_sortable.append([idx,h])

        hands_of_this_type_sorted = sorted(hands_of_this_type_sortable,key=lambda h: h[1])

        for hott in range(len(hands_of_this_type_sorted)):
            assert(ranks[hands_of_this_type_sorted[hott][0]] == None)
            ranks[hands_of_this_type_sorted[hott][0]] = curr_rank
            curr_rank += 1

        if curr_rank>len(hands):
            # we're done
            break

fill_ranks()
ans = 0
for idx,h in enumerate(hands):
    w = bids[idx]*ranks[idx]
    ans += w

print('total winnings',ans)

# part b

# Returns hand type, one of: 5K, 4K, FH, 3K, 2P, 1P, HC
# J cards can pretend to be whatever card is best for the purpose of determining hand type
def get_hand_type_jokers(h):
    # let's count how many of each character are in the hand
    counts = {}
    for c in h:
        if c in counts:
            counts[c] += 1
        else:
            counts[c] = 1
    
    if 5 in counts.values():
        return '5K'
    if 4 in counts.values():
        if 'J' in counts:
            # 4 Js or 1J either way we have 5-of-a-kind
            return '5K'
        return '4K'
    if 3 in counts.values() and 2 in counts.values():
        if 'J' in counts:
            # 3 Js or 2 Js either way we have 5-of-a-kind
            return '5K'
        return 'FH'
    if 3 in counts.values():
        if 'J' in counts:
            # 3 Js or 1 J either way we have 4-of-a-kind
            return '4K'
        return '3K'
    if list(counts.values()).count(2) == 2:
        # 2-2-1
        if 'J' in counts:
            if counts['J'] == 2:
                return '4K'
            if counts['J'] == 1:
                return 'FH'
        return '2P'
    if 2 in counts.values():
        # 2-1-1-1
        if 'J' in counts:
            # 2 Js or 1 J either way we have 3-of-a-kind
            return '3K'
        return '1P'
    # 1-1-1-1-1
    if 'J' in counts:
        return '1P'
    return 'HC'

# recalculate hand types with jokers for part b
hand_types = []
for h in hands:
    ht = get_hand_type_jokers(h)
    if False and 'J' in h:
        print(h,'->',ht)
    hand_types.append(ht)

ranks = [None for x in range(len(hands))]

# redo using new Joker sorting
hands_sortable = []
for h in hands:
    h_sortable = ''
    for c in h:
        h_sortable += card_sortable_joker(c)
    hands_sortable.append(h_sortable)

fill_ranks()
ans = 0
for idx,h in enumerate(hands):
    w = bids[idx]*ranks[idx]
    ans += w

print('total winnings part b with jokers',ans)
# 252724151 is too low -> fix bug in get_hand_type_jokers
# 253473444 is too low -> fix another but in get_hand_type_jokers
# 253666245 is too low, sigh. I'd forgotten that J now sorts differently, it has the lowest rank of any card.