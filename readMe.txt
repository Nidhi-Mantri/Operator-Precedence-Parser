Requirements :-  "sys" library
	        :- "re" library
	        :- "prettytable" library

1.   Input should be given in the exact manner as in the input file.
2.  There must be a space before and after '|', ':', '->'.
3.   Epsilon is denoted by '#'
4.   Proper error handling -> no two same variables, terminals.
5.   All the variables used in productions and in defined in the main variable list must be same. Same for terminals
6.   Single start variable. Name of any variable and any terminal should be of length 1(i.e. single character).
7.   Any grammar that contains epsilon even after the process of removal of epsilon, is not allowed.
	(Ex: - S -> AB | #,  A -> 0A | #, B -> 1B | #) -> this grammar is not allowed.
8.    If there is any violations of above conditions, then it gives the corresponding error in the output file and program will terminate and won't proceed further.
9.   If there are consecutive variables present even after the processing(removal of two consecutive variables), it will terminate not won't proceed further. :-
	Ex : - E -> EE | Ea | Eb | a, this is not an OP Grammar
10.    Output is in the output file, there is nothing to be displayed on console. 

opp_grammar.py : - 
Input file is : - input.txt
Output file is : - op_grammar.txt
This Output.txt contains both leading and trailing set and precedence relation table as well.
If there are multiple entries in the table, it will gives the corresponding output.