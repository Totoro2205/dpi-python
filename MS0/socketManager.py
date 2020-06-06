import socket
import sys
import signal
import os

class SocketManager:
    localSocket: socket
    connection: socket


class ServerSocketManager(SocketManager):
    host = '::1'

    # Constructor binds the socket and listens for connections
    def __init__(self, port):

        for response in socket.getaddrinfo(
                self.host,
                port,
                0,
                socket.SOCK_STREAM,
                0,
                socket.AI_PASSIVE):
            socktype, serverAddress = response

            try:
                self.localSocket = socket.socket(socket.AF_INET, socktype, 0)
            except socket.error as msg:
                self.localSocket = None
                print(msg)
                continue
            try:
                self.localSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.localSocket.bind(serverAddress)
                self.localSocket.listen(1)
                print('Listening for Connections on Port: {0}'.format(port))
            except socket.error as msg:
                self.localSocket.close()
                self.localSocket = None
                print(msg)
                continue
            break
        if self.localSocket is None:
            print('Could not open socket')
            sys.exit(1)

    def acceptConnections(self):
        connection, address = self.localSocket.accept()
        print('Received connetion from: {0}'.format(address))
        self.connection = connection
        self.addr = address

    # Sends data to client, if failed it sends an error message to STDOUT
    def sendData(self, data):
        try:
            self.connection.sendall(data)
        except Exception as ex:
            self.sendErrorAndCloseConnection(ex)
        return 0

    # Sends error data and closes the connection
    def sendErrorAndCloseConnection(self, error):
        print("ERROR: {0}, Connection Closed".format(error))
        self.closeConnection()

    # Close Connection
    def closeConnection(self):
        print("Closing Connection")
        self.localSocket.close()
        self.connection.close()

    # Handles data receiving
    def receiveData(self):
        data = self.connection.recv(2048)
        if not data:
            raise Exception("No data received")
        #print("Data Received: {0}".format(data))
        return data

    # Child Process Signal Manager
    def signalManager(self):
        pid, status = os.wait()
        print("Child {0} terminated with status {1}".format(pid, status))

    # Child Process Manager
    def childManager(self):
        signal.signal(signal.SIGCHLD, self.signalManager)

    # Daemon Manager
    def startDaemon(self):
        try:
            pid = os.fork()
        except OSError:
            raise OSError("Fork failed, unable to create child process")
        
        if pid == 0:
            self.localSocket.close()
            data = self.receiveData()
            self.stopChildProcess()
        else:
            self.localSocket.close()

    def stopChildProcess(self):
        self.connection.close()
        os._exit(0)


class ClientSocketManager(SocketManager):

    # Constructor binds the socket and listens for connections
    def __init__(self, host, port):
        for response in socket.getaddrinfo(
                host,
                port,
                0,
                socket.SOCK_STREAM):
            af, socktype, serverAddress = response
            try:
                self.localSocket = socket.socket(af, socktype)
            except socket.error as msg:
                self.localSocket = None
                print(msg)
                continue
            try:
                self.localSocket.connect(serverAddress)
            except socket.error as msg:
                self.localSocket.close()
                self.localSockets = None
                print(msg)
                continue
            break
        if self.localSocket is None:
            print('Could not open socket')
            sys.exit(1)

    # Sends data to server, if failed it sends an error message to STDOUT
    def sendData(self, data):
        try:
            self.localSocket.sendall(data.encode('utf-8'))
        except Exception as ex:
            self.sendErrorAndCloseConnection(ex)
        return 0

    # Sends error data and closes the connection
    def sendErrorAndCloseConnection(self, error):
        print("ERROR: {0}, Connection Closed".format(error))
        self.closeConnection()

    # Close Connection
    def closeConnection(self):
        self.localSocket.close()

    # Handles data receiving
    def receiveData(self):
        data = self.localSocket.recv(2048)
        if not data:
            raise Exception("No data received")
        return data
