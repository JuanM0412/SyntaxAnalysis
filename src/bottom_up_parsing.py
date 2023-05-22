from src.first_and_follow import calculate_first, calculate_follow


# This function is when we have a reduce and we need to know exactly with which rule we must reduce
def find_rule(derivation, non_terminal, grammar, number_rule):
    rules = grammar[non_terminal]
    for rule in rules:
        if derivation == rule:
            index = rules.index(rule)
            return number_rule[non_terminal][index]


# This function finds the rule that we have to use to reduce and returns the len of that rule
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


# This is the algorithm that calculates if a string belongs to a given grammar
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


# This function calculates each action, dependig of the goto
def action(derivation, goto, non_terminals, index, follow, rule, number_rule, grammar):
    i = derivation.index('•')
    # If the item is not at the end, that means that the action is a shift
    if i + 1 < len(derivation):
        element = derivation[i + 1]
        for go in goto:
            if go[0] == element and go[2] == index:
                return (0, go[1], element, index)
    # This case is when we have this E' -> E•, where E is the initial symbol of the grammar
    elif '•' == derivation[len(derivation) - 1] and derivation[i - 1] == non_terminals[1] and len(derivation.replace('•', '')) == 1:
        for go in goto:
            if derivation[i - 1] == non_terminals[1] and derivation[i] == derivation[len(derivation) - 1]:
                return (2, -1, '$', index)
    # If the item is at the end, this means that the action is a reduce
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


# This function finds what items can we calculate with the items that we have in a moment
def get_symbols(canonical):
    symbols_to_calculate = []
    for closures in canonical:
        for closure in closures.values():
            for element in closure:
                i = element[0].index('•')
                if i + 1 < len(element[0]) and element[0][i + 1] not in symbols_to_calculate:
                    symbols_to_calculate.append(element[0][i + 1])

    return symbols_to_calculate


# This function calculates the firs item
def first_state(grammar, rule, non_terminals, goto):
    closures = {}
    closure = non_terminal_case(rule, grammar, non_terminals, goto, 0)
    closure = set(closure)
    closure = list(closure)
    closures[rule] = closure
    return closures


# If we have an item that is behind a non-terminal symbol, we must add to that item each derivation of the non-terminal
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


# This function avoids dding states that we already have
def check_repetitions(state_to_validate, canonical):
    for closure in canonical:
        for element in state_to_validate:
            if element in closure.values():
                return False

    return True


# This function tells us in which states we can calculate the item of a given symbol
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


# This function calculates all states of the automaton, except for the first state
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
                            # This move the item
                            if item[i + 1] != 'ε':
                                new_closure = list(item)
                                j = i + 1
                                aux, new_closure[j] = new_closure[j], new_closure[i]
                                new_closure[i] = aux
                                new_closure = ''.join(new_closure)
                                index = new_closure.index('•')
                                new_closure = [(new_closure, rule)]
                                # If the symbol next to the item is a non-terminal symbol, we must add the item to each derivation of that non-terminal
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
                            
                            # We store the new item in the new state
                            if symbol not in new_state:
                                new_state[symbol] = new_closure
                            else:
                                tmp = new_state[symbol]
                                tmp = tmp + new_closure
                                tmp = set(tmp)
                                tmp = list(tmp)
                                new_state[symbol] = tmp

                            break
                
                # If the new state is already calculated, we delete that state. But we save the actions that had just did it to get that state
                if not check_repetitions(new_state.values(), canonical):
                    m = closure_to_calculate.index(closures)
                    goto.append((symbol, canonical.index(new_state), came_from[q][0]))
                    new_state = {}

            q += 1

            # We store the new state on the automaton. But store the actions that had just did it to get that state
            if new_state and new_state not in canonical:
                m = closure_to_calculate.index(closures)
                canonical.append(new_state)
                goto.append((symbol, canonical.index(new_state), came_from[m][0]))
                symbols += (get_symbols(canonical[r::]))
                new_state = {}
                r += 1
                

# This algorithm calculates the table using the actions, where all the information is stored (type of action, where it move, with which symbol, from where I move)
def create_table(actions):
    lr_parsing_table = {}
    for action in actions:
        if (action[3], action[2]) not in lr_parsing_table:
            if action[0] == 1:
                lr_parsing_table[(action[3], action[2])] = (action[0], action[1], action[4])
                continue

            lr_parsing_table[(action[3], action[2])] = (action[0], action[1])
        
        # If there is any conflict with the entries of the table, that means that the grammar is not LR(0)
        else: 
            return False

    return lr_parsing_table


def bottom_up():
    # We read the input of the grammar until the line 278
    grammar, extend_grammar, all_firsts, all_follows, number_rule = {}, {}, {}, {}, {}
    closures, goto, actions = [], [], []
    alphabet = input().split()
    non_terminals = input().split()

    # Store the grammar and create the extended grammar
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
            
    # Calculate the first for each symbol in the grammar
    # Calculate the follow for each non-terminal in the grammar
    all_firsts = calculate_first(grammar, alphabet)
    all_follows = calculate_follow(grammar, all_firsts, non_terminals[1], alphabet)
    # Calculate the first state of the automaton
    # The automaton is store as follow: [{state 0}, {state 1}, ..., {state n}]
    closures.append(first_state(extend_grammar, non_terminals[0], non_terminals, goto))
    # Calculate which moves can be done from the first state
    symbols = get_symbols(closures)
    # Calculate all states of the automaton, and it calculate the goto as well
    get_closure(closures, extend_grammar, symbols, non_terminals, goto)
    # With the goto already calculate, we calculate the actions
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