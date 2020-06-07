import os

class ConcurrencyManager():

    def __init__(self):
        self.pid = 0

    def childSignalHandler(self, signalNumber, frame):
        while True:
            try:
                self.pid, status = os.waitpid(-1, os.WNOHANG)
                print("Child {0} terminated with status {1}".format(self.pid, status))
            except OSError:
                return
            if self.pid == 0:
                return