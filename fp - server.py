import select
import socket
import sys
import threading
import pygame
import os
import pickle

client_waiting = []
client_room = []
client_list = []
message_temp = {"player1_pos": [40, 325],
                "player2_pos": [1120, 325],
                "ball_pos": [600, 325],
                "score1_val": 0,
                "score2_val": 0,
                "time": 0,
                "win": 0,
                "status": 0,
                "speed": [1, 1]}
messages = []

class Server:
    def __init__(self):
        self.host = '192.168.43.71'
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
           # print client_waiting
           # for i in client_room:
           #     print "client room"
           #     print i
           # print "client room pertama"
            #print client_room[0][0]
            messages.append(message_temp)

    def game(self, room, data):
        pygame.init()

        message_temp = {"player1_pos": [0, 325],
                "player2_pos": [1140, 325],
                "ball_pos": [600, 325],
                "score1_val": 0,
                "score2_val": 0,
                "time": 0,
                "win": 0,
                "status": 0,
                "speed": [1, 1]}

        # ball
        ball = pygame.image.load("assets/bola.png")
        ball = pygame.transform.scale(ball, (30, 30))
        ballrect = ball.get_rect()
        ballrect.move_ip(messages[room]["ball_pos"][0],  messages[room]["ball_pos"][1])

        # Create Player
        player = pygame.image.load("assets/player.png")
        player = pygame.transform.scale(player, (28, 150))
        player_rect = player.get_rect()
        player_rect = player_rect.move( messages[room]["player1_pos"][0],  messages[room]["player1_pos"][1])

        # Create Enemy
        enemy = pygame.image.load("assets/player.png")
        enemy = pygame.transform.scale(enemy, (28, 150))
        enemy_rect = enemy.get_rect()
        enemy_rect = enemy_rect.move( messages[room]["player2_pos"][0],  messages[room]["player2_pos"][1])

        messages[room]["time"] +=1
        if data["status"] == '1':
            messages[room]["player1_pos"][1] += int(data["input_key"][1])
        else:
            messages[room]["player2_pos"][1] += int(data["input_key"][1])

        if (ballrect.left == player_rect.right and (ballrect.bottom >= player_rect.top and ballrect.top <= player_rect.bottom) ) or (ballrect.right == enemy_rect.left and (ballrect.bottom >= enemy_rect.top and ballrect.top <= enemy_rect.bottom)):
                 messages[room]["speed"][0] = -messages[room]["speed"][0]

        if ballrect.top < 0 or ballrect.bottom > 650:
            messages[room]["speed"][1] = -messages[room]["speed"][1]

        if messages[room]["ball_pos"][0] <= -2:
            messages[room]["ball_pos"][0] = 600
            messages[room]["ball_pos"][1] = 325
            ballrect.move_ip(600, 325)
            player_rect.move_ip(0, 325)
            enemy_rect.move_ip(1140, 325)
            messages[room]["player1_pos"][1] = 325
            messages[room]["player2_pos"][1] = 325
            messages[room]["score2_val"] +=1
            if messages[room]["score2_val"] == 2:
                messages[room]["win"] = 2

        if messages[room]["ball_pos"][0] >= 1140:
            messages[room]["ball_pos"][0] = 600
            messages[room]["ball_pos"][1] = 325
            ballrect.move_ip(600, 325)
            player_rect.move_ip(0, 325)
            enemy_rect.move_ip(0, 325)
            messages[room]["player1_pos"][1] = 325
            messages[room]["player2_pos"][1] = 325
            messages[room]["score1_val"] +=1
            if messages[room]["score1_val"] == 2:
                messages[room]["win"] = 1


        messages[room]["ball_pos"][0] += messages[room]["speed"][0]
        messages[room]["ball_pos"][1] += messages[room]["speed"][1]
        send_data = pickle.dumps(messages[room])
        self.client.send(send_data)
        print ballrect

        if messages[room]["win"] != 0:
             return
        #print()
    #yang dikirim ke server posisi player, status game
    #yg diterima dari server posisi musuh, status game



    def run(self):
        flag = 0
        running = 1
        while running:
            response_data = ''
            # print 'begin'
            # receive data from client, break when null received
            data = self.client.recv(self.size)
            if data == '1':
                for i in range(0, len(client_room)):
                    print client_room[i]
                    temp = client_room[i]
                    for y in range (0,2):
                        if self.address[0] == temp[y]:
                            room = i
                            #print "send play"
                            send_command = str(y+1)
                            flag = 1
                            break
                        else:
                            #print 'send 0'
                            send_command = str(0)
                    if flag==1:
                        break

                if(len(client_room)==0):
                    #print 'send 02'
                    send_command = str(0)

                print "command :"
                print send_command
                self.client.send(send_command)

            if 'ingame' in data:
                #print data
                data_arr = pickle.loads(data)
                #print data_arr
                self.game(room, data_arr)

if __name__ == "__main__":
    s = Server()
    s.run()
