#Final project for the subject Formal Languages and Compilers
***
###Top-Down parser and Bottom-UP parser

This project is an implementation of two parsing algorithms for context-free languages, a top-down parser, and a bottom-up parser. The top-down parser is made for LL(1) grammars and uses parsing to know if a given string is part of the language the given grammar describes. On the other hand, the bottom-up algorithm is made for LR(0) grammars, it first constructs the LR(0) automaton and then uses an SLR parser to know if a given string is part of the language the grammar describes.