def get_item(grammar, canonical, non_terminals):
    closures = {}
    rule = '|'
    calculated = set()
    initial_closure = grammar[canonical].copy()
    while initial_closure:
        for derivations in initial_closure:
            for derivation in derivations:
                if derivations not in calculated and canonical not in closures:
                    closure = [('•' + derivations, rule)]
                    closures[canonical] = closure
                    initial_closure.remove(derivations)
                elif derivations not in calculated and canonical in closures:
                    current_closure = closures[canonical]
                    current_closure = current_closure.append(('•' + derivations, rule))
                    initial_closure.remove(derivations)

                if derivation[0] in non_terminals and derivation not in calculated:
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


def closure(closures, grammar, symbol):
    closure_to_calculate = closures[symbol].copy()
    new_closure = ''
    for closure in closure_to_calculate:
        rule, item, flag = closure[1], closure[0], False
        i = item.index('•')
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
            
            if symbol not in closures:
                closures[symbol] = [(new_closure, rule)]
            else:
                tmp = closures[symbol]
                tmp.append((new_closure, rule))
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
    closures = closure(closures, grammar, '|')
    print(closures)


if __name__ == '__main__':
    main()