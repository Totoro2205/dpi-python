#==============================================================================
 #   Assignment:  Milestone 0
 #
 #       Author:  Bruno Alexander Cremonese de Morais
 #     Language:  NAME OF LANGUAGE IN WHICH THE PROGRAM IS WRITTEN AND THE
 #                      NAME OF ANY CLASSES OR LIBRARIES USED
 #   To Compile:  n/a
 #
 #        Class:  NAME AND TITLE OF CLASS 
 #    Professor:  NAME OF COURSE'S PROFESSOR
 #     Due Date:  DATE AND TIME THAT THIS PROGRAM IS/WAS DUE TO BE SUBMITTED
 #    Submitted:  DATE AND TIME THAT THIS PROGRAM WAS ACTUALLY SUBMITTED
 #
 #-----------------------------------------------------------------------------
 #
 #  Description:  DESCRIBE THE PROBLEM THAT THIS PROGRAM WAS WRITTEN TO
 #      SOLVE.
 #
 #        Input:  DESCRIBE THE INPUT THAT THE PROGRAM REQUIRES.
 #
 #       Output:  DESCRIBE THE OUTPUT THAT THE PROGRAM PRODUCES.
 #
 #    Algorithm:  OUTLINE THE APPROACH USED BY THE PROGRAM TO SOLVE THE
 #      PROBLEM.
 #
 #   Required Features Not Included:  DESCRIBE HERE ANY REQUIREMENTS OF
 #      THE ASSIGNMENT THAT THE PROGRAM DOES NOT ATTEMPT TO SOLVE OR
 #      IS UNSUCCESSFUL IN SOLVING.
 #
 #   Known Bugs:  IF THE PROGRAM DOES NOT FUNCTION CORRECTLY IN SOME
 #      SITUATIONS, DESCRIBE THE SITUATIONS AND PROBLEMS HERE.
 #
 #   Classification: If applicable, which classification are you attempting
 #
#==============================================================================

#!/usr/bin/python3

import argparse
from ticket import LottoTicket, QuickPick, PickYourOwn

switchParser = argparse.ArgumentParser(description="This script will generate you a lotto ticket!")
switchParser.add_argument('-qpk', help="Quick Pick Switch - QPK will generate you a quick pick lotto ticket", required=False)

switchParser.add_argument('-pyo', help="Pick Your Own Switch - PYO will generate you a pick your own ticket", required=False)
switchParser.add_argument('-enc', help="Encore Switch - ENC will generate an encore lotto ticket", required=False)

args = switchParser.parse_args()

if __name__ == "__main__":
    if(args.qpk):
        ticket = QuickPick()
        ticket.printTicket()
    elif(args.pyo):
        ticket = PickYourOwn([1, 2, 3 ,4 ,5 ,6 ,7])
        ticket.printTicket()
    elif(args.enc):
        print("ENC")