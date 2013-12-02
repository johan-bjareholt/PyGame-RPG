import os, sys, time
import threading
import logging
import socket
import json

import globals as globs

# ToDo:
# Settings file
# Database
# Protocol
# Game variable holder

# Logging
logFormat = '%(asctime)-15s %(levelname)s %(name)s:%(lineno)s\t  %(message)s'
logFilename = globs.maindir+"/logs/server/"+time.strftime("%Y-%m-%d %Hh %Mm")+".log"
logging.basicConfig(filename=logFilename, filemode='w', level=logging.DEBUG, format=logFormat)
logging.getLogger().addHandler(logging.StreamHandler())



class Main():
    def __init__(self, addr=None, port=None):
        self.running = True

        global server_address
        if not addr and not port:
            server_address = (str(globs.config.get("network", "ip")), int(globs.config.get("network", "port")))
        else:
            server_address = (addr, port)

        self.log = logging.getLogger('main')

    def start(self):
        self.log.debug("Starting sockets")

        tcp.start()
        udp.start()

        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            tcp.close()
            udp.close()
        except Exception as e:
            print(e)

        #tcp.join()
        #udp.join()


        sys.exit()



class Clients(dict):
    def __init__(self):
        self.log = logging.getLogger('clients')
        self.log.setLevel(logging.DEBUG)

    def addClient(self, client):
        self[client.username] = client

    def hashPassword(self, password):
        return password


class Client(threading.Thread):
    def __init__(self, conn, address):
        threading.Thread.__init__(self)
        self.log = logging.getLogger('Client:{}'.format(address))
        self.log.setLevel(logging.DEBUG)

        self.conn = conn
        self.address = address
        self.connected = True
        self.loggedin = False

        self.start()

    def run(self):
        # Listen for TCP connections
        ping = json.dumps({'conn': 'ping'})
        self.sendTcpData(ping)
        while self.connected:
            data = self.conn.recv(2048)
            for command in data.split(';'):
                if data:
                    msghandler.handle(command, self.address)
        self.conn.close()

    def joinGame(self, username, game, playernum):
        self.game = game
        self.username = username
        self.playernum = playernum
        clients[username] = self

    def login(self, password):
        clients.addClient(self)
        self.password = password
        self.loggedin = True
        self.log.info("{} logged in".format(self.username))

    def sendTcpData(self, data):
        message = data+";"
        try:
            self.conn.send(message)
        except Exception as e:
            self.log.error(e, exc_info=True)

        try:
            self.log.debug('TCP: Client:{} - Sent:{}'.format(self.username, message))
        except AttributeError:
            self.log.debug('TCP: Client:{} - Sent:{}'.format(self.address, message))

    def sendUdpData(self, data):
        address = clients[self.username].udp_address
        message = data+";"
        udp.sock.sendto(message, address)
        self.log.debug('UDP: Client:{} - sent:{}'.format(self.username, message))

class TrafficHandler(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.log = logging.getLogger(self.name)
        self.log.setLevel(logging.DEBUG)
        self.daemon = True

    def close(self):
        print("Closing " + self.name)
        self.sock.close()
        print("Done closing "+self.name)


class TcpHandler(TrafficHandler):
    def __init__(self):
        TrafficHandler.__init__(self, 'tcp')

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        # Bind the socket to the port
        self.log.info('Starting up TCP on {}:{}'.format(server_address[0], server_address[1]))
        self.sock.bind(server_address)

        # Listening for new connections
        self.sock.listen(5)
        while main.running:
            # Accepting new connections
            conn, address = self.sock.accept()
            self.log.info('Client {} connected!'.format(address))
            Client(conn, address)

class UdpHandler(TrafficHandler):
    def __init__(self):
        TrafficHandler.__init__(self, 'udp')
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        # Bind the socket to the port
        self.log.info('Starting up UDP on {}:{}'.format(server_address[0], server_address[1]))
        self.sock.bind(server_address)

        while main.running:
            data, address = self.sock.recvfrom(4096)
            self.log.debug(str(data) + ", " + str(address))

            self.log.debug('UDP: Client:{} - Got:{}'.format(address, data))

            message = msghandler.handle(data, address)
            self.log.debug(message)

if __name__ == '__main__':
    #db = Database()
    #clients = Clients()
    #games = Games()
    #msghandler = MessageHandler()

    main = Main()
    tcp = TcpHandler()
    udp = UdpHandler()
    main.start()