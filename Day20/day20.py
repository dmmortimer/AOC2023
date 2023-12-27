# PART TWO NOT STARTED YET
#from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path

day=20
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input-2.txt')).read()
else:
    data = open(os.path.join(os.path.dirname(__file__),'input.txt')).read()
    #data = get_data(year=year,day=day)

broadcaster = []	# only one broadcaster, with its list of downstream modules
flip_flops = dict()	# key is module name, value is 2-tuple current state (0 or 1) and list of downstream modules
conjunctions = dict()# key is module name, value is 2-tuple dict of input values (name-current value) and list of downstream modules

# given a module name, just look in either place to find it

# first pass identify each module and its downstream modules
for line in data.splitlines():
	module_name = line.split()[0]
	downstream_modules = line[len(module_name)+4:].replace(' ','').split(',')
	if module_name == 'broadcaster':
		broadcaster = downstream_modules
	elif module_name[0] == '%':
		flip_flops[module_name[1:]] = (0,downstream_modules)
	elif module_name[0] == '&':
		conjunctions[module_name[1:]] = (dict(),downstream_modules)
	elif module_name == 'output':
		#print('ignoring output module for now')
		pass
	else:
		print('unable to determine module type, ignoring',module_name)
		pass
	pass

print(broadcaster)
#print(flip_flops)
print('there are',len(flip_flops),'flip-flop modules')

# second pass identify the inputs to the conjunction modules
for c in conjunctions:
	# find inputs, hopefully ordering doesn't matter (how can it?)
	for f in flip_flops:
		(state,downstream_modules) = flip_flops[f]
		if c in downstream_modules:
			# this flip-flop is an input to c, add it to dict
			conjunctions[c][0][f] = 0	# initial value
	for c2 in conjunctions:
		(x,downstream_modules) = conjunctions[c2]
		if c in downstream_modules:
			# this conjunction is an input to c, add it to dict
			conjunctions[c][0][c2] = 0	# initial value

#print(conjunctions)

# turns out this was not required at all, no need to skimp on 1000 button presses
def flip_flops_all_zero():
	for f in flip_flops:
		(state,downstream_modules) = flip_flops[f]
		if state == 1:
			return False
	return True

# pulse is 3-tuple value 0 for low, 1 for high, source module name, and target module name
# updates global state and running pulse counts n_high, n_low
# returns list of pulses generated
def process_pulse(pulse):
	global n_high
	global n_low
	(value,source,target) = pulse
	#print(source,'-high' if value else '-low','->',target)
	if value == 0:
		n_low += 1
	else:
		n_high += 1
	generated_pulses = []
	# what kind of module are we pulsing at?
	if target in flip_flops:
		if value == 0:
			# low pulse changes state of flip-flop
			# wow I really need a better data structure
			flip_flops[target] = ((flip_flops[target][0]+1)%2,flip_flops[target][1])
			new_state = flip_flops[target][0]
			# and sends a pulse with new value from here to each downstream module
			for d in flip_flops[target][1]:
				generated_pulses.append((new_state,target,d))
		else:
			# high pulse does nothing to a flip-flop
			pass
	elif target in conjunctions:
		# When a pulse is received, the conjunction module first updates its memory for that input.
		conjunctions[target][0][source] = value
		# If it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
		output = 0
		for i in conjunctions[target][0]:
			if conjunctions[target][0][i] == 0:
				output = 1
		for d in conjunctions[target][1]:
			generated_pulses.append((output,target,d))
	else:
		#print('module has no targets, ignoring pulses at',target)
		pass

	return generated_pulses

# process button press given current state of flip-flops
def do_button_press():
	global n_low
	n_low += 1 # count initial low pulse from button press to broadcaster module
	# send low pulse through broadcaster node
	pulses_to_process = []
	for module in broadcaster:
		pulses_to_process.append((0,'broadcaster',module))
	while len(pulses_to_process)>0:
		next_round_of_pulses = []
		for pulse in pulses_to_process:
			next_round_of_pulses.extend(process_pulse(pulse))
		pulses_to_process = next_round_of_pulses
	return

n = 0	# number of button presses to return flip-flops to original state
n_high = 0	# running total of high pulses for a complete cycle
n_low = 0
max_button_presses = 1000
while True and n<max_button_presses:
	n += 1
	#print('====button press #',n)
	do_button_press()
	#unnecessary optimization we don't return to initial state with real data
	if flip_flops_all_zero():
		break

print('button presses in cycle:', n, 'high pulses:',n_high,'low pulses:',n_low)
total_high_pulses = int(n_high*max_button_presses/n)
total_low_pulses = int(n_low*max_button_presses/n)
print('after',max_button_presses,'button presses',total_high_pulses,'high pulses *',total_low_pulses,'low pulses')
print('answer',total_high_pulses*total_low_pulses)

