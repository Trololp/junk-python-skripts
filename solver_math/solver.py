# Solver for android game 'Hard Math Game'
# Uses recursive algorithm to find possible combination that solves problem, also using backtracking.

def opeartion (op, num1, num2):
    if op == '+':
        return num1 + num2
    if op == '*':
        return num1 * num2
    if op == '-':
        return abs(num1 - num2)
    if op == '/':
        if num1 > num2:
            return  num1/num2
        return num2/num1
    print(f'unknown op {op}')
    exit(0)



def do_next():
    global path
    global complete
    if complete:
        return
    if len(data) == 1:
        return
    for a in range(len(data)):
        num1 = data[a]
        data.pop(a)
        saved_path1 = path
        path = path + str(num1)
        for b in range(len(data)):
            num2 = data[b]
            saved_path2 = path
            for op in ops:
                num = opeartion(op,num1,num2)
                data[b] = num
                saved_path3 = path
                path = path + op + str(num2) + '\n'
                if num == Result and len(data) == 1:
                    print(path)
                    complete = 1
                    return
                do_next()
                if complete:
                    return
                path = saved_path3

            data[b] = num2
            path = saved_path2

        path = saved_path1
        data.insert(a, num1)


while(1):
    input_str = str(input(">"))
    input_nums = input_str.split(' ')
    if input_nums[0] == 'E':
        exit(0)

    data = []
    ops = []
    path = 'path: '
    ops.append(input_nums[1])
    ops.append(input_nums[2])
    try:
        if input_nums[0] == 'A':
            data.append(int(input_nums[3]))
            data.append(int(input_nums[4]))
            data.append(int(input_nums[5]))
            data.append(int(input_nums[6]))
            Result = int(input_nums[7])
        elif input_nums[0] == 'B':
            data.append(int(input_nums[3]))
            data.append(int(input_nums[4]))
            data.append(int(input_nums[5]))
            data.append(int(input_nums[6]))
            data.append(int(input_nums[7]))
            Result = int(input_nums[8])
    except IndexError:
        print('Something wrong with input.')
        continue
    except ValueError:
        print("Invalid Value")
        continue
    complete = 0
    do_next()
