import os
import signal


class ConcurrencyManager():

    def __init__(self):
        signal.signal(signal.SIGCHLD, self.childSignalHandler)

    def childSignalHandler(self, signalNumber, frame):
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
                # The print on signal handler is a known bug that causes runtime errors, hence it has been commented out
                # https://bugs.python.org/issue24283
                # print(
                # "Child {0} terminated with status {1}".format(
                # pid, status))
            except OSError:
                return
            if pid == 0:
                return
