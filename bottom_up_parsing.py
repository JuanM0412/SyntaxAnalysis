def get_item(grammar, canonical, non_terminals):
    closures = {}
    calculated = set()
    initial_closure = grammar[canonical].copy()
    while initial_closure:
        for derivations in initial_closure:
            for derivation in derivations:
                if derivations not in calculated and canonical not in closures:
                    closure = ['•' + derivations]
                    closures[canonical] = closure
                    initial_closure.remove(derivations)
                elif derivations not in calculated and canonical in closures:
                    current_closure = closures[canonical]
                    current_closure.append('•' + derivations)
                    closures[canonical] = current_closure
                    initial_closure.remove(derivations)

                if derivation[0] in non_terminals and derivation not in calculated:
                    tmp = grammar[derivation[0]].copy()
                    i = 0
                    while i < len(tmp):
                        initial_closure.append(tmp[i])
                        i += 1

                calculated.add(derivation)
                break

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
    print(closures)


if __name__ == '__main__':
    main()