from collections import deque


# symbol is the element (terminal - non terminal) to calculate the first
# alphabet is an array with all the terminals
def first(symbol, alphabet, grammar):
    # flag used to check if one production only derivate in a ε production
    flag = False
    # here is the first of the symbol
    first_set = set()
    # if the symbol is a terminal the first is itself
    if symbol in alphabet:
        return symbol
    # load the productions of the symbol
    derivations = grammar[symbol]
    # this for is to check each derivation
    for derivation in derivations:
        if derivation == 'ε':
            flag = True
            continue

        # This flag is used to pass the recursive derivation in the left recursions grammars and calculate properly the first
        first_symbol = True
        # This flag is used to agreggate epsilon if atleast one derivation can be reduce to epsilon
        # If the flag never turn off, we agreggate the epsilon in the first
        derivation_with_epsilon = True
        for element in derivation:
            # Left recursive case
            if element == symbol and first_symbol:
                derivation_with_epsilon = False
                break

            first_symbol = False
            # We call this function for each element of the production
            partial_first = first(element, alphabet, grammar)
            # in this case, the first of the element could reduce in epsilon, so we keep calculating
            if 'ε' in partial_first:
                # New set is an auxiliar used to avoid eliminate the epsilon of the main first set
                new_set = set(partial_first)
                new_set.discard('ε')
                first_set.update(new_set)
            # in this case, the first of the element couldn't be reduce to epsilon, so we stop to see elements and turn off the flag
            else:
                derivation_with_epsilon = False
                new_set = set(partial_first)
                new_set.discard('ε')
                first_set.update(new_set)
                break

        if derivation_with_epsilon:
            first_set.update('ε')

    if flag:
        first_set.update('ε')

    return first_set

# string is the string to which we will calculate the first
# firsts is the dictionary calculated in the first function
def first_of_string(string, firsts):
    # here is the first of the symbol
    first_of_str = set()
    # this flag is used to verificate that the string could be reduce to epsilon
    # if the flag stay in true, we agreggate the epsilon in the first set
    flag = True
    for character in string:
        #We access to the first of the symbol and look the posible cases
        first = firsts[character]
        # case where the character is reducible to epsilom. We keep calculating
        if 'ε' in first:
            # New set is an auxiliar used to avoid eliminate the epsilon of the main first set
            new_set = set(first)
            new_set.discard('ε')
            first_of_str.update(new_set)
            continue
        # case where the caracter is not reducible to epsilon. We break the for and turn off the flags
        else:
            flag = False
            first_of_str.update(first)
            first_of_str.discard('ε')
            break

    if flag:
        first_of_str.update('ε')    
    
    return first_of_str


# symbol is the non-terminal that we want to find inside the grammar to calculate his follow
def get_derivations(grammar, symbol):
    rules = set()
    for rule, derivations in grammar.items():
        # for each derivation inside the rule we look the symbol
        for derivation in derivations:
            if symbol in derivation:
                rules.update(rule)

    return list(rules)


# rules is where we are going to calculate the follow of the symbol
# symbol is the non-terminal that we are going to calculate his follow
# firsts is where we store the first of each symbol of the grammmar
# start_symbol is the initial symbol of the grammar
def follow_second_rule(rules, symbol, firsts, grammar, start_symbol):
    follow_set = set()
    past_element = False
    if symbol == start_symbol:
        follow_set.update('$')

    for rule in rules:
        for derivation in grammar[rule]:
            for element in derivation:
                if element == symbol and past_element != True:
                    past_element = True
                    continue

                if past_element == True:
                    follow_set.update(firsts[element])
                    
            past_element = False

    return follow_set


def follow_third_rule(rules, symbol, grammar, follows, firsts):
    follow_set = set(follows[symbol])
    for rule in rules:
        for derivation in grammar[rule]:
            if symbol in derivation:
                last_element = derivation[len(derivation) - 1]
                i = derivation.index(symbol)
                while i < len(derivation):
                    if derivation[i].isupper():
                        if derivation[i] != symbol and follows[derivation[i]] and 'ε' in first_of_string(derivation[i::], firsts):
                            follow_set.update(set(follows[rule]))
                        elif derivation[i] != symbol and not follows[derivation[i]] and 'ε' in first_of_string(derivation[i::], firsts):
                            follow_set.update(follow_third_rule(get_derivations(grammar, derivation[i]), derivation[i], grammar, follows, firsts))
                        elif symbol == last_element and rule != symbol:
                            follow_set.update(set(follows[rule]))

                    i += 1

    return follow_set


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


def main():
    # we read the input of the grammar until the line 200
    grammar, all_firsts, all_follows = {}, {}, {}
    alphabet = input().split()
    non_terminals = input().split()

    for non_terminal in non_terminals:
        productions = input().split()
        grammar[non_terminal] = productions

    # for each symbol in the grammar (terminal - non-terminal) we calculate the first. Until the line 209
    for non_terminal in grammar:
        symbol_first = first(non_terminal, alphabet, grammar)
        all_firsts[non_terminal] = list(symbol_first)

    for terminal in alphabet:
        symbol_first = first(terminal, alphabet, grammar)
        all_firsts[terminal] = list(symbol_first)

    # for each non terminal inside the grammar we calculate the follow. Until the line 220
    for non_terminal in grammar:
        # when we call this function (get_derivations) we get the rules of the grammar when we can calculate the follow for the non-terminal that we want
        rule = get_derivations(grammar, non_terminal)
        # we call the function who use the second rule of the follow, which is going to return a partial follow set
        non_trerminal_follow = follow_second_rule(rule, non_terminal, all_firsts, grammar, non_terminals[0]).difference('ε')
        # we store the provitional follow in a dictionary {non-terminal 1: [follow], ..., non-terminal n: [follow]}
        all_follows[non_terminal] = list(non_trerminal_follow)

    for non_terminal in grammar:
        # when we call this function (get_derivations) we get the rules of the grammar when we can calculate the follow for the non-terminal that we want
        rule = get_derivations(grammar, non_terminal)
        # we call the function who use the third rule of the follow, which is going to return the rest of the follow set
        non_terminal_follow = follow_third_rule(rule, non_terminal, grammar, all_follows, all_firsts)
        # we store the provitional follow in a dictionary {non-terminal 1: [follow], ..., non-terminal n: [follow]}      
        all_follows[non_terminal] = list(non_terminal_follow)

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


if __name__ == '__main__':
    main()