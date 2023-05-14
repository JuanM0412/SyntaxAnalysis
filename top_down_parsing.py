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

        for element in rule:
            partial_first = first(element, alphabet, productions)
            if 'ε' in partial_first:
                first_set.update(partial_first)
            else:
                new_set = set(partial_first)
                new_set.discard('ε')
                first_set.update(new_set)
                first_set.discard('ε')
                break

    if flag:
        first_set.update('ε')

    return first_set


def first_of_string(string, firsts):
    first_of_str = set()
    for character in string:
        first = firsts[character]
        first_of_str.update(first)
        if 'ε' in first_of_str:
            continue
        else:
            break
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

                if element.isupper() and past_element == True:
                    if element != symbol and 'ε' in firsts[element]:
                        follow_set.update(firsts[element])
                        if 'ε' not in firsts[element]:
                            past_element = False

                if not element.isupper() and past_element == True:
                    follow_set.update(firsts[element])
                    past_element = False

            past_element = False

    return follow_set


def follow_third_rule(rules, symbol, firsts, grammar, follows):
    follow_set = set(follows[symbol])
    past_element = False

    for rule in rules:
        for derivation in grammar[rule]:
            last_element = derivation[len(derivation) - 1]
            for element in derivation:
                if element == symbol:
                    past_element = True

                if element.isupper() and past_element == True:
                    if element != symbol and 'ε' in firsts[element]:
                        follow_set.update(set(follows[rule]))

                    if symbol == last_element and rule != symbol:
                        follow_set.update(set(follows[rule]))
                        past_element = False

        past_element = False

    return follow_set


def parsing_table(grammar, follow, first, alphabet, non_terminals):
    parsing_table = {}
    for rule, derivations in grammar.items():
        for derivation in derivations:
            if ((derivation[0] in alphabet and derivation[0] != 'ε') or (derivation[0] in non_terminals and 'ε' not in first[derivation[0]])) and (rule, derivation[0]) not in parsing_table:
                if (derivation[0] in non_terminals):
                    for terminal in first[derivation[0]]:
                        parsing_table[(rule, terminal)] = derivation
                else:
                    parsing_table[(rule, derivation[0])] = derivation

            elif 'ε' in first[derivation[0]] and (rule, derivation[0]) not in parsing_table:
                if '$' in follow[rule]:
                    parsing_table[(rule, '$')] = derivation
                for terminal in follow[rule]:
                    parsing_table[(rule, terminal)] = derivation

            elif (rule, derivation[0]) in parsing_table:
                return False

    return parsing_table


def analyzer(string, stack, alphabet, table):
    stack = stack.copy()
    a = string[0]
    symbol = stack.pop()
    i = 1
    while symbol != '$':
        if symbol == a:
            if i == len(string):
                break
            a = string[i]
            i += 1
            symbol = stack.pop()
        elif symbol in alphabet:
            return 'Error'
        elif (symbol, a) not in table:
            return 'Error'
        elif (symbol, a) in table:
            derivation = table[(symbol, a)]
            for element in derivation[::-1]:
                stack.append(element)
            symbol = stack.pop()
            if symbol == 'ε':
                symbol = stack.pop()

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
        non_terminal_follow = follow_third_rule(rule, non_terminal, all_firsts, grammar, all_follows)
        all_follows[non_terminal] = list(non_terminal_follow)

    print(f'First set: \n{all_firsts}')
    print(f'Follow set: \n{all_follows}', end='\n')

    """ parsing = parsing_table(grammar, all_follows,
                            all_firsts, alphabet, non_terminals)
    if parsing == False:
        print('This grammar is not LL1')
    else:
        stack = []
        stack.append('$')
        stack.append(non_terminals[0])

        while True:
            string = input()
            if string == ';':
                break

            result = analyzer(string, stack, alphabet, parsing)
            if result == True:
                print(f'{string} is valid')
            else:
                print(f'{string} is invalid') """


if __name__ == '__main__':
    main()