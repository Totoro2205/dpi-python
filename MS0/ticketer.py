#!/usr/bin/env python3

# ==============================================================================
#   Assignment:  Milestone 1
#
#       Author:  Bruno Alexander Cremonese de Morais
#     Language:  Python, using argparse, datetime and random libraries
#   To Compile:  python3 .\ticketer.py [-h] [-port PORT]
#
#        Class:  DPI 912: Python for Programmers: Sockets and Security
#    Professor:  Harvey Kaduri
#     Due Date:  June 2nd, 2020
#    Submitted:  June 2nd, 2020
#
# -----------------------------------------------------------------------------
#
#    Description:  This program generates tickets following the business rules of OLG's Lotto Max using Quick Pick, Pick Your Own and Encore's logic. It is a "daemon" that processes
#                   client requests for tickets and sends them back to the clients for saving and display
#
#    Input:  The program requires the port on which the daemon will listen to for setup, by default it will listen on port 5111
#
#    Output:  The program returns the tickets to the client as a manually serialized string to be deserialized on the client side
#
#    Algorithm:  The program has a pool of numbers following OLG's Lotto Max, Lottario or Lotto 649 1 to 45/49 or 50 from which users can pick for Pick Your Own tickets and from which
#                  random ticket numbers are generated for the subsequent ticketLines using the numbers on the pool for the whole ticket on Quick Pick tickets using the random library.
#                  The algorithm also validates user inputs against invalid values that are outside the pool and/or are not integers, or duplicates.
#                  CLI switches are used to give users options for ticket generation and process the values that the users will input for Pick Your Own tickets on the client side creating the request
#                  The request is then processed by the daemon, sent back to the client and deserialized for display and saving it to a file.
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


if __name__ == "__main__":
    print("Welcome to your Python Lotto Ticket Server!")
    while True:
        socketManager = ServerSocketManager(args.port)
        request = clientTicketDataParser(socketManager.receiveData())
        try:
            tickets = request.getTickets()
            serializedTicket = ''
            for ticket in tickets:
                serializedTicket += ticket.serializeTicket()
                if ticket is not tickets[-1]:
                    serializedTicket += '|'
            socketManager.sendData(serializedTicket)
            socketManager.closeConnection()
            del socketManager
        except Exception as ex:
            socketManager.sendErrorAndCloseConnection(ex)
            del socketManager
