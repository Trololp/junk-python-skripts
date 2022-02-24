# pyther 3
# #		# #### ##  #   ### 
#  # # #  #  # ### ###  # 	calc made by human
#   # #   #### # #   #  #
# Make calculator with that can be bad as possible inside code but still work
# input is string expresion like 'log((21701-19937)-(23209-21701))/log(2)' and this program must calculate
# right result no matter how bad it is doing it and print it.
import math 
import time
test_exp = 'log((21701-19937)-(23209-21701))/log(2)'
test_exp2 = '1+2*3-1-2+3-1*6*3-1+891/1+2'
test_exp3 = '1+7*(2+1-3*(4+1) + 5*7 - (1 + 3*(4+4)))'
test_exp5 = 'sin(1.5708)+0.04321+log(sqrt(exp(1*1*1)))+(1+2*3)-0.4-0.6+(4+6)*(2-1+2*3)-tan(0.785398)+2*10/3*6*sqrt(16/2/2)*10+10000-1000' #check it

fancy_words = ['asin', 'acos', 'atan', 'sin', 'cos', 'log', 'logd', 'tan', 'exp', 'sqr', 
			   'sqrt', 'inv', 'abs']

fancy_func = {
	'sin': lambda a: math.sin(a),
	'cos': lambda a: math.cos(a),
	'asin': lambda a: math.asin(a),
	'acos': lambda a: math.acos(a),
	'log': lambda a: math.log(a),
	'logd': lambda a: math.log10(a),
	'tan': lambda a: math.tan(a),
	'exp': lambda a: math.exp(a),
	'sqr': lambda a: a * a,
	'sqrt': lambda a: math.sqrt(a),
	'atan': lambda a: math.atan(a),
	'inv': lambda a: 1/a,
	'abs': lambda a: abs(a)
}

def parentesis_end(exp, ch_from):
	count = 0
	j = ch_from
	for ch in exp[ch_from:]:
		if ch == '(':
			count += 1
		if ch == ')':
			count -= 1
			if count == 0:
				return j+1
		j += 1
	
def have_parentesis(exp):
	for ch in exp:
		if ch == '(' or ch == ')':
			return True
	return False

#looking for abc() pos is first parentesis
def is_func(exp, pos): 
	if pos <= 0:
		return False
	if exp[pos - 1].isalpha():
		return True
	return False



def search_for_fancy_words(str):
	for word in fancy_words:
		if str.endswith(word):
			return word;
	return "unkn"

def calc_func(oldexp, exp, pos):
	if pos < 3:
		print("bad func name %s" % oldexp[:pos])
		return 0;
	if pos == 3:
		fname = oldexp[:3]
	elif pos == 4:
		fname = oldexp[:4]
	else:
		fname = oldexp[pos-4:pos]
	fname = search_for_fancy_words(fname)
	
	if fname == "unkn":
		print("Unkown function name [%s]" % fname)
		return 3, 0
	fname_len = len(fname)
	val = do_solve(exp)
	res = fancy_func[fname](val)
	return fname_len, res
	
	


def do_solve(exp):
	if have_parentesis(exp):
		for idx,ch in enumerate(exp):
			if ch == '(':
				if is_func(exp, idx):
					ch_end = parentesis_end(exp, idx)
					exp2 = exp[idx+1:ch_end-1]
					fname_len, res = calc_func(exp, exp2, idx)
					exp = exp[:idx-fname_len] + str(res) + exp[ch_end:]
					return do_solve(exp)
				else:
					ch_end = parentesis_end(exp, idx)
					exp2 = exp[idx+1:ch_end-1]
					res = do_solve(exp2)
					exp = exp[:idx] + str(res) + exp[ch_end:]
					return do_solve(exp)
			
	else:
		res = do_simple_calculations(exp)
		return res

#also get rid of signs
def get_numbers_and_operations(str):
	sign = 1.0
	h = ""
	numbers = []
	operations = []
	#remove_spaces
	str = str.replace(' ', '')
	#get all numbers in str
	for ch in str:
		if ch.isdigit() or ch == '.':
			h+=ch
		else:
			if h == "":
				if ch == '-':
					sign *= -1.0
			else:
				if	(ch == '-' or ch == '+' or ch == '*' or ch == '/'):
					if (ch == '-' or ch == '+'):
						operations.append('+') #it always '+' now
					if ch == '*':
						operations.append('*')
					if ch == '/':
						operations.append('/')
					numbers.append(sign*float(h))
					sign = 1.0
					if ch == '-':
						sign *= -1.0
					h = ""
	try:
		numbers.append(sign*float(h))
	except ValueError:
		print("Incorrect expression ?")
		return [0], []
	return numbers,operations

def search(list, val):
    for i in range(len(list)):
        if list[i] == val:
            return True
    return False

def do_simple_calculations(exp):
	numbers,operations = get_numbers_and_operations(exp)
	#take care of hign priority op first '*' and '/'
	while search(operations, '*') or search(operations, '/'):
		for idx,op in enumerate(operations):
			if op == '*':
				numbers[idx] = numbers[idx] * numbers[idx + 1]
				numbers.pop(idx + 1)
				operations.pop(idx)
			if op == '/':
				numbers[idx] = numbers[idx] / numbers[idx + 1]
				numbers.pop(idx + 1)
				operations.pop(idx)
	# take care of low priority op '+' 
	while search(operations, '+'):
		for idx,op in enumerate(operations):
			if op == '+':
				numbers[idx] = numbers[idx] + numbers[idx + 1]
				numbers.pop(idx + 1)
				operations.pop(idx)
	return numbers[0] #result

#exp = input()
res = do_solve(test_exp5)

middle_time = 0;
sum_time = 0;
for i in range(0, 100):
	
	start_time = time.perf_counter()
	do_solve(test_exp)
	delta_time = (time.perf_counter() - start_time)
	sum_time += delta_time
	middle_time = sum_time/(i+1)
	#print("--- %.7f seconds ---" % (delta_time))

print(">>> %.7f seconds <<<" % (middle_time))
print(do_solve(test_exp2))