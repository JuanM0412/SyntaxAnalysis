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
    rules = []
    for closure in canonical:
        items = []
        for elements in closure.values():
            for element in elements:
                derivation = element[0]
                i = derivation.index('•')
                if i + 1 < len(derivation) and derivation[i + 1] == symbol:
                    items.append(element)

            if items not in rules:
                rules.append(items)

    return rules


def get_closure(canonical, grammar, symbols, non_terminals, goto):
    r = 1
    calculated_items = set()
    for symbol in symbols:
        new_state = {}
        closure_to_calculate = search_rule(canonical, symbol)
        new_closure = ''
        for closures in closure_to_calculate:
            for closure in closures:
                rule, item, flag = closure[1], closure[0], False
                i = item.index('•')
                if item[len(item) - 1] != '•' and item[i + 1] == symbol and symbol != 'ε' and closure not in calculated_items:
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
                            calculated_items.add(closure)
                            new_closure = [(new_closure, rule)]
                            if index + 1 < len(item) and new_closure[0][0][index + 1] in non_terminals:
                                add_to_closure = non_terminal_case(new_closure[0][0][index + 1], grammar, non_terminals)
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
                    new_state = {}

            if new_state and new_state not in canonical:
                canonical.append(new_state)
                goto.append((symbol, canonical.index(new_state)))
                symbols += (get_symbols(canonical[r::]))
                new_state = {}
                r += 1


def main():
    grammar = {}
    alphabet = input().split()
    non_terminals = input().split()
    non_terminals.insert(0, '|')

    for non_terminal in non_terminals:
        if non_terminal == '|':
            grammar[non_terminal] = list(non_terminals[1])
            continue
        
        productions = input().split()
        grammar[non_terminal] = productions

    closures = []
    goto = []
    closures.append(get_item(grammar, non_terminals[0], non_terminals))
    symbols = get_symbols(closures)
    get_closure(closures, grammar, symbols, non_terminals, goto)
    
    i = 0
    for closure in closures:
        print(f'state {i}: {closure}')
        i += 1

    print(goto)
    

if __name__ == '__main__':
    main()