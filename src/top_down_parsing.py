from collections import deque
from src.first_and_follow import calculate_first, first_of_string, calculate_follow


def parsing_table(grammar, follows, firsts):
    parsing_table = {}
    for rule in grammar: 
        for derivation in grammar[rule]:
            first_of_derivation = first_of_string(derivation, firsts)
            # For each terminal a ∈ First(α), add A -> α to M[A, α]
            for first in first_of_derivation:
                # If ε ∈ First(α), then for each terminal b ∈ Follow(A), add A -> α to M[A, b]
                # If ε ∈ First(α) and $ ∈ Follow(A), add A -> α to M[A, $] as well
                if first == 'ε':
                    for follow in follows[rule]:
                        if (rule, follow) not in parsing_table.keys():
                            parsing_table[(rule, follow)] = derivation
                        else:
                            return False

                if (rule, first) not in parsing_table.keys():
                        if first != 'ε':
                            parsing_table[(rule, first)] = derivation

                # If there is a conflict between the table entries we return False, which means that the grammar is not LL(1).
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
        # This means that the string belongs to the grammar
        if top == '$' and string[index] == '$':
            break
        # We move on to the next symbol on the string
        elif top == string[index]:
            top = stack.pop()
            index += 1
        # If we have this case means that the string doesn't belong to the grammar
        elif top in alphabet:
            return 'Error'
        # If we have this case means that the string doesn't belong to the grammar
        elif (top, string[index]) not in parsing_table:
            return 'Error'
        # We add new elements to the stack
        elif (top, string[index]) in parsing_table:
            derivation = parsing_table[(top, string[index])]
            for element in derivation[::-1]:
                stack.append(element)    
            
            top = stack.pop()
            while top == 'ε':
                top = stack.pop()

    return True


def top_down():
    # We read the input of the grammar until the line 76
    grammar, all_firsts, all_follows = {}, {}, {}
    alphabet = input().split()
    non_terminals = input().split()

    for non_terminal in non_terminals:
        productions = input().split()
        grammar[non_terminal] = productions

    # Calculate the first for each symbol in the grammar
    # Calculate the follow for each non-terminal in the grammar
    all_firsts = calculate_first(grammar, alphabet)
    all_follows = calculate_follow(grammar, all_firsts, non_terminals[0], alphabet)

    # We create the table, if the function returns false that means that the grammar is not LL1, by the other hand, if the grammar is LL1 we will have the table inside a dictionary
    parsing = parsing_table(grammar, all_follows, all_firsts)
    if parsing == False:
        print('This grammar is not LL1')
    else:
        # We read the string to validate, until the user wants to stop using ;
        flag = True
        while True:
            string = input()
            if string == ';':
                break

            for char in string:
                if char not in alphabet:
                    flag = False
                    break

            # We call the function that analyzes the string, if the string belongs to the grammar the function returns true, if the string does not belong to the grammar the function returns false
            result = analyzer(string + '$', alphabet, parsing, non_terminals[0])
            if result == True and flag != False:
                print(f'{string} is valid')
            else:
                print(f'{string} is invalid')