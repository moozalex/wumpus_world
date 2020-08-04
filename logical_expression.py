#Alex Moozhayil

#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        logical_expression
# Purpose:     Contains logical_expression class, inference engine,
#              and assorted functions
#
# Created:     09/25/2011
# Last Edited: 07/22/2013  
# Notes:       *This contains code ported by Christopher Conly from C++ code
#               provided by Dr. Vassilis Athitsos
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so put it in a list which is
#               passed by reference. We can also now pass just one variable in
#               the class and the function will modify the class instead of a
#               copy of that variable. So, be sure to pass the entire list to a
#               function (i.e. if we have an instance of logical_expression
#               called le, we'd call foo(le.symbol,...). If foo needs to modify
#               le.symbol, it will need to index it (i.e. le.symbol[0]) so that
#               the change will persist.
#              *Written to be Python 2.4 compliant for omega.uta.edu
#Additional cititation: used Dr. Vassilis Athitsos PowerPoint slides on TT-entails.
#                       He covered, in detail, all the necessary functions and how to 
#                       address the problem step by step.
#                       http://vlm1.uta.edu/~athitsos/courses/cse4308_fall2016/lectures/03a_tt_entails.pdf
#-------------------------------------------------------------------------------

import sys
from copy import deepcopy

#-------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos
class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []


def print_expression(expression, separator):
    """Prints the given expression using the given separator"""
    if expression == 0 or expression == None or expression == '':
        print('\nINVALID\n')

    elif expression.symbol[0]: # If it is a base case (symbol)
        sys.stdout.write('%s' % expression.symbol[0])

    else: # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':  # It's the beginning of a connective
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print('\nUnexpected end of input.\n')
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    word = ''
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):
    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
         expression.connective[0].lower() != 'or' and \
         expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
#-------------------------------------------------------------------------------

# Add all your functions here

def TT_Entails(knowledge_base, alpha, add_sym):
    list_symbol = []
    extract_symbols(knowledge_base, list_symbol)
    extract_symbols(alpha, list_symbol)
    model = {}
    return TT_Check_All(knowledge_base, alpha, list_symbol, model, add_sym)

def TT_Check_All(knowledge_base, alpha, symbols, model, add_sym):
    if len(symbols) == 0:
        if PL_True(knowledge_base, model):
            return PL_True(alpha, model)
        else:
            return True
    else:
        popped = symbols.pop(0)
        rest_one = deepcopy(symbols)
        rest_two = deepcopy(symbols)

        if popped in add_sym:
            return TT_Check_All(knowledge_base, alpha, rest_one, extend(popped, add_sym[popped], model), add_sym)
        else:
            return TT_Check_All(knowledge_base, alpha, rest_one, extend(popped, True, model), add_sym) and TT_Check_All(knowledge_base, alpha, rest_two, extend(popped, False, model), add_sym)


def extend(P, value, model):
    model[P] = value
    return model

def extract_symbols(sentence, symbols):
    if not sentence.subexpressions:
        return sentence.symbol[0]
    for child in sentence.subexpressions:
        extraction = extract_symbols(child, symbols)
        if extraction not in symbols and extraction is not None:
            symbols.append(extraction)

def PL_True(sentence, model):
    if sentence.symbol[0] != '':
        return model[sentence.symbol[0]]

    elif sentence.connective[0] == "and":
        for child in sentence.subexpressions:
            if PL_True(child, model) == False:
                return False
        return True
    elif sentence.connective[0] == "or":
        for child in sentence.subexpressions:
            if PL_True(child, model) == True:
                return True
        return False
    elif sentence.connective[0] == "if":
        left = sentence.subexpressions[0]
        right = sentence.subexpressions[1]
        if PL_True(left, model) == True and PL_True(right, model) == False:
            return False
        return True
    elif sentence.connective[0] == "iff":
        left = sentence.subexpressions[0]
        right = sentence.subexpressions[1]
        if PL_True(left, model) == PL_True(right, model):
            return True
        return False
    elif sentence.connective[0] == "not":
        child = sentence.subexpressions[0]
        if PL_True(child, model) == True:
            return False
        elif PL_True(child, model) == False:
            return True
    elif sentence.connective[0] == "xor":
        left = sentence.subexpressions[0]
        right = sentence.subexpressions[1]
        if PL_True(left, model) == PL_True(right, model):
            return False
        return True

