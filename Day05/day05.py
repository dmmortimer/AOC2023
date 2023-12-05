from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path

day=5
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = get_data(year=year,day=day)

seeds = []
seed_to_soil_map = []
soil_to_fertilizer_map = []
fertilizer_to_water_map = []
water_to_light_map = []
light_to_temperature_map = []
temperature_to_humidity_map = []
humidity_to_location_map = []

def get_mapped_value(x,rules):
    y = x
    for r in rules:
        dest = r[0]
        src = r[1]
        n = r[2]
        if x in range(src,src+n+1):
            y = dest+(x-src)
            break
    return y

def get_soil(x):
    return get_mapped_value(x,seed_to_soil_map)

def get_fertilizer(x):
    return get_mapped_value(x,soil_to_fertilizer_map)

def get_water(x):
    return get_mapped_value(x,fertilizer_to_water_map)

def get_light(x):
    return get_mapped_value(x,water_to_light_map)

def get_temperature(x):
    return get_mapped_value(x,light_to_temperature_map)

def get_humidity(x):
    return get_mapped_value(x,temperature_to_humidity_map)

def get_location(x):
    return get_mapped_value(x,humidity_to_location_map)

def get_seed_location(seed):
    soil = get_soil(seed)
    fertilizer = get_fertilizer(soil)
    water = get_water(fertilizer)
    light = get_light(water)
    temperature = get_temperature(light)
    humidity = get_humidity(temperature)
    location = get_location(humidity)
    return location

a = []  # current map we're adding to
for line in data.splitlines():
    if len(line.strip()) == 0:
        continue
    section = line.split(':')[0]
    match section:
        case 'seeds':
            seeds = list(map(int,line.split(':')[1].split()))
        case 'seed-to-soil map':
            a = seed_to_soil_map
        case 'soil-to-fertilizer map':
            a = soil_to_fertilizer_map
        case 'fertilizer-to-water map':
            a = fertilizer_to_water_map
        case 'water-to-light map':
            a = water_to_light_map
        case 'light-to-temperature map':
            a = light_to_temperature_map
        case 'temperature-to-humidity map':
            a = temperature_to_humidity_map
        case 'humidity-to-location map':
            a = humidity_to_location_map
        case _:
            # non-empty line is a list of numbers, add it to current map
            a.append(list(map(int,line.split())))

seed_locations = []

for seed in seeds:
    seed_location = get_seed_location(seed)
    seed_locations.append(seed_location)

print('Lowest location number', min(seed_locations))

# part b
# seeds line is a list of ranges of seeds
# grab first line and strip off seeds label
seed_range_numbers = list(map(int,data.splitlines()[0].split(':')[1].split()))
start = 0
count = 0
seed_ranges = []
for idx,n in enumerate(seed_range_numbers):
    if idx%2==0:
        # even index is start of a range
        start = n
    else:
        # odd index is length of range
        count = n
        seed_ranges.append([start,count])

def is_seed(seed):
    for r in seed_ranges:
        if r[0] <= seed and seed < r[0]+r[1]:
            return True
    return False

# guessed 484023871 it's too high
# oops, that was part a answer
# also, part b runs too slow, need to speed it up

# what if we work backwards - want a low location number
# start traveling up from 0 location number and see if you can get to any of the seed numbers
# given a location number, what seed maps to it?

# let's make reverse map versions of our functions
def get_reverse_mapped_value(x,rules):
    y = x
    for r in rules:
        dest = r[0]
        src = r[1]
        n = r[2]
        if x in range(dest,dest+n+1):
            y = src+(x-dest)
            break
    return y

def get_reverse_seed(x):
    return get_reverse_mapped_value(x,seed_to_soil_map)

def get_reverse_soil(x):
    return get_reverse_mapped_value(x,soil_to_fertilizer_map)

def get_reverse_fertilizer(x):
    return get_reverse_mapped_value(x,fertilizer_to_water_map)

def get_reverse_water(x):
    return get_reverse_mapped_value(x,water_to_light_map)

def get_reverse_light(x):
    return get_reverse_mapped_value(x,light_to_temperature_map)

def get_reverse_temperature(x):
    return get_reverse_mapped_value(x,temperature_to_humidity_map)

def get_reverse_humidity(x):
    return get_reverse_mapped_value(x,humidity_to_location_map)

# gets the seed number that would map to this location number
def get_reverse_seed_number(location):
    humidity = get_reverse_humidity(location)
    temperature = get_reverse_temperature(humidity)
    light = get_reverse_light(temperature)
    water = get_reverse_water(light)
    fertilizer = get_reverse_fertilizer(water)
    soil = get_reverse_soil(fertilizer)
    seed = get_reverse_seed(soil)
    return seed

# did this with successive searches - knew part a answer 484023871 was too high because I guessed it accidentally
# searched in units of 10000 then 1000 then 100 then 10 then 1 to find the answer
candidate_location = 46294170
while True:
    print('checking',candidate_location)
    if is_seed(get_reverse_seed_number(candidate_location)):
        break
    candidate_location += 1

print('Lowest location number, part b', candidate_location)