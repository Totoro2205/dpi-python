import sys, os, time, atexit
from signal import SIGTERM 
from loggingManager import LoggingManager

class Daemon():

    forkFailedMessage = " failed, unable to create child process. \n Exception: "

    # Writed to the default location /var/run
    def __init__(self, semaphore="/var/run/ticketer.pid"):
        sys.stdin = open(os.devnull, 'w')
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        self.semaphore = semaphore
        self.logger = LoggingManager("DAEMON")

    # Writes semaphore file to the directory
    def writeSemaphore(self):
        atexit.register(self.deleteSemaphore)
        pid = str(os.getpid())

        file = open(self.semaphore,'w')
        file.write("{0}\n".format(pid))
        self.logger.logInfo("Semaphore Created with PID: {0}".format(pid))

    # Deletes semaphore file from the directory
    def deleteSemaphore(self):
        os.remove(self.semaphore)

    # Daemonizes the process by double-forking and writing the semaphore
    def daemonizeProcess(self):
        try:
            pid = os.fork()
            if pid > 0:
                self.logger.logInfo("Fork 1 Exitting Parent")
                sys.exit(0)
        except OSError as ex:
            self.logger.logError("Fork 1 {0} {1}".format(self.forkFailedMessage, ex))
            sys.exit(1)

        uid = os.getuid()
        os.chdir("/")
        os.setuid(uid)
        gid = os.getgid() 
        os.setgid(gid)
        os.setsid()

        try:
            pid = os.fork()
            if pid > 0:
                self.logger.logInfo("Fork 2 Exitting Parent")
                sys.exit(0)
        except OSError as ex:
            self.logger.logError("Fork 2 {0} {1}".format(self.forkFailedMessage, ex))
            sys.exit(1)

        self.writeSemaphore()
        self.logger.logInfo("Daemonized, process starting...")

    # Starts up the daemon
    def startDaemon(self):
        pid = None
        try:
            semaphoreFile = open(self.semaphore,'r')
            pid = int(semaphoreFile.read().strip())
            semaphoreFile.close()
        except IOError as ex:
            self.logger.logError("Error starting the daemon: {0}".format(ex))

        if pid:
            self.logger.logError("Daemon with PID {0} already running, start aborted".format(pid))
            sys.exit(1)
        
        # Start the daemon
        self.daemonizeProcess()

    # Stops the daemon and performs a cleanup of all setup
    def stopDaemon(self):
        try:
            semaphoreFile = open(self.semaphore,'r')
            pid = int(semaphoreFile.read().strip())
            semaphoreFile.close()
        except IOError:
            self.logger.logError("Error reading the daemon file")

        if not pid:
            self.logger.logError("Daemon was not running, cannot stop")
            return

        try:
            while 1:
                os.kill(pid, SIGTERM)
            os.remove(self.semaphore)
        except OSError as ex:
            err = str(ex)
            if err.find("No such process") > 0:
                if os.path.exists(self.semaphore):
                    os.remove(self.semaphore)
            else:
                self.logger.logError(ex)
                sys.exit(1)