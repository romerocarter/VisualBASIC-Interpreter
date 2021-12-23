import lookup_table


# Instructions to be executed are stored on the stack in infix notation
stack = []
P = []
Px = 0  # abstract machine program counter


def IDENT():
    global Px
    Px += 1  # now points to the code of the identifier
    stack.append(P[Px])
    # if len(stack) == 0:
    #     stack.append(P[Px])
    # elif stack[len(stack)-1]!= P[Px]:
    #     stack.append(P[Px])


def INT():
    global Px
    Px += 1  # now points to the value of the integer
    stack.append(P[Px])


def OP():
    global Px
    Px += 1
    op = P[Px]  # value of the operator
    first = None  # code of identifier
    second = None
    if op == '=':
        second = stack.pop()
        first = stack.pop()
        if second in lookup_table.identifier_set.keys():  # second is an identifier
            lookup_table.identifier_set[first] = lookup_table.identifier_set[second]
        else:  # second is a numeral or literal
            lookup_table.identifier_set[first] = second
    elif op == '+':
        second = stack.pop()
        first = stack.pop()
        if first in lookup_table.identifier_set.keys():
            if second in lookup_table.identifier_set.keys():
                # both items are identifiers
                stack.append(int(lookup_table.identifier_set[first]) + int(lookup_table.identifier_set[second]))
            else: # first is identifier but second is a numeral
                stack.append(int(lookup_table.identifier_set[first]) + int(second))
        else:  # first is a numeral
            if second in lookup_table.identifier_set.keys(): # second is an identifier
                stack.append(int(first) + int(lookup_table.identifier_set[second]))
            else:  # both are numerals
                stack.append(first + second)
    elif op == '-':
        None
    elif op == '*':
        None
    elif op == '/':
        None


def STR():
    global Px
    Px += 1
    stack.append(P[Px])


def KEY():
    global Px
    Px += 1
    return None


def TER():
    global Px
    Px += 1
    return None


def printStackValue():
    print('[', end='')
    ind = 0
    for val in stack:
        if val in lookup_table.identifier_set.keys():
            if ind < len(stack) - 1:
                print(str(lookup_table.identifier_set[val]) + ', ', end='')
            else:
                print(str(lookup_table.identifier_set[val]), end='')
        else:
            print(str(val), end='')
        ind += 1
    print(']')


def evaluate():
    global Px
    LAST = len(P)
    print('Detected Instructions: ')
    print(P)
    # index = 0
    # ptr = 0
    # while index < LAST:
    #     if P[index] == lookup_table.OPERATOR:
    #         ptr = index
    #         temp1 = P[ptr]  # token
    #         temp2 = P[ptr+1]  # value
    #         P[ptr] = P[ptr+2]
    #         P[ptr+1] = P[ptr+3]
    #         P[ptr+2] = temp1
    #         P[ptr+3] = temp2
    #         index += 3
    #     index += 1
    while Px < LAST:
       if P[Px] == lookup_table.IDENTIFIER:
           IDENT()
       elif P[Px] == lookup_table.OPERATOR:
           OP()
       elif P[Px] == lookup_table.NUMERAL:
           INT()
       else:
           STR()
       Px += 1
       print('Stack: ')
       print(stack)
       print('Stack Values: ')
       printStackValue()