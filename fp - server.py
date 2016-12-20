import select
import socket
import sys
import threading
import os

client_waiting = []
client_room = []
client_list = []

class Server:
    def __init__(self):
        self.host = '10.151.43.23'
        self.port = 8008
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)

    def run(self):
        self.open_socket()
        input = [self.server]
        running = 1
        print "aaaa"
        while running:
            inputready, outputready, exceptready = select.select(input, [], [])



            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

        # close all threads

        self.server.close()
        for c in self.threads:
            c.join()


class Client(threading.Thread):
    def __init__(self, (client, address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        if self.address[0] not in client_waiting:
            if self.address[0] not in client_list:
                client_waiting.append(self.address[0])
                client_list.append(self.address[0])
        self.size = 1024
        print "Client List"
        print client_list
        for i in client_waiting:
            print "client waiting"
            print i
        print "panjang waiting"
        print len(client_waiting)
        #print self.address
        if len(client_waiting) % 2 == 0:
            client_room.append([client_waiting[0], client_waiting[1]])
            del client_waiting[:]
            print client_waiting
            for i in client_room:
                print "client room"
                print i
            print "client room pertama"
            print client_room[0][0]

    def run(self):
        running = 1
        while running:
            response_data = ''
            # print 'begin'
            # receive data from client, break when null received
            data = self.client.recv(self.size)
            if data == '1':
                print "sini"
                for i in range(0, len(client_room)):
                    print client_room[i]
                    temp = client_room[i]
                    for i in range (0,2):
                        print temp[i]
                        if self.address[0] == temp[i]:
                            print "adw"
                            self.client.send('1')
                        else:
                            print 'send 0'
                            self.client.send('0')


                if(len(client_room)==0):
                    print 'send 02'
                    self.client.send('0')

            if data == 'ingame':
                print "a"

if __name__ == "__main__":
    s = Server()
    s.run()
