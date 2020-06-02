from datetime import date, datetime
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
            if(number not in returnList):
                returnList.append(number)
        return returnList

    # Unique Identifier Generator
    def generateUniqueIdentifier(self):
        return self.ticketType + self.playType + "." + self.date.strftime("%m%d%Y") + "." + str(random.randint(100000, 999999))

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
        serializationBuffer = ''
        serializationBuffer += self.uniqueIdentifier
        serializationBuffer += '_'
        serializationBuffer += self.ticketType
        serializationBuffer += '_'
        serializationBuffer += self.playType
        serializationBuffer += '_'

        serializedLinesString = ''
        for line in self.ticketLines: 
            for number in line:
                serializedLinesString += str(number)
                if number is not line[-1]:
                    serializedLinesString += '-'
            if line is not self.ticketLines[-1]:
                serializedLinesString += ':'
        serializationBuffer += serializedLinesString

        serializationBuffer += '_'
        if self.encorePlayed:
            serializationBuffer += '1'
        else:
            serializationBuffer += '0'
        return serializationBuffer
    
    #Ticket Deserialization
    def deserializeTicket(self, serializationBuffer):
        bufferAsString = str(serializationBuffer.decode('utf-8'))
        buffer = bufferAsString.split('_')
        self.uniqueIdentifier = buffer[0]
        self.ticketType = buffer[1]
        self.playType = buffer[2]
        ticketLineBuffer = buffer[3].split(':')
        for line in ticketLineBuffer:
            self.ticketLines.append(line.split('-'))
        if serializationBuffer[4] == 0:
            self.encorePlayed = True
        else:
            self.encorePlayed = False


# Ticket Types
class LottoMax(LottoTicket):
    # Constructor
    def __init__(self):
        self.ticketLines = []
        self.ticketType = "LMX"
        self.numbersLength = 7
        self.numberPool = list(range(1, 50))
        self.ticketLines.append(self.randomLineGenerator())

class LottoSixFortyNine(LottoTicket):
    # Constructor
    def __init__(self):
        self.ticketLines = []
        self.ticketType = "SFN"
        self.numbersLength = 6
        self.numberPool = list(range(1, 49))

class Lottario(LottoTicket):
    # Constructor
    def __init__(self):
        self.ticketLines = []
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
        self.ticketLines = lottoTicket.ticketLines
        self.ticketLines.append(self.randomLineGenerator())
        self.ticketLines.insert(0, self.randomLineGenerator())
        self.encorePlayed = encorePlayed
        self.uniqueIdentifier = self.generateUniqueIdentifier()
        del lottoTicket

    # Ticket Printer
    def printTicket(self):
        print("--- {0} ---".format(self.uniqueIdentifier))
        print("--- Quick Pick Ticket ---")
        self.printTicketLines()

class PickYourOwn(LottoTicket):

    # Constructor
    def __init__(self, firstLine, encorePlayed, lottoTicket):
        self.playType = "P"
        self.ticketType = lottoTicket.ticketType
        self.numberPool = lottoTicket.numberPool
        self.numbersLength = lottoTicket.numbersLength
        self.ticketLines = lottoTicket.ticketLines
        del lottoTicket
        self.ticketLines.append(self.randomLineGenerator())
        self.ticketLines.insert(0, firstLine)
        self.validateInput()
        self.encorePlayed = encorePlayed
        self.uniqueIdentifier = self.generateUniqueIdentifier()

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
        print("--- {0} ---".format(self.uniqueIdentifier))
        print("--- Pick Your Own Ticket ---")
        self.printTicketLines()

# Ticket request sent by the client and read by the server
class TicketRequest:

    def __init__(self, playType = None, ticketType = None, encorePlayed = False, pickedNumbers = []):
        self.playType = playType
        self.ticketType = ticketType
        self.encorePlayed = encorePlayed
        self.pickedNumbers = []

    # Request Serialization
    def serializeRequest(self):
        serializationBuffer = self.ticketType
        serializationBuffer += '_'
        serializationBuffer += self.playType
        serializationBuffer += '_'
        if self.pickedNumbers is not None:
            serializationBuffer += str(len(self.pickedNumbers))
            for number in self.pickedNumbers:
                serializationBuffer += '-'
                serializationBuffer += str(number)
        else:
            serializationBuffer += '0'
        serializationBuffer += '_'
        if self.encorePlayed:
            serializationBuffer += '1'
        else:
            serializationBuffer += '0'
        return serializationBuffer
    
    # Request Deserialization
    def deserializeRequest(self, serializationBuffer):
        bufferAsString = str(serializationBuffer.decode('utf-8'))
        buffer = bufferAsString.split('_')
        self.playType = buffer[0]
        self.ticketType = buffer[1]
        if buffer[2] == 0:
            self.pickedNumbers = None
        else:
            pickedNumbersBuffer = buffer[2].split('-')
            for i in range(1, int(pickedNumbersBuffer[0]) + 1):
                self.pickedNumbers.append(int(pickedNumbersBuffer[i]))
            