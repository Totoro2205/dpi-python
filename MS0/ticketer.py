#!/usr/bin/env python3

# ==============================================================================
#   Assignment:  Milestone 2
#
#       Author:  Bruno Alexander Cremonese de Morais
#     Language:  Python, using argparse, datetime, os, signal and random libraries
#   To Compile:  python3 .\ticketer.py [-h] [-port PORT]
#
#        Class:  DPI 912: Python for Programmers: Sockets and Security
#    Professor:  Harvey Kaduri
#     Due Date:  June 9th, 2020
#    Submitted:  June 9th, 2020
#
# -----------------------------------------------------------------------------
#
#    Description:  This program generates tickets following the business rules of OLG's Lotto Max using Quick Pick, Pick Your Own and Encore's logic. It is a "daemon" that processes
#                   client requests for tickets and sends them back to the clients for saving and display. This program has also high availability and spawns "child" processes to handle
#                   user connections and their requests simultaneously.
#
#    Input:  The program requires the port on which the daemon will listen to for setup, by default it will listen on port 5111
#
#    Output:  The program returns the tickets to the client as a manually serialized string to be deserialized on the client side
#
#    Algorithm:  The program has a pool of numbers following OLG's Lotto Max, Lottario or Lotto 649 1 to 45/49 or 50 from which users can pick for Pick Your Own tickets and from which
#                  random ticket numbers are generated for the subsequent ticketLines using the numbers on the pool for the whole ticket on Quick Pick tickets using the random library.
#                  The algorithm also validates user inputs against invalid values that are outside the pool and/or are not integers, or duplicates.
#                  CLI switches are used to give users options for ticket generation and process the values that the users will input for Pick Your Own tickets on the client side creating the request
#                  The request is then processed by the daemon's "children", sent back separately to the clients and deserialized for display and saving it to a file.
#
#   Required Features Not Included:  None
#
#   Known Bugs:  No known bugs
#
#   Classification: N/A
#
# ==============================================================================

import argparse
import os
import signal
from ticket import LottoTicket, QuickPick, PickYourOwn, LottoSixFortyNine, Lottario, LottoMax, TicketRequest
from socketManager import ServerSocketManager
from concurrencyManager import ConcurrencyManager
from daemon import Daemon

switchParser = argparse.ArgumentParser(
    description="Welcome to your Python Lotto Ticket Server!")

# Port selector
switchParser.add_argument(
    '-port',
    help="Port the server will listen on",
    required=False,
    default=5111,
    nargs=1)

# Pool queue size
switchParser.add_argument(
    '-queue',
    help="Pool queue size",
    required=False,
    default=2,
    nargs=1)

args = switchParser.parse_args()


def clientRequestHandler(commandData, socketManager):
    if not commandData:
        raise ValueError("Empty Command Received By The Client!")
    request = TicketRequest()
    request.deserializeRequest(commandData)
    socketManager.sendData(request.getSerializedTickets())


def runDaemon(port, queueSize):
    concurrencyManager = ConcurrencyManager()
    socketManager = ServerSocketManager(port, queueSize)
    while True:
        try:
            socketManager.acceptConnections()
            socketManager.startDaemon(clientRequestHandler)
        except IOError as err:
            code, msg = err.args
            if code == errno.EINTR:
                continue
            else:
                raise


if __name__ == "__main__":
    print(args)
    if isinstance(args.queue, list):
        queueAmount = int(args.queue[0])
    else:
        queueAmount = args.queue

    if isinstance(args.port, list):
        port = int(args.port[0])
    else:
        port = args.port

    # We do not have sudo access to add it to /var/run so /tmp is a workaround. /var/run is the default on the Daemon class
    daemon = Daemon('/tmp/ticketer.pid')
    daemon.startDaemon()
    runDaemon(port, queueAmount)
    
