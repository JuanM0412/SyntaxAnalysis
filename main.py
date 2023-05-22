import sys
from src.top_down_parsing import top_down
from src.bottom_up_parsing import bottom_up
from src.grammar_generator import grammar_generator


def main(args):
    if len(args) == 1:
        if args[0] == '-td':
            top_down()
        elif args[0] == '-bu':
            bottom_up()
        elif args[0] == '-g':
            grammar_generator()

    else:
        arg = input('Choose an option between Bottom-Up parsing (bu), Top-Down parsing (td) and Grammar generator (g): ')
        while arg != 'td' and arg != 'bu' and arg != 'g':
            arg = input('Please, choose a valid option between Bottom-Up parsing (bu) Top-Down parsing (td) and Grammar generator (g): ')

        if arg == 'td':
            top_down()
        elif arg == 'bu':
            bottom_up()
        else:
            grammar_generator()

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)