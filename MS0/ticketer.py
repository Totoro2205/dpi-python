#==============================================================================
 #   Assignment:  Milestone 0
 #
 #       Author:  Bruno Alexander Cremonese de Morais
 #     Language:  Python, using argparse, datetime and random libraries
 #   To Compile:  python3 .\ticketer.py [-h] [-quick] [-pick PICK PICK PICK PICK PICK PICK PICK] [-encore]
 #
 #        Class:  DPI 912: Python for Programmers: Sockets and Security
 #    Professor:  Harvey Kaduri
 #     Due Date:  May 26th, 2020
 #    Submitted:  May 26th, 2020
 #
 #-----------------------------------------------------------------------------
 #
 #  Description:  This program generates tickets following the business rules of OLG's Lotto Max using Quick Pick, Pick Your Own and Encore's logic.
 #
 #        Input:  The program requires different inputs depending on the type of ticket the user wants generated,
 #                  as outlined below: 
 #                      ticketer.py -quick : will generate a Quick Pick ticket, if the switch -encore is added, the numbers are added to the Encore draw
 #                      ticketer.py -pick x x x x x x x : will generate a Pick Your Own ticket, the numbers on the ticket to be picked need to be added 
 #                                           right after the switch, if the switch -encore is added, the numbers are added to the Encore draw
 #
 #       Output:  The program outputs the 3 generated ticket lines with the current date and a text indicating if Encore was played or not
 #
 #    Algorithm:  The program has a pool of numbers following Lotto Max's 1 to 50 from which users can pick for Pick Your Own tickets and from which
 #                  random ticket numbers are generated for the subsequent lines using the numbers on the pool for the whole ticket on Quick Pick tickets using the random library.
 #                  The algorithm also validates user inputs against invalid values that are outside the pool and/or are not integers, or duplicates.
 #                  CLI switches are used to give users options for ticket generation and process the values that the users will input for Pick Your Own tickets.
 #
 #   Required Features Not Included:  None
 #
 #   Known Bugs:  No known bugs
 #
 #   Classification: N/A
 #
#==============================================================================

#!/usr/bin/python3

import argparse
from ticket import LottoTicket, QuickPick, PickYourOwn

switchParser = argparse.ArgumentParser(description="This script will generate you a lotto ticket!")
#Quick Pick Switch
switchParser.add_argument('-quick', help="Quick Pick will generate you a quick pick lotto ticket with randomly selected numbers.", required=False, action='store_true')
#Pick Your Own Switch
switchParser.add_argument('-pick', help="Pick Your Own will generate you a pick your own ticket, select 7 unique numbers between 1 & 50 and we will generate another 2 sets of random numbers for your ticket.", required=False, nargs=7)
switchParser.add_argument('-encore', help="Encore will be added to your ticket for more chances to win!", required=False, action='store_true')

args = switchParser.parse_args()

if __name__ == "__main__":

    ticket = LottoTicket()
    try:
        if(args.quick):

            if(args.encore):
                ticket = QuickPick(True)
            else:
                ticket = QuickPick(False)

        elif(args.pick):
            argsAsInt = []

            try:
                argsAsInt = list(map(int, args.pick))
            except ValueError as ex:
                raise ValueError("Invalid value inserted, please insert only numbers")

            if(args.encore):
                ticket = PickYourOwn(argsAsInt, True)
            else:
                ticket = PickYourOwn(argsAsInt, False)

        elif(args.encore):
            raise AttributeError("The encore argument must be used with a Quick Pick or a Pick Your Own ticket")
        else:
            raise AttributeError("None or invalid arguments given, ticket not generated!")

        ticket.printTicket()

    except ValueError as ex:
        print(ex)
    except AttributeError as ex:
        print(ex)
