import socket
import sys


class SocketManager:
    localSocket: socket
    connection: socket


class ServerSocketManager(SocketManager):
    host = '::1'

    # Constructor binds the socket and listens for connections
    def __init__(self, port):

        for res in socket.getaddrinfo(
                self.host,
                port,
                0,
                socket.SOCK_STREAM,
                0,
                socket.AI_PASSIVE):
            af, socktype, proto, canonname, sa = res

            try:
                self.localSocket = socket.socket(af, socktype, 0)
            except socket.error as msg:
                self.localSocket = None
                print(msg)
                continue
            try:
                self.localSocket.bind(sa)
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
        conn, addr = self.localSocket.accept()
        print('Received connetion from: {0}'.format(addr))
        self.connection = conn

    # Sends data to client, if failed it sends an error message to STDOUT
    def sendData(self, data):
        try:
            self.connection.sendall(data.encode('utf-8'))
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
        self.connection.close()

    # Handles data receiving
    def receiveData(self):
        data = self.connection.recv(2048)
        if not data:
            raise Exception("No data received")
        #print("Data Received: {0}".format(data))
        return data


class ClientSocketManager(SocketManager):

    # Constructor binds the socket and listens for connections
    def __init__(self, host, port):
        for res in socket.getaddrinfo(
                host,
                port,
                socket.AF_UNSPEC,
                socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.localSocket = socket.socket(af, socktype, proto)
            except socket.error as msg:
                self.localSocket = None
                print(msg)
                continue
            try:
                self.localSocket.connect(sa)
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
