# PART TWO NOT STARTED YET
#from aocd import get_data    # https://pypi.org/project/advent-of-code-data/
import os.path

day=19
year=2023
test=False

data = None
if test:
    data = open(os.path.join(os.path.dirname(__file__),'test-input.txt')).read()
else:
    data = open(os.path.join(os.path.dirname(__file__),'input.txt')).read()
    #data = get_data(year=year,day=day)

workflows = dict()	# workflow name -> list of workflow rules

# a full workflow rule has 4 elements all strings
# the last rule in the workflow has only 1
#		category,comparison_op,op2,action

# px{a<2006:qkq,m>2090:A,rfg}
# workflow name brace comma-separated list of rules close brace
# rule category comparison operator comparison value colon action
# action Accept Reject or next workflow which can't be named A or R
# last rule has no condition

# get workflows until first blank line
for line in data.splitlines():
	if len(line.strip()) == 0:
		break
	# parse workflow
	workflow_name = line[0:line.find('{')]
	# strip leading/trailing braces
	line = line[line.find('{')+1:-1]
	rules = line.split(',')
	wf = []
	for idx,r in enumerate(rules):
		this_rule = []
		#a<2006:qkq
		if idx == len(rules)-1:
			this_rule.append(r)
		else:
			this_rule.append(r[0])	# category
			op = r[1]		# comparison operator
			this_rule.append(op)
			r = r[2:].split(':')	#2006:qkq
			this_rule.append(int(r[0]))	# comparison value
			this_rule.append(r[1])
		wf.append(this_rule)
		
	workflows[workflow_name] = wf

parts = []	# list of x m a s ratings - as a list of 4 integers

# parts start after first blank line
# {x=787,m=2655,a=1222,s=2876}
workflow_section = True
for line in data.splitlines():
	if len(line.strip()) == 0:
		workflow_section = False
		continue
	elif workflow_section:
		continue
	# strip leading/trailing braces
	line = line[1:-1]
	# split on comma
	category_ratings = line.split(',')
	part = []
	for category_rating in category_ratings:
		# assume x m a s in order
		(category,rating) = category_rating.split('=')
		part.append(int(rating))
	parts.append(part)
		
# returns next workflow or A or R
def do_workflow(workflow_name,part):
	x = part[0]
	m = part[1]
	a = part[2]
	s = part[3]
	next_wf = None
	wf_rules = workflows[workflow_name]
	last_rule_idx = len(wf_rules)-1
	for idx,rule in enumerate(wf_rules):
		if idx == last_rule_idx:
			# last rule in the list has no condition, always matches
			next_wf = rule[0]
			break
		# regular rule with comparison
		category,comparison_op,op2,action = rule
		op1 = None
		match category:
			case 'x':
				op1 = x
			case 'm':
				op1 = m
			case 'a':
				op1 = a
			case 's':
				op1 = s
		rule_match = None
		match comparison_op:
			case '<':
				rule_match = op1<op2
			case '>':
				rule_match = op1>op2
		if rule_match:
			next_wf = action
			break
	return next_wf

def is_accepted(part):
	# run part through workflow starting at 'in'
	next_wf = 'in'
	while True:
		next_wf = do_workflow(next_wf,part)
		if next_wf in ('A','R'):
			break
	
	return (next_wf == 'A')

ans = 0
for part in parts:
	if is_accepted(part):
		ratings_sum = sum(part)
		ans += ratings_sum

print('sum of ratings for accepted parts',ans)
