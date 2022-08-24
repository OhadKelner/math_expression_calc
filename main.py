import re


def calc(expression):
    """
    0) def calc: Main function, returns solution (float) to a mathematical expression (str)

       1) def re_arrange_expression: Re-arrange expression operators and spaces
       2) def map_brackets: Map all the brackets indexes
       3) def solve_exp: Solve for each bracket-pair
       4) def solve_brackets_exp: Calls "def mul_div_phase" and then "def add_sub_phase"
       5) def mul_div_phase: solve for each "*", "/" operators
       6) def add_sub_phase: solve for each "+", "-" operators
    """
    exp_list = re_arrange_expression(expression)  # re-arrange expression operators and spaces

    brackets_map = map_brackets(exp_list)  # map all the brackets indexes
    return solve_exp(brackets_map, exp_list)  # solve for each bracket-pair


def solve_exp(brackets_map, exp_list):  # solve for each bracket-pair
    bracket_count = len(brackets_map['('])  # calc number of bracket-pairs

    index_remove_count, save_remove_count = 0, 0

    for i in range(bracket_count - 1, -1, -1):  # iterate on each bracket-pair
        pre_brackets = exp_list[:brackets_map['('][i]]  # expression part before the current calculated brackets
        brac_op_index = brackets_map['('][i]  # index for the current (-bracket expression to be solved
        brac_cl_index = brackets_map[')'][i]  # index for the current )-bracket expression to be solved
        index_remove_count = brac_cl_index - brac_op_index  # the number of indexes to be "deleted" from the expression

        # check if a "new" bracket-pair or an "inner" bracket-pair is to be solved:
        if i < bracket_count - 1:
            if brac_cl_index < brackets_map['('][i + 1]:
                save_remove_count = 0

        # solving the current bracket pair:
        solved_brackets_exp = solve_brackets_exp(exp_list[brac_op_index + 1: brac_cl_index - save_remove_count])
        after_brackets = exp_list[brackets_map[')'][i] + 1 - save_remove_count:]  # expression part after the current calculated brackets
        exp_list = pre_brackets + solved_brackets_exp + after_brackets  # re-assemble the expression with solved part

        print("".join([str(x) for x in exp_list])+"=")

        save_remove_count = index_remove_count  # saving the "lossed" number of indexes

    return float(solve_brackets_exp(exp_list)[0])


def map_brackets(exp_list):
    brackets_map = {'(': [], ')': []}  # dictionary for saving each bracket index

    for index, bracket in enumerate(exp_list):  # iterating on the expression searching for brackets
        if bracket == "(":  # (-bracket found
            brackets_map["("].append(index)  # save its index
            brackets_map[")"].append(0)  # append a "saved slot" matching the current (-bracket

        elif bracket == ")":  # )-bracket found
            save_i = 0
            min_sub = index - brackets_map["("][0]
            for i in range(0, len(brackets_map["("])):
                if index - brackets_map["("][i] < min_sub and brackets_map[")"][i] == 0:
                    save_i = i
            brackets_map[")"][save_i] = index

    return brackets_map


def re_arrange_expression(expression):
    operator_dict = {" ": "", "--": "+", "+-": "-", "-+": "-"}  # dictionary for replacing operators

    for operator in operator_dict:
        expression = expression.replace(operator, operator_dict[
            operator])  # replacement for operators acorrding to the dictionary

    exp_list = re.split(r"([-+*/()])", expression)  # split the expression string with each operator

    exp_list = [x for x in exp_list if x != ""]  # delete each empty string found in the expression list

    if exp_list[0] == "+":  # delete + operator if found in the begining of the expression
        del exp_list[0]

    if exp_list[0] == "-" and exp_list[1].isnumeric():  # delete - operator if found and *-1 the next number
        del exp_list[0]
        exp_list[0] = float(exp_list[0]) * -1

    return exp_list


def solve_brackets_exp(exp_list):
    exp_list = mul_div_phase(exp_list)  # solve for each "*", "/" operators
    exp_list = add_sub_phase(exp_list)  # solve for each "+", "-" operators
    return exp_list


def mul_div_phase(exp_list):
    i = 2
    if exp_list[0] == "-":  # delete - operator if found and *-1 the next number
        exp_list[1] = float(exp_list[1]) * -1
        del exp_list[0]

    while i < len(exp_list):  # iterate on the expression searching for "*", "/" operators
        if exp_list[i - 1] == "*":  # * found
            if exp_list[i] == "-":  # delete - operator if found and *-1 the next number
                exp_list[i + 1] = float(exp_list[i + 1]) * -1
                del exp_list[i]

            exp_list[i - 2] = float(exp_list[i - 2]) * float(
                exp_list[i])  # MULTIPLY the 2 numbers next to the "*" operator
            del exp_list[i - 1:i + 1]  # delete the "*" operator

        elif exp_list[i - 1] == "/":  # / found
            if exp_list[i] == "-":  # delete - operator if found and *-1 the next number
                exp_list[i + 1] = float(exp_list[i + 1]) * -1
                del exp_list[i]

            exp_list[i - 2] = float(exp_list[i - 2]) / float(
                exp_list[i])  # DIVIDE the 2 numbers next to the "/" operator
            del exp_list[i - 1:i + 1]  # delete the "/" operator
        else:
            i += 2  # continue iteration

    return exp_list


def add_sub_phase(exp_list):
    i = 2

    while i < len(exp_list):# iterate on the expression searching for "+", "-" operators
        if exp_list[i - 1] == "+":# + found
            exp_list[i - 2] = float(exp_list[i - 2]) + float(exp_list[i])# ADD the 2 numbers next to the "/" operator
            del exp_list[i - 1:i + 1]# delete the "+" operator

        elif exp_list[i - 1] == "-":# - found
            exp_list[i - 2] = float(exp_list[i - 2]) - float(exp_list[i])# SUBTRACT the 2 numbers next to the "/" operator
            del exp_list[i - 1:i + 1]# delete the "-" operator
        else:
            i += 2# continue iteration
    return exp_list

print("Waiting for your expression input:")
print("e.g: (-10)/(-423.4)*((((21*-32/(2-20)-1))))/-(-3858.4)/(-43.0)*((((1/-39/(2-500)-6.1))))")
exp = input()
print(calc(exp))
