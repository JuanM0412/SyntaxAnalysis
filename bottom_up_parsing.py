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
                if derivations not in calculated and rule not in closures:
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


def closure(closures, grammar, symbol, non_terminals):
    closure_to_calculate = closures[symbol].copy()
    new_closure = ''
    for closure in closure_to_calculate:
        rule, item, flag = closure[1], closure[0], False
        i = item.index('•')
        if item[len(item) - 1] != '•':
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
                        add_to_closure = non_terminal_case(new_closure[0][0][index + 1], grammar, non_terminals)
                        k = 0
                        while k < len(add_to_closure):
                            new_closure.append(add_to_closure[k])
                            k += 1

                    if symbol not in closures:
                        closures[symbol] = new_closure
                    else:
                        compare_with = closures[symbol]
                        if new_closure[0] in compare_with:
                            tmp = closures[symbol]
                            tmp = tmp + new_closure
                            closures[symbol + symbol] = tmp
                        else:
                            tmp = closures[symbol]
                            tmp = tmp + new_closure
                            closures[symbol] = tmp
                            
                    break
    
    return closures


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

    closures = get_item(grammar, non_terminals[0], non_terminals)
    closures = closure(closures, grammar, '|', non_terminals)
    closures = closure(closures, grammar, 'E', non_terminals)
    closures = closure(closures, grammar, '+', non_terminals)
    print(closures)


if __name__ == '__main__':
    main()