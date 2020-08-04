# Alex Moozhayil

#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        check_true_false
# Purpose:     Main entry into logic program. Reads input files, creates 
#              base, tests statement, and generates result file.
#
# Created:     09/25/2011
# Last Edited: 07/22/2013     
# Citation:       *Ported by Christopher Conly from C++ code supplied by Dr. 
#               Vassilis Athitsos.
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so I put it in a list, which
#               is passed by reference.
#              *Written to be Python 2.4 compliant for omega.uta.edu
#
#Additional cititation: used Dr. Vassilis Athitsos PowerPoint slides on TT-entails.
#                       He covered, in detail, all the necessary functions and how to 
#                       address the problem step by step. Link below:
#                       http://vlm1.uta.edu/~athitsos/courses/cse4308_fall2016/lectures/03a_tt_entails.pdf
#                   
#-------------------------------------------------------------------------------

import sys
from logical_expression import *

def main(argv):
    if len(argv) != 4:
        print('Usage: %s [wumpus-rules-file] [additional-knowledge-file] [input_file]' % argv[0])
        sys.exit(0)

    # Read wumpus rules file
    try:
        input_file = open(argv[1], 'r')
    except:
        print('failed to open file %s' % argv[1])
        sys.exit(0)

    add_sym = {}

    # Create the knowledge base with wumpus rules
    print('\nLoading wumpus rules...')
    knowledge_base = logical_expression()
    knowledge_base.connective = ['and']
    for line in input_file:
        # Skip comments and blank lines. Consider all line ending types.
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue
        counter = [0]  # A mutable counter so recursive calls don't just make a copy
        ######

        
        truth_value = line.rstrip('\r\n').split()

        if len(truth_value) == 1:
            add_sym[line[0]] = True
        elif len(truth_value) == 2 and truth_value[0][1:] == 'not':
            symbol =  truth_value[1]
            symbol = symbol[:-1]
            add_sym[symbol] = False


        ######
        subexpression = read_expression(line.rstrip('\r\n'), counter)
        knowledge_base.subexpressions.append(subexpression)
    input_file.close()

    # Read additional knowledge base information file
    try:
        input_file = open(argv[2], 'r')
    except:
        print('failed to open file %s' % argv[2])
        sys.exit(0)

    # Add expressions to knowledge base
    print('Loading additional knowledge...')
    for line in input_file:
        # Skip comments and blank lines. Consider all line ending types.
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue

        #####
        truth_value = line.rstrip('\r\n').split()

        if len(truth_value) == 1:
            add_sym[line[0]] = True
        elif len(truth_value) == 2 and truth_value[0][1:] == 'not':
            symbol =  truth_value[1]
            symbol = symbol[:-1]
            add_sym[symbol] = False


        counter = [0]  # a mutable counter

        ####

        subexpression = read_expression(line.rstrip('\r\n'), counter)
        knowledge_base.subexpressions.append(subexpression)
    input_file.close()

    # Verify it is a valid logical expression
    if not valid_expression(knowledge_base):
        sys.exit('invalid knowledge base')

    # I had left this line out of the original code. If things break, comment out.
    print_expression(knowledge_base, '\n')

    # Read statement whose entailment we want to determine
    try:
        input_file = open(argv[3], 'r')
    except:
        print('failed to open file %s' % argv[3])
        sys.exit(0)
    print('Loading statement...')
    statement = input_file.readline().rstrip('\r\n')
    input_file.close()
    
    # Convert statement into a logical expression and verify it is valid
    statement = read_expression(statement)
    if not valid_expression(statement):
        sys.exit('invalid statement')

    # Show us what the statement is
    print('\nChecking statement: ')
    print_expression(statement, '')
    #print

    #####
    statement_complement = logical_expression()
    statement_complement.connective = ['not']
    statement_complement.subexpressions.append(statement)

    if not valid_expression(statement_complement):
        sys.exit("The negation is not valid")

    TT_entails_result = TT_Entails(knowledge_base, statement, add_sym)
    not_TT_entails_result = TT_Entails(knowledge_base, statement_complement, add_sym)
    out_file = open("result.txt", "w")

    if TT_entails_result == True and not_TT_entails_result == False:
        print("\nDefinitely True\n")
        out_file.write("Definitely True\n")
    elif TT_entails_result == False and not_TT_entails_result == True:
        print("\nDefinitely False\n")
        out_file.write("Definitely False\n")
    elif TT_entails_result == False and not_TT_entails_result == False:
        print("\nPossbily True, possibly False\n")
        out_file.write("Possbily True, possibly False\n")
    elif TT_entails_result == True and not_TT_entails_result == True:
        print("\nBoth True and False\n")
        out_file.write("Both True and False\n")


    #####

    # Run the statement through the inference engine
    #check_true_false(knowledge_base, statement)
    out_file.close()
    sys.exit(1)
    

if __name__ == '__main__':
    main(sys.argv)
