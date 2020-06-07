import socket
import sys
import signal
import os

class SocketManager:
    listenerSocket: socket
    connection: socket


class ServerSocketManager(SocketManager):
    host = '::1'

    # Constructor binds the socket and listens for connections
    def __init__(self, port, queueSize):

        for response in socket.getaddrinfo(
                self.host,
                port,
                0,
                socket.SOCK_STREAM,
                0,
                socket.AI_PASSIVE):
            addressFamily, socktype, proto, canonname, sa = response

            try:
                self.listenerSocket = socket.socket(addressFamily, socktype, proto)
            except socket.error as msg:
                self.listenerSocket = None
                print(msg)
                continue
            try:
                self.listenerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.listenerSocket.bind(sa)
                self.listenerSocket.listen(queueSize)
                print('Listening for Connections on Port: {0}'.format(port))
            except socket.error as msg:
                self.listenerSocket.close()
                self.listenerSocket = None
                print(msg)
                continue
            break
        if self.listenerSocket is None:
            print('Could not open socket')
            sys.exit(1)

    def acceptConnections(self):
        connection, address = self.listenerSocket.accept()
        print('Received connetion from: {0}'.format(address))
        self.connection = connection
        self.addr = address

    # Sends data to client, if failed it sends an error message to STDOUT
    def sendData(self, data):
        #try:
        self.connection.sendall(data.encode('utf-8'))
        #except Exception as ex:
            #self.sendErrorAndCloseConnection(ex)
        return 0

    # Sends error data and closes the connection
    def sendErrorAndCloseConnection(self, error):
        print("ERROR: {0}, Connection Closed".format(error))
        self.listenerSocket.sendall("ERROR: {0}, Connection Closed".format(error).encode('utf-8'))
        self.closeConnection()

    # Close Connection
    def closeConnection(self):
        print("Closing Connection")
        self.listenerSocket.close()
        self.connection.close()

    # Handles data receiving
    def receiveData(self):
        data = self.connection.recv(2048)
        if not data:
            raise Exception("No data received")
        print("Data Received: {0}".format(data))
        return data

    # Daemon Manager
    def startDaemon(self, daemonHandler):
        try:
            pid = os.fork()
        except OSError:
            raise OSError("Fork failed, unable to create child process")
        data = ''
        if pid == 0:
            data = self.receiveData()
            daemonHandler(data, self)
            self.stopChildProcess()
        else:
            self.connection.close()

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
            af, socktype, proto, canonname, serverAddress = response
            try:
                self.listenerSocket = socket.socket(af, socktype)
            except socket.error as msg:
                self.listenerSocket = None
                print(msg)
                continue
            try:
                self.listenerSocket.connect(serverAddress)
            except socket.error as msg:
                self.listenerSocket.close()
                self.listenerSockets = None
                print(msg)
                continue
            break
        if self.listenerSocket is None:
            print('Could not open socket')
            sys.exit(1)

    # Sends data to server, if failed it sends an error message to STDOUT
    def sendData(self, data):
        try:
            self.listenerSocket.sendall(data.encode('utf-8'))
        except Exception as ex:
            self.sendErrorAndCloseConnection(ex)
        return 0

    # Sends error data and closes the connection
    def sendErrorAndCloseConnection(self, error):
        print("ERROR: {0}, Connection Closed".format(error))
        self.closeConnection()

    # Close Connection
    def closeConnection(self):
        self.listenerSocket.close()

    # Handles data receiving
    def receiveData(self):
        data = self.listenerSocket.recv(2048)
        if not data:
            raise Exception("No data received")
        return data