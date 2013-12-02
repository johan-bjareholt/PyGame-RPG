import sys, os, time
import logging
import threading
import socket

import globals as globs

maindir = os.path.dirname(os.getcwd())
# Logging
logFormat = '%(asctime)-15s %(levelname)s %(name)s:%(lineno)s\t  %(message)s'
logFilename = maindir+"/logs/client/"+time.strftime("%Y-%m-%d %Hh %Mm")+".log"
logging.basicConfig(filename=logFilename, filemode='w', level=logging.DEBUG, format=logFormat)
logging.getLogger().addHandler(logging.StreamHandler())

netlog = logging.getLogger('netlog')



class ClientConn(threading.Thread):
    def __init__(self, addr='127.0.0.1', port=2500):
        threading.Thread.__init__(self)
        globs.address = (addr, port)
        self.daemon = True

        self.tcp = TcpHandler()
        self.udp = UdpHandler()

    def run(self):
        try:
            self.udp.start()
            self.tcp.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.udp.sock.close()
            self.tcp.sock.close()
        except Exception as e:
            print(e)

        #self.tcp.join()
        #self.udp.join()

        sys.exit()


class NetworkHandler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.load()

    def load(self):
        pass

    def close(self):
        self.sock.close()
        print("Closed " + self.protocol + " socket")

    def listen(self):
        pass

    def handle(self, data):
        try:
            if data:
                print(data)
        except Exception as e:
            netlog.error("Could not parse: {} \nError: {}".format(data, e), exc_info=True)

    def parse(self, data):
        pass
        # TCP
        #if self.__name__ == "TcpHandler":
        #    pass
        # TCP
        #elif self.__name__ == "UdpHandler":
        #    pass


class TcpHandler(NetworkHandler):
    def load(self):
        self.protocol = "TCP"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen(self):
        return self.sock.recv(2048)

    def run(self):
        netlog.info("Starting tcp socket!")
        self.sock.connect(globs.address)

        # Lobby and game section
        while self.running:
            # Recv action
            data = self.listen()
            if data:
                for message in data.split(';'):
                    netlog.debug("TCP:Got: " + message)
                    response = self.handle(message)
                    if response:
                        self.sendData(response)

        self.socket.close()

    def sendData(self, data):
        self.sock.send(data)
        netlog.debug(self.protocol+":Sent: " + data)


class UdpHandler(NetworkHandler):
    def load(self):
        self.protocol = "UDP"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def listen(self):
        return self.sock.recvfrom(2048)

    def run(self):
        netlog.info("Starting udp socket!")
        while self.running:
            data, addr = self.listen()
            if data:
                for message in data.split(';'):
                    netlog.debug(self.protocol+":Got: " + message)
                    response = net.msghandler.handle(message)
                    if response:
                        self.sendData(response)

    def sendData(self, data):
        self.sock.sendto(data, globs.address)
        netlog.debug(self.protocol+":Sent: " + data)


if __name__ == '__main__':
    networking = ClientConn()
    networking.start()