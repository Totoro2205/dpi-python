#!/usr/bin/env python3

# ==============================================================================
#   Assignment:  Milestone 1
#
#       Author:  Bruno Alexander Cremonese de Morais
#     Language:  Python, using argparse, datetime, socketManager and random libraries
#   To Compile:  python3 .\client.py [-h] (-sixfournine | -lottario | -lottomax) [-quick] [-pick PICK [PICK ...]] [-encore] -port PORT -host HOST -tickets TICKETS
#
#        Class:  DPI 912: Python for Programmers: Sockets and Security
#    Professor:  Harvey Kaduri
#     Due Date:  June 2nd, 2020
#    Submitted:  June 2nd, 2020
#
# -----------------------------------------------------------------------------
#
#  Description:  This program generates tickets following the business rules of OLG's Lotto Max using Quick Pick, Pick Your Own and Encore's logic.
#
#        Input:  The program requires different inputs depending on the type of ticket the user wants generated,
#                  as outlined below:
#                      client.py (-type) -quick : will generate a Quick Pick ticket, if the switch -encore is added, the numbers are added to the Encore draw
#                      client.py (-type)  -pick x x x x x x x : will generate a Pick Your Own ticket, the numbers on the ticket to be picked need to be added
#                                           right after the switch, if the switch -encore is added, the numbers are added to the Encore draw
#                   Added to the previous mentioned inputs, the port and host's IPV6 address to connect to the daemon are required as well as the amount of tickets to be generated
#
#       Output:  The program outputs the generated tickets with the unique ID and a text indicating if Encore was played or not as well as saves the same information to a file
#
#    Algorithm:  Based on the used switches the program creates a request file that is sent to the daemon so it can be processed and generate tickets based on user's input.
#                   It then deserializes the response and display and saves the tickets received from the daemon
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
from socketManager import ClientSocketManager

switchParser = argparse.ArgumentParser(
    description="Welcome to your Python Lotto Ticketer!")

# Ticket type selection
group = switchParser.add_mutually_exclusive_group(required=True)
group.add_argument(
    '-sixfournine',
    help="Generates a Lotto 649 ticket. If used with -pick select 6 numbers to play",
    action='store_true')
group.add_argument(
    '-lottario',
    help="Generates a Lottario ticket. If used with -pick select 6 numbers to play",
    action='store_true')
group.add_argument(
    '-lottomax',
    help="Generates a LottoMax ticket. If used with -pick select 7 numbers to play",
    action='store_true')

# Quick Pick Switch
switchParser.add_argument(
    '-quick',
    help="Quick Pick will generate you a quick pick lotto ticket with randomly selected numbers.",
    required=False,
    action='store_true')
# Pick Your Own Switch
switchParser.add_argument(
    '-pick',
    help="Pick Your Own will generate you a pick your own ticket, with numbers you picked! (6 or 7 numbers depending on your ticket type)",
    required=False,
    nargs='+')

switchParser.add_argument(
    '-encore',
    help="Encore will be added to your ticket for more chances to win!",
    required=False,
    action='store_true')

# Port selector
switchParser.add_argument(
    '-port',
    help="Port the server will listen on",
    required=True,
    default=5111,
    type=int,
    nargs=1)

# Host selector
switchParser.add_argument(
    '-host',
    help="Host server address",
    required=True,
    nargs=1)

# Ticket amount
switchParser.add_argument(
    '-tickets',
    help="Amount of tickets to be generated",
    required=True,
    nargs=1)

# Unique ID
switchParser.add_argument(
    '-uid',
    help="Unique ID to be generated",
    required=True,
    nargs=1)

args = switchParser.parse_args()

if __name__ == "__main__":
    print("Welcome to your Python Lotto Ticket Client!")
    socketManager = ClientSocketManager(args.host[0], args.port[0])

    try:
        request = TicketRequest()
        if(args.quick):
            request.playType = "Q"
            if(args.encore):
                request.encorePlayed = True

        elif (args.pick):
            request.playType = "P"
            argsAsInt = []
            try:
                argsAsInt = list(map(int, args.pick))
                request.pickedNumbers = argsAsInt
            except ValueError:
                raise ValueError(
                    "Invalid value inserted, please insert only numbers")
            if(args.encore):
                request.encorePlayed = True

        elif(args.encore):
            raise AttributeError(
                "The encore argument must be used with a Quick Pick or a Pick Your Own ticket")
        else:
            raise ValueError(
                "No valid play type selected, please select either a Quick Pick or Pick your own type of ticket")

        if(args.lottomax):
            request.ticketType = "LMX"
        elif (args.lottario):
            request.ticketType = "LTR"
        elif (args.sixfournine):
            request.ticketType = "SFN"
        else:
            raise ValueError(
                "No valid ticket type selected, please select either LottoMax, Lottario and Lotto Six Forty Nine")

        request.uid = args.uid[0]
        ticketAmount = int(args.tickets[0])
        request.ticketAmount = ticketAmount
        socketManager.sendData(request.serializeRequest())
        ticket = LottoTicket()
        serializedTickets = socketManager.receiveData()
        decodedTickets = serializedTickets.decode('utf-8')
        individualSerializeTickets = decodedTickets.split('|')

        for serializedTicket in individualSerializeTickets:
            ticket.deserializeTicket(serializedTicket)
            ticket.printAndSaveTicket()

        socketManager.closeConnection()
    except Exception as ex:
        socketManager.sendErrorAndCloseConnection(ex)
