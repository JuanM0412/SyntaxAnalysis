def get_derivations(grammar, symbol):
    rules = set()
    for non_terminal, derivations in grammar.items():
        for item in derivations:
            if symbol in item:
                rules.update(non_terminal)
    
    return list(rules)


def calculate_closure(closures, grammar, non_terminals):
    for closure in closures.values():
        for symbol in closure:
            flag = False
            for element in symbol:
                if element == '•':
                    flag = True

                if flag == True and element in non_terminals:
                    rules = get_derivations(grammar, element)
                    for derivations in rules:
                        for derivation in grammar[derivations]:
                            update = derivation
                            if element in closures:
                                old_closure = closures[element]
                                old_closure.append('•' + update)
                                update = old_closure
                            else:
                                update = ['•' + update]
                            closures[element] = update


def first_closure(grammar):
    closures = {}
    closure = grammar['|']
    closure = ['•' + closure[0]]
    closures['|'] = closure

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

    closures = first_closure(grammar)
    calculate_closure(closures, grammar, non_terminals)

    print(closures)


if __name__ == '__main__':
    main()