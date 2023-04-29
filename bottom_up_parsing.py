def non_terminal_case(grammar, symbol, calculated, non_terminals):
    closure, test = [], []
    for derivations in grammar[symbol]:
        closure.append('•' + derivations)
        calculated.add(symbol)
        if derivations[0] in non_terminals and derivations[0] not in calculated:
            test = non_terminal_case(grammar, derivations[0], calculated, non_terminals)

        closure = closure + test

    return closure


def get_closure(closures, symbol, grammar, non_terminals):
    next_closure = set()
    i = 0
    for closure in closures.values():
        for element in closure:
            last_element, flag = False, False
            if element[len(element) - 1] == '•':
                last_element = False
            
            for item in element:
                if item == '•':
                    flag = True
                    i = element.index('•')
                    continue
                
                if item != symbol and flag:
                    break
                elif flag and last_element == False:
                    new_closure = element
                    tmp = list(new_closure)
                    j = i + 1
                    aux = tmp[j]
                    tmp[j] = tmp[i]
                    tmp[i] = aux
                    new_closure = ''.join(tmp)
                    next_closure.add(new_closure)
                    if j + 1 < len(tmp) and tmp[j + 1] in non_terminals:
                        calculated = set()
                        non_terminal_closure = non_terminal_case(grammar, tmp[j + 1], calculated, non_terminals)
                        next_closure = next_closure.union(set(non_terminal_closure))

    return list(next_closure)


def calculate_item(grammar, symbol):
    closures = {}
    symbol = (symbol, 0)
    for items in grammar.values():
        for derivation in items:
            if symbol in closures:
                old_closure = closures[symbol]
                old_closure.append('•' + derivation)
                closure = old_closure
            else:
                closure = ['•' + derivation]
                closures[symbol] = closure

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

    closures = calculate_item(grammar, '|')

    print(closures)
    last_element = ''
    i = 0
    for closure in closures.copy().values():
        for element in closure:
            flag = False
            for item in element:
                if item == '•':
                    flag = True
                    continue
                if flag == True and last_element != item and item not in closures:
                    add_closure = get_closure(closures, item, grammar, non_terminals)
                    closures[(item, i)] = add_closure
                    last_element = item
                    i += 1
                break

    print(closures)


if __name__ == '__main__':
    main()