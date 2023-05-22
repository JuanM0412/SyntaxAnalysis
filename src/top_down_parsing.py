from collections import deque
from src.first_and_follow import calculate_first, first_of_string, calculate_follow


def parsing_table(grammar, follows, firsts):
    parsing_table = {}
    for rule in grammar: 
        for derivation in grammar[rule]:
            first_of_derivation = first_of_string(derivation, firsts)
            for first in first_of_derivation:
                if first == 'ε':
                    for follow in follows[rule]:
                        if (rule, follow) not in parsing_table.keys():
                            parsing_table[(rule, follow)] = derivation
                        else:
                            return False

                if (rule, first) not in parsing_table.keys():
                        if first != 'ε':
                            parsing_table[(rule, first)] = derivation
                else:
                    return False

    return parsing_table


def analyzer(string, alphabet, parsing_table, initial_symbol):
    stack = deque()
    stack.append('$')
    stack.append(initial_symbol)
    index = 0
    top = stack.pop()
    while deque:
        if top == '$' and string[index] == '$':
            break
        elif top == string[index]:
            top = stack.pop()
            index += 1
        elif top in alphabet:
            return 'Error'
        elif (top, string[index]) not in parsing_table:
            return 'Error'
        elif (top, string[index]) in parsing_table:
            derivation = parsing_table[(top, string[index])]
            for element in derivation[::-1]:
                stack.append(element)    
            
            top = stack.pop()
            while top == 'ε':
                top = stack.pop()

    return True


def top_down():
    # we read the input of the grammar until the line 200
    grammar, all_firsts, all_follows = {}, {}, {}
    alphabet = input().split()
    non_terminals = input().split()

    for non_terminal in non_terminals:
        productions = input().split()
        grammar[non_terminal] = productions

    all_firsts = calculate_first(grammar, alphabet)
    all_follows = calculate_follow(grammar, all_firsts, non_terminals[0])

    # we create the table, if the function returns false that means that the grammar is not LL1, by the other hand, if the grammar is LL1 we will have the table inside a dictionary
    parsing = parsing_table(grammar, all_follows, all_firsts)
    if parsing == False:
        print('This grammar is not LL1')
    else:
        # we read the string to validate, until the user wants to stop using ;
        flag = True
        while True:
            string = input()
            if string == ';':
                break

            for char in string:
                if char not in alphabet:
                    flag = False
                    break

            # we call the function that analyzes the string, if the string belongs to the grammar the function returns true, if the string does not belong to the grammar the function returns false
            result = analyzer(string + '$', alphabet, parsing, non_terminals[0])
            if result == True and flag != False:
                print(f'{string} is valid')
            else:
                print(f'{string} is invalid')