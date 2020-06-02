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

    def __init__(self):
        self.ticketLines = []

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
        return self.ticketType + self.playType + "." + \
            self.date.strftime("%m%d%Y") + "." + str(random.randint(100000, 999999))

    def writeTicketToFile(self):
        file = open("lottoTickets.txt", "a")
        file.write("--- {0} --- \n".format(self.uniqueIdentifier))
        if self.playType == 'Q':
            file.write("--- Quick Pick Ticket ---\n")
        elif self.playType == 'P':
            file.write("--- Pick Your Own Ticket ---\n")
        for line in self.ticketLines:
            if(self.ticketLines.index(line) == 1):
                file.write("-------------------------\n")
            for lineNumber in line:
                file.write(lineNumber)
                file.write(' ')
                if lineNumber == line[-1]:
                    file.write('\n')
        if(self.encorePlayed):
            file.write("--- Encore Played ---\n")
        else:
            file.write("--- Encore Not Played ---\n\n")
        file.write("\n")
        file.close()

    # Ticket Lines Printer
    def printAndSaveTicket(self):
        print("--- {0} ---".format(self.uniqueIdentifier))
        if self.playType == 'Q':
            print("--- Quick Pick Ticket ---")
        elif self.playType == 'P':
            print("--- Pick Your Own Ticket ---")
        for line in self.ticketLines:
            if(self.ticketLines.index(line) == 1):
                print("-------------------------")
            print(*line, sep="  ")
        if(self.encorePlayed):
            print("--- Encore Played ---")
        else:
            print("--- Encore Not Played ---")
        print("")
        self.writeTicketToFile()

    # Ticket Serialization
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

    # Ticket Deserialization
    def deserializeTicket(self, serializationBuffer):
        try:
            bufferAsString = str(serializationBuffer.decode('utf-8'))
        except BaseException:
            bufferAsString = serializationBuffer

        buffer = bufferAsString.split('_')
        self.uniqueIdentifier = buffer[0]
        self.ticketType = buffer[1]
        self.playType = buffer[2]
        ticketLineBuffer = buffer[3].split(':')
        self.ticketLines = []
        for line in ticketLineBuffer:
            self.ticketLines.append(line.split('-'))
        if buffer[4] == '1':
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

# Ticket request sent by the client and read by the server


class TicketRequest:

    def __init__(
            self,
            playType=None,
            ticketType=None,
            encorePlayed=False,
            pickedNumbers=[],
            ticketAmount=1):
        self.playType = playType
        self.ticketType = ticketType
        self.encorePlayed = encorePlayed
        self.pickedNumbers = []
        self.ticketAmount = ticketAmount

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
        serializationBuffer += '_'
        serializationBuffer += str(self.ticketAmount)
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
        if buffer[3] == '1':
            self.encorePlayed = True
        else:
            self.encorePlayed = False
        self.ticketAmount = int(buffer[4])

    # Processes request and returns the ticket based on ticket rules
    def getTickets(self):
        tickets = []
        for amount in range(0, self.ticketAmount):
            if(self.pickedNumbers):
                totalNumbers = len(self.pickedNumbers)
            else:
                totalNumbers = -1

            if(self.playType == "SFN"):
                if(totalNumbers != 6 and totalNumbers != -1):
                    raise ValueError(
                        "You picked {0} numbers. Please pick six numbers for your Lotto 649 Ticket".format(totalNumbers))
                baseTicket = LottoSixFortyNine()

            elif(self.playType == "LTR"):
                if(totalNumbers != 6 and totalNumbers != -1):
                    raise ValueError(
                        "You picked {0} numbers. Please pick six numbers for your Lottario Ticket".format(totalNumbers))
                baseTicket = Lottario()

            elif(self.playType == "LMX"):
                if(totalNumbers != 7 and totalNumbers != -1):
                    raise ValueError(
                        "You picked {0} numbers. Please pick seven numbers for your LottoMax Ticket".format(totalNumbers))
                baseTicket = LottoMax()

            if(self.ticketType == "Q"):
                if(self.encorePlayed):
                    ticket = QuickPick(True, baseTicket)
                else:
                    ticket = QuickPick(False, baseTicket)
            elif(self.ticketType == "P"):
                if(self.encorePlayed):
                    ticket = PickYourOwn(self.pickedNumbers, True, baseTicket)
                else:
                    ticket = PickYourOwn(self.pickedNumbers, False, baseTicket)
            elif(self.encorePlayed):
                raise AttributeError(
                    "The encore argument must be used with a Quick Pick or a Pick Your Own ticket")
            else:
                raise AttributeError(
                    "None or invalid arguments given, ticket not generated! Please pick a ticket mode, either Quick Pick or Pick Your Own Ticket. Use the -h switch if required.")
            tickets.append(ticket)
        return tickets
