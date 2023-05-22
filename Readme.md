# Final project for the subject Formal Languages and Compilers
***
### Top-Down parser and Bottom-UP parser

This project is an implementation of two parsing algorithms for context-free languages, a top-down parser, and a bottom-up parser. The top-down parser is made for LL(1) grammars and uses parsing to know if a given string is part of the language the given grammar describes. On the other hand, the bottom-up algorithm is made for LR(0) grammars, it first constructs the LR(0) automaton and then uses an SLR parser to know if a given string is part of the language the grammar describes.


### Usage
If you want to use the Top-Down parser all you have to do is run the top_down_parsing.py file as follows:
```
python top_down_parsing.py
```
Once you have done this, the program is already running.
Next, you have to put the grammar as follows:
```
terminal_1 terminal_2 ... terminal_n
non-terminal_1 non-terminal_2 ... non-terminal_n
derivation_1 for the non-terminal_1 ... derivation_m for the non-terminal_1
derivation_1 for the non-terminal_2 ... derivation_m for the non-terminal_2
...
derivation_1 for the non-terminal_n ... derivation_m for the non-terminal_n
```
Each terminal, non-terminal and derivations must be separated for one space.
Example:
```
i ( ) + * ε
E R T Y F
TR
+TR ε
FY
*FY ε
(E) i
```
This grammar represents:
```
E -> TR
R -> +TR | ε
T -> FY
Y -> *FY | ε
F -> (E) | i
```
**The first non-terminal in the line of the non-terminals symbols is going to be the initial symbol of the grammar**