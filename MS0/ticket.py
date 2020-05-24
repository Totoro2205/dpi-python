from datetime import date
import random

class LottoTicket:

    numberPool = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 
    43, 44, 45, 46, 47, 48, 49, 50]

    #Random Number Generator for Lotto tickets
    def randomGenerator(self):
        returnList = []
        while len(returnList) < 7:
            number = random.choice(self.numberPool)
            if(number not in returnList):
                 returnList.append(random.choice(self.numberPool))
        return returnList

    #Ticket Printer
    def printTicket(self):
        print(self.date)
        print()
        print(self.firstLine)
        print(self.secondLine)
        print(self.thirdLine)

    #Constructor
    def __init__(self, firstLine, isQuickPick):
        self.date = date.today()
        if isQuickPick:
            self.firstLine = self.randomGenerator()
        else:
            self.firstLine = firstLine
        self.secondLine = self.randomGenerator()
        self.thirdLine = self.randomGenerator()