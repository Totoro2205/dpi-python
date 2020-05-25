from datetime import date
import random

class LottoTicket:

    numberPool = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 
    43, 44, 45, 46, 47, 48, 49, 50]

    firstLine = []
    encorePlayed = False

    #Random Number Generator for Lotto tickets
    def randomGenerator(self):
        returnList = []
        while len(returnList) < 7:
            number = random.choice(self.numberPool)
            if(number not in returnList):
                 returnList.append(number)
        return returnList

    #Ticket Lines Printer
    def printTicketLines(self):
        print(*self.firstLine, sep="  ")
        print("-------------------------")
        print(*self.secondLine, sep="  ")
        print(*self.thirdLine, sep="  ")
        if(self.encorePlayed):
            print("--- Encore Played ---")
        else:
            print("--- Encore Not Played ---")

    #Constructor
    def __init__(self):
        self.date = date.today()
        self.secondLine = self.randomGenerator()
        self.thirdLine = self.randomGenerator()

class QuickPick(LottoTicket):

    #Constructor
    def __init__(self, encorePlayed):
        LottoTicket.__init__(self)
        self.firstLine = self.randomGenerator()
        self.encorePlayed = encorePlayed

    #Ticket Printer
    def printTicket(self):
        print(self.date)
        print("--- Quick Pick Ticket ---")
        self.printTicketLines()

class PickYourOwn(LottoTicket):

    #Constructor
    def __init__(self, firstLine, encorePlayed):
        LottoTicket.__init__(self)
        self.firstLine = firstLine
        self.validateInput()
        self.encorePlayed = encorePlayed

    #Validates User's Input against duplicates or numbers out of the pool
    def validateInput(self):
        for number in self.firstLine:
            if(number not in self.numberPool):
                raise ValueError("Invalid value inserted: {0}, please selected a number between 1 & 50".format(number))
            if(self.firstLine.count(number) > 1):
                raise ValueError("Duplicate value inserted: {0}, please insert only unique numbers between 1 & 50".format(number))

    #Ticket Printer
    def printTicket(self):
        print(self.date)
        print("--- Pick Your Own Ticket ---")
        self.printTicketLines()