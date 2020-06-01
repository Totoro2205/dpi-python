#!/usr/bin/env python3

# ==============================================================================
#   Assignment:  Milestone 0
#
#       Author:  Bruno Alexander Cremonese de Morais
#     Language:  Python, using argparse, datetime and random libraries
#   To Compile:  python3 .\ticketer.py [-h] (-sixfournine | -lottario | -lottomax) [-quick] [-pick PICK [PICK ...]] [-encore]
#
#        Class:  DPI 912: Python for Programmers: Sockets and Security
#    Professor:  Harvey Kaduri
#     Due Date:  May 26th, 2020
#    Submitted:  May 26th, 2020
#
# -----------------------------------------------------------------------------
#
#  Description:  This program generates tickets following the business rules of OLG's Lotto Max using Quick Pick, Pick Your Own and Encore's logic.
#
#        Input:  The program requires different inputs depending on the type of ticket the user wants generated,
#                  as outlined below:
#                      ticketer.py (-type) -quick : will generate a Quick Pick ticket, if the switch -encore is added, the numbers are added to the Encore draw
#                      ticketer.py (-type)  -pick x x x x x x x : will generate a Pick Your Own ticket, the numbers on the ticket to be picked need to be added
#                                           right after the switch, if the switch -encore is added, the numbers are added to the Encore draw
#
#       Output:  The program outputs the 2 or 3 generated ticket ticketLines with the current date and a text indicating if Encore was played or not
#
#    Algorithm:  The program has a pool of numbers following OLG's Lotto Max, Lottario or Lotto 649 1 to 45/49 or 50 from which users can pick for Pick Your Own tickets and from which
#                  random ticket numbers are generated for the subsequent ticketLines using the numbers on the pool for the whole ticket on Quick Pick tickets using the random library.
#                  The algorithm also validates user inputs against invalid values that are outside the pool and/or are not integers, or duplicates.
#                  CLI switches are used to give users options for ticket generation and process the values that the users will input for Pick Your Own tickets.
#
#   Required Features Not Included:  None
#
#   Known Bugs:  No known bugs
#
#   Classification: N/A
#
# ==============================================================================

import argparse
from ticket import LottoTicket, QuickPick, PickYourOwn, LottoSixFortyNine, Lottario, LottoMax, TicketRequest
from socketManager import ServerSocketManager

switchParser = argparse.ArgumentParser(
    description="Welcome to your Python Lotto Ticket Server!")

# Port selector
switchParser.add_argument(
    '-port',
    help="Port the server will listen on",
    required=False,
    default=5111,
    type=int,
    nargs=1)

args = switchParser.parse_args()

def clientTicketDataParser(commandData):
    if not commandData:
        raise ValueError("Empty Command Received By The Client!")
    request = TicketRequest()
    request.deserializeRequest(commandData)
    return request

def requestProcessor(request):
    if(request.pickedNumbers):
        totalNumbers = len(request.pickedNumbers)
    else:
        totalNumbers = -1

    if(request.playType == "SFN"):
        if(totalNumbers != 6 and totalNumbers != -1):
            raise ValueError(
                "You picked {0} numbers. Please pick six numbers for your Lotto 649 Ticket".format(totalNumbers))
        baseTicket = LottoSixFortyNine()

    elif(request.playType == "LTR"):
        if(totalNumbers != 6 and totalNumbers != -1):
            raise ValueError(
                "You picked {0} numbers. Please pick six numbers for your Lottario Ticket".format(totalNumbers))
        baseTicket = Lottario()

    elif(request.playType == "LMX"):
        if(totalNumbers != 7 and totalNumbers != -1):
            raise ValueError(
                "You picked {0} numbers. Please pick seven numbers for your LottoMax Ticket".format(totalNumbers))
        baseTicket = LottoMax()

    if(request.ticketType == "Q"):
        if(request.encorePlayed):
            ticket = QuickPick(True, baseTicket)
        else:
            ticket = QuickPick(False, baseTicket)
    elif(request.ticketType == "P"):
        if(request.encorePlayed):
            ticket = PickYourOwn(request.pickedNumbers, True, baseTicket)
        else:
            ticket = PickYourOwn(request.pickedNumbers, False, baseTicket)
    elif(request.encorePlayed):
        raise AttributeError(
            "The encore argument must be used with a Quick Pick or a Pick Your Own ticket")
    else:
        raise AttributeError(
            "None or invalid arguments given, ticket not generated! Please pick a ticket mode, either Quick Pick or Pick Your Own Ticket. Use the -h switch if required.")
    return ticket

if __name__ == "__main__":
    print("Welcome to your Python Lotto Ticket Server!")
    socketManager = ServerSocketManager(args.port)
    try:
        request = clientTicketDataParser(socketManager.receiveData())
        ticket = requestProcessor(request)
        socketManager.sendData(ticket.serializeTicket())
        socketManager.closeConnection()
    except Exception as ex:
        socketManager.sendErrorAndCloseConnection(ex)
