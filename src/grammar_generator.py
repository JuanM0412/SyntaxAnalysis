import random


def grammar_generator():
    terminals = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', '+', ')',
                 '(', '%', '#', '&', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    non_terminals = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                     'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    number_of_terminals = random.randint(2, 5)
    number_of_non_terminals = random.randint(2, 5)
    # in this string we save the set of terminals. We use a string for print in a easily way according to our input for the analyzers
    alphabet = ""
    # in this string we save the set of non_terminals. We use a string for print in a easily way according to our input for the analyzers
    non_terminals_string = ""
    i = 1
    while i <= number_of_terminals:
        # it select a random terminal to put in the grammar
        terminal = terminals[random.randint(1, len(terminals)-1)]
        # the terminal is eliminated to avoid have the same element in the set two times
        terminals.remove(terminal)
        # concatenate the terminal in the alphabet
        alphabet = terminal + " " + alphabet
        i += 1

    print(alphabet)
    i = 1
    while i <= number_of_non_terminals:
        # it select a random non_terminal to put in the grammar
        non_terminal = non_terminals[random.randint(1, len(non_terminals)-1)]
        # the non_terminal is eliminated to avoid have the same element in the set two times
        non_terminals.remove(non_terminal)
        # concatenate the non_terminal in the set
        non_terminals_string = non_terminal + " " + non_terminals_string
        i += 1

    print(non_terminals_string)
    # We convert the two sets in arrays to handle them more easily
    non_terminals_array = non_terminals_string.split()
    alphabet_array = alphabet.split()
    # in this for we create the productions for each non_terminal
    for non_terminal in non_terminals_array:
        # create an arbitrary number of productions
        number_of_productions = random.randint(1, 4)
        productions = ""
        # this set is used as a memmory. Avoid repeat productions
        rules = set()
        # We create an obligation to the initial symbol. Avoid that derivates in just epsilon
        if non_terminal == non_terminals_array[0]:
            new_rule = alphabet_array[random.randint(1, len(alphabet_array) - 1)] + non_terminals_array[random.randint(1, len(non_terminals_array)-1)] + alphabet_array[random.randint(1, len(alphabet_array) - 1)] + " " + alphabet_array[random.randint(1, len(alphabet_array)-1)] + " "
            rules.update(new_rule)
            productions = alphabet_array[random.randint(1, len(alphabet_array) - 1)] + non_terminals_array[random.randint(1, len(non_terminals_array)-1)] + alphabet_array[random.randint(1, len(alphabet_array) - 1)] + " " + alphabet_array[random.randint(1, len(alphabet_array)-1)] + " " + productions

        i = 1
        while i <= number_of_productions:
            # random to choose a kind of derivation
            type_of_derivation = random.randint(1, 4)
            # this flag is used to avoid that one derivation have epsilon two times in their derivations
            # if the flag is false and the type is 3, we agreggate just epsilon, otherwise, we cant.
            flag = False
            # creates a derivation abB and break the generations of more productions
            if type_of_derivation == 1:
                new_rule = alphabet_array[random.randint(1, len(alphabet_array)-1)] + alphabet_array[random.randint(
                    1, len(alphabet_array)-1)] + non_terminals_array[random.randint(1, len(non_terminals_array)-1)]
                if new_rule not in rules:
                    productions = alphabet_array[random.randint(1, len(alphabet_array)-1)] + alphabet_array[random.randint(
                        1, len(alphabet_array)-1)] + non_terminals_array[random.randint(1, len(non_terminals_array)-1)] + " " + 'ε'

                break
            # add the epsilon in a derivation that is not empty
            elif type_of_derivation == 2 and flag:
                productions = productions + " ε"
                break
            # add epsilon as the only derivation
            elif type_of_derivation == 3 and flag == False and non_terminal != non_terminals_array[0]:
                productions = "ε"
                break
            # creates a derivation aBbc
            else:
                new_rule = alphabet_array[random.randint(1, len(alphabet_array)-1)] + non_terminals_array[random.randint(1, len(
                    non_terminals_array)-1)] + alphabet_array[random.randint(1, len(alphabet_array)-1)] + alphabet_array[random.randint(1, len(alphabet_array)-1)] + " "
                if new_rule not in rules:
                    rules.update(new_rule)
                    productions = alphabet_array[random.randint(1, len(alphabet_array)-1)] + non_terminals_array[random.randint(1, len(
                        non_terminals_array)-1)] + alphabet_array[random.randint(1, len(alphabet_array)-1)] + alphabet_array[random.randint(1, len(alphabet_array)-1)] + " " + productions

                flag = True

            i += 1

        print(productions)

    # Ask for the number of tests
    num_of_str = int(input(("How many strings do you want?: ")))
    print("Strings to test:")
    # this set is used as a memmory. Avoid repeat tests
    test = set()
    # This for create a random string with elements of the alphabet. The strings do not repeat.
    for i in range(num_of_str):
        j = random.randint(1, 10)
        string = ""
        for n in range(j):
            string = string + alphabet_array[random.randint(1, len(alphabet_array) - 1)]
        if string not in test:
            print(string)
            test.update(string)
        else:
            # Concatenate the inverse of the test, to avoid repetitions.
            while string in test:
                string = string + string[::-1]

            print(string)
            test.update(string)

    return ""


if __name__ == '__main__':
    grammar_generator()