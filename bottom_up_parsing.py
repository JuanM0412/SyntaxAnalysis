from top_down_parsing import follow_second_rule, follow_third_rule, first, get_derivations


def find_rule(derivation, non_terminal, grammar, number_rule):
    rules = grammar[non_terminal]
    for rule in rules:
        if derivation == rule:
            index = rules.index(rule)
            return number_rule[non_terminal][index]


def get_rule(all_closures, move_to, character):
    closures = all_closures[move_to - 1]
    for closure in closures.values():
        for element in closure:
            if character in element[0]:
                return element[1]


def find_action(actions, state, symbol):
    for action in actions:
        if action[3] == state and action[2] == symbol:
            if action[0] == 2:
                return (-1, action[1])
            
            return (action[1], action[0])


def lr_parsing(string, stack, actions, grammar, closures, number_rule):
    string += '$'
    a = string[0]
    i = 0
    while True:
        s = stack.pop()
        stack.append(s)
        new_state = find_action(actions, s, a)
        action = new_state[1]
        if action == 0:
            move_to = new_state[0]
            stack.append(move_to)
            i += 1
            a = string[i]
        elif action == 1:
            move_to = new_state[0]
            non_terminal = get_rule(closures, move_to, string[i - 1])
            derivations = grammar[non_terminal]
            for derivation in derivations:
                if string[i - 1] in derivation and len(stack) > 0:
                    j = 0
                    while j < len(derivation[0]):
                        stack.pop()
                        j += 1
                elif not stack:
                    return False
            
            move_to = stack.pop()
            stack.append(move_to)
            new = find_action(actions, move_to, non_terminal)
            stack.append(new[0])
        elif action == 2:
            return True
        else:
            return False


def action(derivation, goto, non_terminals, index, follow, rule, number_rule, grammar):
    i = derivation.index('•')
    if i + 1 < len(derivation):
        element = derivation[i + 1]
        for go in goto:
            if go[0] == element and go[2] == index:
                return (0, go[1], element, index)
    elif '•' == derivation[len(derivation) - 1] and derivation[i - 1] == non_terminals[1]:
        for go in goto:
            if derivation[i - 1] == non_terminals[1]:
                return (2, -1, '$', index)
    elif '•' == derivation[len(derivation) - 1] and derivation[i - 1] != non_terminals[1]:
        element = derivation[i - 1]
        for go in goto:
            if go[0] == element and go[1] == index:
                goto_array = []
                for symbol in follow[rule]:
                    goto_array.append((1, go[1], symbol, find_rule(derivation.replace('•', ''), rule, grammar, number_rule), rule))
                
                return goto_array


def get_symbols(canonical):
    symbols_to_calculate = []
    for closures in canonical:
        for closure in closures.values():
            for element in closure:
                i = element[0].index('•')
                if i + 1 < len(element[0]) and element[0][i + 1] not in symbols_to_calculate:
                    symbols_to_calculate.append(element[0][i + 1])

    return symbols_to_calculate


def get_item(grammar, rule, non_terminals):
    closures = {}
    closure = non_terminal_case(rule, grammar, non_terminals)
    closures[rule] = closure
    return closures


def non_terminal_case(rule, grammar, non_terminals):
    closures = []
    calculated = set()
    initial_closure = grammar[rule].copy()
    while initial_closure:
        for derivations in initial_closure:
            for derivation in derivations:
                if (derivations not in calculated or derivations == 'ε') and rule not in closures:
                    closure = ('•' + derivations, rule)
                    closures.append(closure)
                    initial_closure.remove(derivations)

                if derivation[0] in non_terminals and derivation not in calculated and rule != derivation[0]:
                    rule = derivation
                    tmp = grammar[derivation[0]].copy()
                    i = 0
                    while i < len(tmp):
                        initial_closure.append(tmp[i])
                        i += 1

                calculated.add(derivation)
                break

            break

    return closures


def check_repetitions(state_to_validate, canonical):
    for closure in canonical:
        for element in state_to_validate:
            if element in closure.values():
                return False

    return True


def search_rule(canonical, symbol):
    rules, tmp = [], []
    for closure in canonical:
        items, came_from = [], []
        for elements in closure.values():
            for element in elements:
                derivation = element[0]
                i = derivation.index('•')
                if i + 1 < len(derivation) and derivation[i + 1] == symbol:
                    items.append(element)
                    came_from.append(canonical.index(closure))

            rules.append(items)
            tmp.append(came_from)

    return (rules, tmp)


def get_closure(canonical, grammar, symbols, non_terminals, goto):
    r = 1
    for symbol in symbols:
        new_state = {}
        to_calculate = search_rule(canonical, symbol)
        closure_to_calculate, came_from = to_calculate[0], to_calculate[1]
        new_closure = ''
        q = 0
        for closures in closure_to_calculate:
            for closure in closures:
                rule, item, flag = closure[1], closure[0], False
                i = item.index('•')
                if item[len(item) - 1] != '•' and item[i + 1] == symbol and symbol != 'ε':
                    symbol = item[i + 1]
                    for element in item:
                        if element == '•':
                            flag = True
                            continue

                        if flag == True:
                            new_closure = list(item)
                            j = i + 1
                            aux, new_closure[j] = new_closure[j], new_closure[i]
                            new_closure[i] = aux
                            new_closure = ''.join(new_closure)
                            index = new_closure.index('•')
                            new_closure = [(new_closure, rule)]
                            if index + 1 < len(item) and new_closure[0][0][index + 1] in non_terminals:
                                add_to_closure = non_terminal_case(
                                    new_closure[0][0][index + 1], grammar, non_terminals)
                                k = 0
                                while k < len(add_to_closure):
                                    new_closure.append(add_to_closure[k])
                                    k += 1

                            if symbol not in new_state:
                                new_state[symbol] = new_closure
                            else:
                                tmp = new_state[symbol]
                                tmp = tmp + new_closure
                                new_state[symbol] = tmp

                            break

                if not check_repetitions(new_state.values(), canonical):
                    m = closure_to_calculate.index(closures)
                    goto.append((symbol, canonical.index(new_state), came_from[q][0]))
                    new_state = {}

            q += 1

            if new_state and new_state not in canonical:
                m = closure_to_calculate.index(closures)
                canonical.append(new_state)
                goto.append((symbol, canonical.index(new_state), came_from[m][0]))
                symbols += (get_symbols(canonical[r::]))
                new_state = {}
                r += 1
                


def main():
    grammar, extend_grammar, all_firsts, all_follows, number_rule = {}, {}, {}, {}, {}
    alphabet = input().split()
    non_terminals = input().split()

    non_terminals.insert(0, '|')
    i = 1
    for non_terminal in non_terminals:
        if non_terminal == '|':
            extend_grammar[non_terminal] = list(non_terminals[1])
            continue

        productions = input().split()
        extend_grammar[non_terminal] = productions
        grammar[non_terminal] = productions
        for production in productions:
            if non_terminal in number_rule:
                tmp = number_rule[non_terminal]
                tmp.append(i)
            else:
                number_rule[non_terminal] = [i]

            i += 1
            
    for non_terminal in grammar:
        symbol_first = first(non_terminal, alphabet, grammar)
        all_firsts[non_terminal] = list(symbol_first)

    for terminal in alphabet:
        symbol_first = first(terminal, alphabet, grammar)
        all_firsts[terminal] = list(symbol_first)

    for non_terminal in grammar:
        rule = get_derivations(grammar, non_terminal)
        non_trerminal_follow = follow_second_rule(rule, non_terminal, all_firsts, grammar, non_terminals[1]).difference('ε')
        all_follows[non_terminal] = list(non_trerminal_follow)

    for non_terminal in grammar:
        rule = get_derivations(grammar, non_terminal)
        non_terminal_follow = follow_third_rule(rule, non_terminal, grammar, all_follows, all_firsts)
        all_follows[non_terminal] = list(non_terminal_follow)

    closures, goto = [], []
    closures.append(get_item(extend_grammar, non_terminals[0], non_terminals))
    symbols = get_symbols(closures)
    get_closure(closures, extend_grammar, symbols, non_terminals, goto)
    print(goto)
    i = 0
    for closure in closures:
        print(f'state {i}: {closure}')
        i += 1

    actions = []
    for closure in closures:
        for items in closure.values():
            for item in items:
                calculated = action(item[0], goto, non_terminals, closures.index(closure), all_follows, item[1], number_rule, extend_grammar)
                if calculated not in actions and calculated != None:
                    if type(calculated) == list:
                        for element in calculated:
                            actions.append(element)
                    else:
                        actions.append(calculated)

    #(type, move to - reduce with, symbol, from)
    print(actions)
    print(len(actions))

    """ string = input()
    stack = [0]
    test = lr_parsing(string, stack, actions, grammar, closures, number_rule)
    if test:
        print('Valid')
    else:
        print('Invalid') """


if __name__ == '__main__':
    main()