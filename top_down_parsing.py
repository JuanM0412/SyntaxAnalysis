from collections import deque


def first(symbol, alphabet, productions):
    flag = False
    first_set = set()
    if symbol in alphabet:
        return symbol

    derivations = productions[symbol]
    for rule in derivations:
        if rule == 'ε':
            flag = True
            continue

        first_symbol = True
        derivation_with_epsilon = True
        for element in rule:
            if element == symbol and first_symbol:
                derivation_with_epsilon = False
                break

            first_symbol = False
            partial_first = first(element, alphabet, productions)
            if 'ε' in partial_first:
                new_set = set(partial_first)
                new_set.discard('ε')
                first_set.update(new_set)
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


def first_of_string(string, firsts):
    first_of_str = set()
    flag = True
    for character in string:
        first = firsts[character]
        if 'ε' in first:
            new_set = set(first)
            new_set.discard('ε')
            first_of_str.update(new_set)
            continue
        else:
            flag = False
            first_of_str.update(first)
            first_of_str.discard('ε')
            break

    if flag:
        first_of_str.update('ε')    
    
    return first_of_str


def get_derivations(grammar, symbol):
    rules = set()
    for non_terminal, derivations in grammar.items():
        for item in derivations:
            if symbol in item:
                rules.update(non_terminal)

    return list(rules)


def follow_second_rule(rules, symbol, firsts, grammar, start_symbol):
    follow_set = set()
    past_element = False
    if symbol == start_symbol:
        follow_set.update('$')

    for rule in rules:
        for derivation in grammar[rule]:
            for element in derivation:
                if element == symbol:
                    past_element = True
                    continue

                if past_element == True and element != symbol:
                    follow_set.update(firsts[element])
                    if 'ε' not in firsts[element] or not element.isupper():
                        past_element = False

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


def parsing_table(grammar, follows, firsts, alphabet, non_terminals):
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


def analyzer(string, alphabet, table, initial_symbol):
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
        elif (top, string[index]) not in table:
            return 'Error'
        elif (top, string[index]) in table:
            derivation = table[(top, string[index])]
            for element in derivation[::-1]:
                stack.append(element)    
            
            top = stack.pop()
            while top == 'ε':
                top = stack.pop()

    return True


def main():
    grammar, all_firsts, all_follows = {}, {}, {}
    alphabet = input().split()
    non_terminals = input().split()

    for non_terminal in non_terminals:
        productions = input().split()
        grammar[non_terminal] = productions

    for non_terminal in grammar:
        symbol_first = first(non_terminal, alphabet, grammar)
        all_firsts[non_terminal] = list(symbol_first)

    for terminal in alphabet:
        symbol_first = first(terminal, alphabet, grammar)
        all_firsts[terminal] = list(symbol_first)

    for non_terminal in grammar:
        rule = get_derivations(grammar, non_terminal)
        non_trerminal_follow = follow_second_rule(
            rule, non_terminal, all_firsts, grammar, non_terminals[0]).difference('ε')
        all_follows[non_terminal] = list(non_trerminal_follow)

    for non_terminal in grammar:
        rule = get_derivations(grammar, non_terminal)
        non_terminal_follow = follow_third_rule(rule, non_terminal, grammar, all_follows, all_firsts)
        all_follows[non_terminal] = list(non_terminal_follow)

    parsing = parsing_table(grammar, all_follows,all_firsts, alphabet, non_terminals)
    if parsing == False:
        print('This grammar is not LL1')
    else:
        while True:
            string = input()
            if string == ';':
                break

            result = analyzer(string + '$', alphabet, parsing, non_terminals[0])
            if result == True:
                print(f'{string} is valid')
            else:
                print(f'{string} is invalid')


if __name__ == '__main__':
    main()