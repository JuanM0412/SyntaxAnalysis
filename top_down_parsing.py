def first(symbol, alphabet, productions):
  first_set = set()

  if symbol in alphabet:
    return symbol
  
  derivations = productions[symbol]
  flag_epsilon = True

  for rule in derivations:
    if rule == "@":
      first_set.update("@")
      continue

    for element in rule:
      partial_first = first(element, alphabet, productions)
      if "@" in partial_first:
        first_set.update(partial_first)

      else:
        flag_epsilon = False
        break
    
    first_set.update(partial_first)
    if flag_epsilon is False:
      first_set.discard("@")

  return first_set


def get_derivations(grammar, symbol):
    rules = set()

    for non_terminal, derivations in grammar.items():
      for item in derivations:
        if symbol in item:
          rules.update(non_terminal)
    
    return list(rules)


def follow(rules, symbol, firsts, grammar, start_symbol):
    follow_set = set()
    past_element = False

    if symbol == start_symbol:
        follow_set.update("$")
    
    for rule in rules:
        for derivation in grammar[rule]:
            for element in derivation:
                last_element = derivation[len(derivation) - 1]
                if element == symbol:
                    past_element = True
                
                if element.isupper() and past_element == True:
                  if element != symbol:
                    if "@" in firsts[element]:
                      derivations = get_derivations(grammar, element)
                      follow_set.update(follow(derivations, element, firsts, grammar, start_symbol))
                      follow_set.update(firsts[element])

                    else:
                       follow_set.update(firsts[element])

                  if symbol == last_element and rule != symbol:
                    derivations = get_derivations(grammar, rule)
                    follow_set.update(follow(derivations, rule, firsts, grammar, start_symbol))
                    past_element = False
                
                if not element.isupper() and past_element == True:
                  follow_set.update(firsts[element])
                  past_element = False

        past_element = False

    return follow_set


def main():
    grammar, all_firsts, all_follows = {}, {}, {}
    alphabet = input().split()
    non_terminals = input().split()

    for non_terminal in non_terminals:
        productions = input().split()
        grammar[non_terminal] = productions

    for non_terminal in grammar:
        symbol_first = first(non_terminal, alphabet, grammar)
        all_firsts[non_terminal] = list(symbol_first)

    for terminal in alphabet:
        symbol_first = first(terminal, alphabet, grammar)
        all_firsts[terminal] = list(symbol_first)

    for non_terminal in grammar:
        rule = get_derivations(grammar, non_terminal)
        non_trerminal_follow = follow(rule, non_terminal, all_firsts, grammar, non_terminals[0]).difference("@")
        all_follows[non_terminal] = list(non_trerminal_follow)

    print(f"First set: \n{all_firsts}")
    print(f"Follow set: \n{all_follows}")


if __name__ == "__main__":
  main()