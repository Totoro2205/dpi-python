from datetime import date
import random


class LottoTicket:
    numberPool = []
    lines = []
    encorePlayed = False
    numbersLength = 0
    date = date.today()

    # Random Number Generator for Lotto tickets
    def randomGenerator(self):
        returnList = []
        while len(returnList) < self.numbersLength:
            number = random.choice(self.numberPool)
            if(number not in returnList):
                returnList.append(number)
        return returnList

    # Ticket Lines Printer
    def printTicketLines(self):
        for line in self.lines:
            if(self.lines.index(line) == 1):
                print("-------------------------")
            print(*line, sep="  ")
        if(self.encorePlayed):
            print("--- Encore Played ---")
        else:
            print("--- Encore Not Played ---")

# Ticket Types


class LottoMax(LottoTicket):
    # Constructor
    def __init__(self):
        self.numbersLength = 7
        self.numberPool = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50]
        self.lines.append(self.randomGenerator())


class LottoSixFortyNine(LottoTicket):
    # Constructor
    def __init__(self):
        self.numbersLength = 6
        self.numberPool = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49]


class Lottario(LottoTicket):
    # Constructor
    def __init__(self):
        self.numbersLength = 6
        self.numberPool = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45]

# Game Types


class QuickPick(LottoTicket):

    # Constructor
    def __init__(self, encorePlayed, lottoTicket):
        self.numberPool = lottoTicket.numberPool
        self.numbersLength = lottoTicket.numbersLength
        self.lines.append(self.randomGenerator())
        self.lines.insert(0, self.randomGenerator())
        self.encorePlayed = encorePlayed

    # Ticket Printer
    def printTicket(self):
        print(self.date)
        print("--- Quick Pick Ticket ---")
        self.printTicketLines()


class PickYourOwn(LottoTicket):

    # Constructor
    def __init__(self, firstLine, encorePlayed, lottoTicket):
        self.numberPool = lottoTicket.numberPool
        self.numbersLength = lottoTicket.numbersLength
        self.lines.append(self.randomGenerator())
        self.lines.insert(0, firstLine)
        self.validateInput()
        self.encorePlayed = encorePlayed

    # Validates User's Input against duplicates or numbers out of the pool
    def validateInput(self):
        for number in self.lines[0]:
            if(number not in self.numberPool):
                raise ValueError(
                    "Invalid value inserted: {0}, please selected a number between 1 & {1}".format(
                        number, max(
                            self.numberPool)))
            if(self.lines[0].count(number) > 1):
                raise ValueError(
                    "Duplicate value inserted: {0}, please insert only unique numbers between 1 & {1}".format(
                        number, max(
                            self.numberPool)))

    # Ticket Printer
    def printTicket(self):
        print(self.date)
        print("--- Pick Your Own Ticket ---")
        self.printTicketLines()
