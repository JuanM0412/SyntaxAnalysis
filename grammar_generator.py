import random

def grammar_generator():
    terminals = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k','+',')','(','%','#','&','$', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    non_terminals = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    number_of_terminals = random.randint(2,5)
    number_of_non_terminals = random.randint(2,5)

    alphabet = ""
    non_terminals_string = ""

    i = 1
    while i <= number_of_terminals:
        terminal = terminals[random.randint(1,len(terminals)-1)]
        terminals.remove(terminal)
        alphabet =  terminal + " " + alphabet 
        i += 1
    
    print(alphabet)

    i = 1
    while i <= number_of_non_terminals:
        non_terminal = non_terminals[random.randint(1,len(non_terminals)-1)]
        non_terminals.remove(non_terminal)
        non_terminals_string =  non_terminal + " " + non_terminals_string
        i += 1

    print(non_terminals_string)

    non_terminals_array = non_terminals_string.split()
    alphabet_array = alphabet.split()

    for non_terminal in non_terminals_array:
        number_of_productions = random.randint(1,3)
        productions = ""
        i = 1
        while i <= number_of_productions:
            type_of_derivation = random.randint(1,4)
            flag = False
            if type_of_derivation == 1:
                productions = alphabet_array[random.randint(1,len(alphabet_array)-1)] + alphabet_array[random.randint(1,len(alphabet_array)-1)] + non_terminals_array[random.randint(1,len(non_terminals_array)-1)] + " " + 'ε'
                break
            elif type_of_derivation == 2 and flag:
                productions = productions + " ε" 
                break
            elif type_of_derivation == 3 and flag == False:
                productions = "ε"
                break
            else:
                productions = alphabet_array[random.randint(1,len(alphabet_array)-1)] + non_terminals_array[random.randint(1,len(non_terminals_array)-1)] + alphabet_array[random.randint(1,len(alphabet_array)-1)] + " " + alphabet_array[random.randint(1,len(alphabet_array)-1)] + " " + productions
                flag = True
            
            i += 1
        print(productions)

    return ""


def main():
    grammar_generator()


if __name__ == '__main__':
    main()