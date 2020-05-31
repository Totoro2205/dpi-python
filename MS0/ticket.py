from datetime import date
import random


class LottoTicket:
    numberPool = []
    ticketLines = []
    encorePlayed = False
    numbersLength = 0
    date = date.today()
    ticketType = ""
    playType = ""
    uniqueIdentifier = ""

    # Random Number Generator for Lotto tickets
    def randomLineGenerator(self):
        returnList = []
        while len(returnList) < self.numbersLength:
            number = random.choice(self.numberPool)
            returnList.append(number)
            self.numberPool.remove(number)
        return returnList

    # Unique Identifier Generator
    def generateUniqueIdentifier(self):
        self.uniqueIdentifier = self.ticketType + self.playType + self.date + "." + random.randint(100000, 999999)

    # Ticket Lines Printer
    def printTicketLines(self):
        for line in self.ticketLines:
            if(self.ticketLines.index(line) == 1):
                print("-------------------------")
            print(*line, sep="  ")
        if(self.encorePlayed):
            print("--- Encore Played ---")
        else:
            print("--- Encore Not Played ---")

    #Ticket Serialization
    def serializeTicket(self):
        serializationBuffer = []
        serializationBuffer.append(self.date)
        serializationBuffer.append(self.uniqueIdentifier)
        serializationBuffer.append(self.ticketType)
        serializationBuffer.append(self.playType)
        serializationBuffer.append(self.ticketLines)
        serializationBuffer.append(self.encorePlayed)
        return serializationBuffer
    
    #Ticket Deserialization
    def deserializeTicket(self, serializationBuffer):
        self.date = serializationBuffer[0]
        self.uniqueIdentifier = serializationBuffer[1]
        self.ticketType = serializationBuffer[2]
        self.playType = serializationBuffer[3]
        self.ticketLines = serializationBuffer[4]
        self.encorePlayed = serializationBuffer[5]


# Ticket Types
class LottoMax(LottoTicket):
    # Constructor
    def __init__(self):
        self.ticketType = "LMX"
        self.numbersLength = 7
        self.numberPool = list(range(1, 50))
        self.ticketLines.append(self.randomLineGenerator())

class LottoSixFortyNine(LottoTicket):
    # Constructor
    def __init__(self):
        self.ticketType = "SFN"
        self.numbersLength = 6
        self.numberPool = list(range(1, 49))

class Lottario(LottoTicket):
    # Constructor
    def __init__(self):
        self.ticketType = "LTR"
        self.numbersLength = 6
        self.numberPool = list(range(1, 45))

# Game Types
class QuickPick(LottoTicket):

    # Constructor
    def __init__(self, encorePlayed, lottoTicket):
        self.playType = "Q"
        self.ticketType = lottoTicket.ticketType
        self.numberPool = lottoTicket.numberPool
        self.numbersLength = lottoTicket.numbersLength
        self.ticketLines.append(self.randomLineGenerator())
        self.ticketLines.insert(0, self.randomLineGenerator())
        self.encorePlayed = encorePlayed

    # Ticket Printer
    def printTicket(self):
        print(self.date)
        print("--- Quick Pick Ticket ---")
        self.printTicketLines()

class PickYourOwn(LottoTicket):

    # Constructor
    def __init__(self, firstLine, encorePlayed, lottoTicket):
        self.playType = "P"
        self.ticketType = lottoTicket.ticketType
        self.numberPool = lottoTicket.numberPool
        self.numbersLength = lottoTicket.numbersLength
        self.ticketLines.append(self.randomLineGenerator())
        self.ticketLines.insert(0, firstLine)
        self.validateInput()
        self.encorePlayed = encorePlayed

    # Validates User's Input against duplicates or numbers out of the pool
    def validateInput(self):
        for number in self.ticketLines[0]:
            if(number not in self.numberPool):
                raise ValueError(
                    "Invalid value inserted: {0}, please selected a number between 1 & {1}".format(
                        number, max(
                            self.numberPool)))
            if(self.ticketLines[0].count(number) > 1):
                raise ValueError(
                    "Duplicate value inserted: {0}, please insert only unique numbers between 1 & {1}".format(
                        number, max(
                            self.numberPool)))

    # Ticket Printer
    def printTicket(self):
        print(self.date)
        print("--- Pick Your Own Ticket ---")
        self.printTicketLines()

# Ticket request sent by the client and read by the server
class TicketRequest:

    def __init__(self, playType = None, ticketType = None, encorePlayed = False, pickedNumbers = None):
        self.playType = playType
        self.ticketType = ticketType
        self.encorePlayed = encorePlayed
        self.pickedNumbers = pickedNumbers

    # Request Serialization
    def serializeRequest(self):
        serializationBuffer: str = ''
        serializationBuffer += self.ticketType
        serializationBuffer += self.playType
        serializationBuffer += '_'
        if self.pickedNumbers is not None:
            serializationBuffer += len(self.pickedNumbers)
            for number in self.pickedNumbers:
                serializationBuffer += number
        serializationBuffer += '_'
        if self.encorePlayed:
            serializationBuffer += '1'
        else:
            serializationBuffer += '0'
        return serializationBuffer
    
    # Request Deserialization
    def deserializeRequest(self, serializationBuffer):
        self.ticketType = serializationBuffer[0]
        self.playType = serializationBuffer[1]
        if serializationBuffer[2] is not None:
            length = serializationBuffer[2]
            for i in length:
                self.pickedNumbers = serializationBuffer[i]
            self.encorePlayed = serializationBuffer[length + 2]
        else:
            self.pickedNumbers = serializationBuffer[2]
            self.encorePlayed = serializationBuffer[3]
        
    