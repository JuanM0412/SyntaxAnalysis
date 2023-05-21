from top_down_parsing import follow_second_rule, follow_third_rule, first, get_derivations


def find_rule(derivation, non_terminal, grammar, number_rule):
    rules = grammar[non_terminal]
    for rule in rules:
        if derivation == rule:
            index = rules.index(rule)
            return number_rule[non_terminal][index]


def get_rule(move_to, number_rules, grammar):
    for rule, derivations in grammar.items():
        i = 0
        while i < len(derivations):
            compare_to = number_rules[rule]
            if compare_to[i] == move_to and derivations[i] != 'ε':
                return len(derivations[i])
            elif compare_to[i] == move_to and derivations[i] == 'ε':
                return 0
            
            i += 1


def lr_parsing(string, stack, number_rules, original_grammar, parsing_table, non_terminals):
    a = string[0]
    i = 0
    while True:
        try:
            s = stack.pop()
            stack.append(s)
            new_state = parsing_table[(s, a)]
            action = new_state[0]
            if action == 0 and a not in non_terminals:
                move_to = new_state[1]
                stack.append(move_to)
                i += 1
                a = string[i]
            elif action == 1:
                reduce_to = new_state[1]
                derivation_len = get_rule(reduce_to, number_rules, original_grammar)
                j = 0
                if derivation_len <= len(stack):
                    while j < derivation_len:
                        stack.pop()
                        j += 1
                else:
                    return False
                
                move_to = stack.pop()
                stack.append(move_to)
                new = parsing_table[(move_to, new_state[2])]
                stack.append(new[1])
            elif action == 2:
                return True
            else:
                return False
            
        except Exception:
            return False


def action(derivation, goto, non_terminals, index, follow, rule, number_rule, grammar):
    i = derivation.index('•')
    if i + 1 < len(derivation):
        element = derivation[i + 1]
        for go in goto:
            if go[0] == element and go[2] == index:
                return (0, go[1], element, index)
    elif '•' == derivation[len(derivation) - 1] and derivation[i - 1] == non_terminals[1] and len(derivation.replace('•', '')) == 1:
        for go in goto:
            if derivation[i - 1] == non_terminals[1] and derivation[i] == derivation[len(derivation) - 1]:
                return (2, -1, '$', index)
    elif '•' == derivation[len(derivation) - 1]:
        if len(derivation) == 1:
            for go in goto:
                if go[0] == 'ε' and go[1] == index:
                    goto_array = []
                    for symbol in follow[rule]:
                        goto_array.append((1, find_rule('ε', rule, grammar, number_rule), symbol, go[1], rule))
                    
                    return goto_array
        element = derivation[i - 1]
        for go in goto:
            if go[0] == element and go[1] == index:
                goto_array = []
                for symbol in follow[rule]:
                    goto_array.append((1, find_rule(derivation.replace('•', ''), rule, grammar, number_rule), symbol, go[1], rule))
                
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


def get_item(grammar, rule, non_terminals, goto):
    closures = {}
    closure = non_terminal_case(rule, grammar, non_terminals, goto, 0)
    closure = set(closure)
    closure = list(closure)
    closures[rule] = closure
    return closures


def non_terminal_case(rule, grammar, non_terminals, goto, state):
    closures = []
    calculated = set()
    initial_closure = grammar[rule].copy()
    while initial_closure:
        for derivations in initial_closure:
            for derivation in derivations:
                if (derivations not in calculated or derivations == 'ε') and rule not in closures:
                    if derivations == 'ε':
                        closure = ('•', rule)
                        goto.append(('ε', state, 0))
                    else:
                        closure = ('•' + derivations, rule)

                    closures.append(closure)
                    initial_closure.remove(derivations)

                if derivation[0] in non_terminals and derivation not in calculated and rule != derivation[0]:
                    tmp = non_terminal_case(derivation, grammar, non_terminals, goto, state)
                    i = 0
                    while i < len(tmp):
                        closures.append(tmp[i])
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
                if item[len(item) - 1] != '•' and item[i + 1] == symbol:
                    symbol = item[i + 1]
                    for element in item:
                        if element == '•':
                            flag = True
                            continue

                        if flag == True:
                            if item[i + 1] != 'ε':
                                new_closure = list(item)
                                j = i + 1
                                aux, new_closure[j] = new_closure[j], new_closure[i]
                                new_closure[i] = aux
                                new_closure = ''.join(new_closure)
                                index = new_closure.index('•')
                                new_closure = [(new_closure, rule)]
                                if index + 1 < len(item) and new_closure[0][0][index + 1] in non_terminals:
                                    add_to_closure = non_terminal_case(new_closure[0][0][index + 1], grammar, non_terminals, goto, r)
                                    add_to_closure = set(add_to_closure)
                                    add_to_closure = list(add_to_closure)
                                    k = 0
                                    while k < len(add_to_closure):
                                        new_closure.append(add_to_closure[k])
                                        k += 1

                            else:
                                item = item.replace('ε', '')
                                new_closure = [(item, rule)]

                            if symbol not in new_state:
                                new_state[symbol] = new_closure
                            else:
                                tmp = new_state[symbol]
                                tmp = tmp + new_closure
                                tmp = set(tmp)
                                tmp = list(tmp)
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
                

def create_table(actions):
    lr_parsing_table = {}
    for action in actions:
        if (action[3], action[2]) not in lr_parsing_table:
            if action[0] == 1:
                lr_parsing_table[(action[3], action[2])] = (action[0], action[1], action[4])
                continue
            lr_parsing_table[(action[3], action[2])] = (action[0], action[1])
        else: return False

    return lr_parsing_table


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
    closures.append(get_item(extend_grammar, non_terminals[0], non_terminals, goto))
    symbols = get_symbols(closures)
    get_closure(closures, extend_grammar, symbols, non_terminals, goto)
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

    table = create_table(actions)
    if table:
        while True:
            string = input()
            if string == ';':
                break
            
            stack = [0]
            test = lr_parsing(string + '$', stack, number_rule, grammar, table, non_terminals)
            if test == True:
                print(f'{string} is valid')
            else:
                print(f'{string} is invalid')
    else:
        print('Grammar is not LR(0)')


if __name__ == '__main__':
    main()