# Final project for the subject Formal Languages and Compilers

***

### Top-Down parser and Bottom-UP parser
This project is an implementation of two parsing algorithms for context-free languages, a top-down parser, and a bottom-up parser. The top-down parser is made for LL(1) grammars and uses parsing to know if a given string is part of the language the given grammar describes. On the other hand, the bottom-up algorithm is made for LR(0) grammars, it first constructs the LR(0) automaton and then uses an SLR parser to know if a given string is part of the language the grammar describes.

***

## Build
To build this project simply clone this repository using the following command:
```
git clone https://github.com/JuanM0412/SyntaxAnalysis.git
```
This will create a directory call SyntaxAnalysis, you can acces to this directory using:
```
cd SyntaxAnalysis
```
Here you are going to find the follow archives:

* `main.py`. This is the file you must run to use one of the parsers or the grammar generator.
* `grammars.txt`. Here you can find some grammars to test in the parsers, as well as some strings.
* `Readme.med`. This file.

You can also see a directory called `src`. Here are the parsers and the grammar generator.

To run the program we recommend using Python 3.10.10 because the program was built using this version of Python.

If you don't know your Python version you can use the follow command if you are using a Linux system:
```
python -V
```
The output will be:
```
Python x.xx.xx
```
Where x.xx.xx represents the version of Python you have on your OS.

***

## Usage
To use the program you must run the main.py file.
```
python main.py
```
To use parsers such as the grammar generator, the following options are available:

`python main.py -g`. Where the -g option means grammar generator. This will execute the grammar generator.

`python main.py -td`. Where the -td option means Top-Down parsing. This will execute the Top-Down parsing.

`python main.py -bu`. Where the -bu option means Bottom-Up parsing. This will execute the Bottom-Up parsing.

`python main.py`. This will show you a menu, where you can choose among one of the three options (g, td, bu).

If you have choose one of the parsers, you have to put the grammar as follows:
```
terminal_1 terminal_2 ... terminal_n
non-terminal_1 non-terminal_2 ... non-terminal_n
derivation_1 for the non-terminal_1 ... derivation_m for the non-terminal_1
derivation_1 for the non-terminal_2 ... derivation_m for the non-terminal_2
...
derivation_1 for the non-terminal_n ... derivation_m for the non-terminal_n
```

### Some clarifications
* **The first non-terminal in the line of the non-terminals symbols is going to be the initial symbol of the grammar.**
* **Each terminal, non-terminal and derivations must be separated for one space.**

***

## Example of usage
1. Run the program. 
    ```
    python main.py -tp
    ```
2. Enter the grammar.
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
3. Enter the string that you want to test.
    ```
    (i*i+(i*i))+(i+i)*(i)
    ```
    If the string belongs to the grammar (as in this case), we will get the following message:
    ```
    (i*i+(i*i))+(i+i)*(i) is valid
    ```
    On the other hand, if the string doesn't belong to the grammar (like `()`), we will get the following message:
    ```
    () is invalid
    ```
    Once we get the answer of the program (whatever the result is, valid or invalid), we can enter a new string in the same way we had done it.

    If we want to stop the execution of the program we can enter `;` or use `ctrl+c`.

**If the grammar is not LL(1) (in this case we are running Top-Down parsing), we will not be able to enter a string to test the parser, so we will see a message indicating that the grammar is not LL(1). And the execution will stop.**

***

## Contributors
* ***Juan Manuel Gómez***
* ***Miguel Ángel Hoyos***