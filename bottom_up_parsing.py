def get_derivations(grammar, symbol):
    rules = set()
    for non_terminal, derivations in grammar.items():
        for item in derivations:
            if symbol in item:
                rules.update(non_terminal)
    
    return list(rules)


def get_closure(closures, symbol):
    next_closure = []
    for closure in closures.values():
        for element in closure:
            flag = False
            for item in element:
                if item == '•':
                    flag = True
                    continue
                
                if item != symbol and flag:
                    break
                elif flag:
                    next_closure.append(element)

    return next_closure


def calculate_closure(closures, grammar, non_terminals):
    pass


def calculate_closure(grammar, non_terminals, symbol):
    closures = {}

    for rule, items in grammar.items():
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

    closures = calculate_closure(grammar, non_terminals, '|')
    #calculate_closure(closures, grammar, non_terminals)

    print(closures)

    print(get_closure(closures, 'E'))


if __name__ == '__main__':
    main()