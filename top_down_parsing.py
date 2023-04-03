def first(symbol, alphabet, productions):
  first_set = set()
  if symbol in alphabet:
    return symbol
  
  if symbol == "@":
    return "@"
  
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


def follow(non_terminal, firsts, grammar, alphabet, start_symbol):
  follow_set = set()
  derivations = grammar[non_terminal]

  for rule in derivations:
    for element in rule:
      """if "@" in firsts:
        follow("E", firsts[0], grammar, alphabet, start_symbol)"""
      if not element.islower():
        follow_set.update(firsts)
      if element == start_symbol:
        follow_set.update("$")

  return follow_set


def main():
  grammar = {}
  print("Cuando se le pida, ingrese los simbolos no terminales en mayusculas y los terminales en minusculas.")

  print("Ingrese los epsilons como @")

  print("Ingrese los simbolos terminales de su alfabeto separados por espacios en blanco")
  alphabet = input().split()

  print("Ingrese los simbolos no terminales de su gramatica separados por espacios en blanco, ingresando primero el simbolo inicial de la gramatica")
  non_terminals = input().split()

  for non_terminal in non_terminals:
    print(f"Ingrese las derivaciones del simbolo {non_terminal}, separando cada una por un solo espacio")
    productions = input().split()
    grammar[non_terminal] = productions

  print(grammar)
  all_first = []

  for non_terminal in grammar:
    symbol_first = first(non_terminal, alphabet, grammar)
    all_first.append(symbol_first)
  
  print(all_first)
  
  non_trerminal_follow = follow("F", ")", grammar, alphabet, non_terminals[0]).difference("@")
  print(non_trerminal_follow)


if __name__ == "__main__":
  main()