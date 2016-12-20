import sys, pygame, time, msvcrt, socket, pickle



message_in = {"player1_pos" : [0,325],
                "player2_pos" : [1140,325],
                "ball_pos" : [600, 325],
                "score1_val" : 0,
                "score2_val" : 0,
                "time" : 0,
                "win" : 0,
                "status" : 0}

message_out = { "input_key" : [0,0],
                "status" : 0}

pygame.init()
location = [0, 0]
size = width, height = 1200, 650
player_offset = 20
speed = [1, 1]
black = 0, 0, 0
move_tick2log2er = 0

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
YELLOW =   (255,   255,   0)

pygame.font.init()
myfont = pygame.font.Font("assets/HighlandGothicFLF.ttf", 50)
screen = pygame.display.set_mode(size)

ball = pygame.image.load("assets/bola.png")
ball = pygame.transform.scale(ball, (30, 30))

#CreateGoal1
goal1 = pygame.image.load("assets/goal.png")
goal1 = pygame.transform.scale(goal1, (15, 650))
goal1_rect = goal1.get_rect()
goal1_rect = goal1_rect.move(0, 0) #Set PositionGoal1

#CreateGoal1
goal2 = pygame.image.load("assets/goal.png")
goal2 = pygame.transform.scale(goal2, (15, 650))
goal2_rect = goal2.get_rect()
goal2_rect = goal2_rect.move(1180, 0) #Set PositionGoal2

#CreateMidLine
midline = pygame.image.load("assets/midline.png")
midline = pygame.transform.scale(goal2, (15, 650))
midline_rect = midline.get_rect()
midline_rect = midline_rect.move(590, 0) #Set Midline Pos

#Create Player
player = pygame.image.load("assets/player.png")
player = pygame.transform.scale(player, (28, 150))


#Create Enemy
enemy = pygame.image.load("assets/player.png")
enemy = pygame.transform.scale(enemy, (28, 150))

#initial score
score1_val = 0
score2_val = 0
id = ""
char = ""

score1 = myfont.render(str(score1_val), 1, WHITE)
score2 = myfont.render(str(score2_val), 1, WHITE)

seconds = divmod(pygame.time.get_ticks(), 1000)
timeMatch = myfont.render(str(seconds[0]), 1, BLACK)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ballrect = ball.get_rect()


#Create Player
player_rect = player.get_rect()

#posisi player Y diambil posisi di paling atas dari pemain. Min 0, max 50
player_posY = str(player_rect.move(location)).split(',')[1]

#Create Enemy
enemy_rect = enemy.get_rect()

def loading_page():
    thisfont = pygame.font.Font("assets/HighlandGothicFLF.ttf", 50)
    blink = 1
    enter_msg = "Finding Match"
    global s
    s.connect(("192.168.43.71", 8008))

    while 1:
        s.send('1')
        data = s.recv(1024)

        # TIME MATCH
        if (blink >= 0 and blink < 500):
            msg_enter = thisfont.render(enter_msg, 1, WHITE)
        else:
            msg_enter = thisfont.render(enter_msg, 1, BLACK)
        if blink >= 750:
            blink = 0

        if (data == '1' or data =='2'):
            message_out["status"] = data
            break
        else:
            blink = blink + 1


        #EVENT KEY DWN AND UP
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYUP:
                #print "berenti oi "+ str(location[1])
                location[1] = 0

        # DRAW THE ASSETS
        screen.fill(black)
        screen.blit(msg_enter, (width / 2 - 50, 125))
        pygame.display.flip()

    countdown_page()

def countdown_page():
    thisfont = pygame.font.Font("assets/HighlandGothicFLF.ttf", 100)
    blink = 1
    number_loading = 3

    while 1:
        #TIME MATCH
        if(blink>=0 and blink <500):
            msg_enter = thisfont.render(str(number_loading), 1, WHITE)
        else:
            msg_enter = thisfont.render(str(number_loading), 1, BLACK)
        if blink>=750:
            blink = 0
            number_loading -= 1

        if(number_loading<=0):
            break
        else:
            blink = blink + 1


        #EVENT KEY DWN AND UP
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYUP:
                #print "berenti oi "+ str(location[1])
                location[1] = 0

        #DRAW THE ASSETS
        screen.fill(black)
        screen.blit(msg_enter, (width / 2-50, 125))
        pygame.display.flip()
    message = {"key" : "ingame"}
    message.update({"status": message_out["status"]})
    message.update({"input_key": location})
    message = pickle.dumps(message)
    s.send(message)
    game()




def win_page(win):

    global score1_val, score2_val

    score1_val = 0
    score2_val = 0

    if win==0:
        msg="You Lose The Game"
    else:
        msg="You Win The Game"


    blink = 1
    enter_msg = "Hit Space to Continue"

    while 1:
        #TIME MATCH
        msg_win = myfont.render(msg, 1, WHITE)
        if(blink>=100 and blink <200):
            msg_enter = myfont.render(enter_msg, 1, WHITE)
        else:
            msg_enter = myfont.render(enter_msg, 1, BLACK)
        if blink>=200:
            blink = 0

        blink = blink+1

        #EVENT KEY DWN AND UP
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYUP:
                #print "berenti oi "+ str(location[1])
                location[1] = 0


        #EVENT KEY PRESSED BUFFERED
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            main()

        #DRAW THE ASSETS
        screen.fill(black)
        screen.blit(msg_win, (width / 2 - 150, 125))
        screen.blit(msg_enter, (width / 2 - 200, 400))
        pygame.display.flip()

#
# def screenblit_game():


def game():
    global s
    global player_posY, player_rect, enemy_rect
    global ballrect, ball_posX,ball_posY
    global score1_val,score2_val
    global score1, score2, seconds, timeMatch

    time = 0;

    while 1:
        datarecv = s.recv(1024)
        datarecv = pickle.loads(datarecv)
        print datarecv

        temp = ballrect.move(0,0)
        ball_posX = datarecv["ball_pos"][0]-temp[0]
        ball_posY = datarecv["ball_pos"][1]-temp[1]

        temp_player = player_rect.move(0,0)
        player_posX = datarecv["player1_pos"][0] - temp_player[0]
        player_posY = datarecv["player1_pos"][1] - temp_player[1]


        temp_enemy = enemy_rect.move(0,0)
        enemy_PosX = datarecv["player2_pos"][0] - temp_enemy[0]
        enemy_PosY = datarecv["player2_pos"][1] - temp_enemy[1]

        ballrect.move_ip(ball_posX,ball_posY)
        player_rect = player_rect.move(player_posX, player_posY)
        enemy_rect = enemy_rect.move(enemy_PosX, enemy_PosY)


        message = {"key" : "ingame"}
        time=datarecv["time"]
        seconds = time/200;
        #print time
        player_posY = str(player_rect.move(location)).split(',')[1]
        player_posY = int(player_posY)
        ball_posX = str(ballrect.move(speed)).split(',')[0]
        ball_posY = str(ballrect.move(location)).split(',')[1]
        ball_posX = str(ball_posX).split('(')[1]
        ball_posX = int(ball_posX)
        #print ball_posX, ball_posY

        #TIME MATCH
        timeMatch = myfont.render(str(seconds), 1, BLACK)


        if(datarecv["win"]!=0):
            if(str(datarecv["win"])==str(message_out["status"])):
                win = 1
            else:
                win = 0
            win_page(win)



        score1 = myfont.render(str(datarecv["score1_val"]), 1, WHITE)
        score2 = myfont.render(str(datarecv["score2_val"]), 1, WHITE)

        #EVENT KEY DWN AND UP
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYUP:
                #print "berenti oi "+ str(location[1])
                location[1] = 0

        #EVENT KEY PRESSED BUFFERED
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            location[1] = 3
        if keys[pygame.K_UP]:
            location[1] = -3

        message.update({"input_key" : location})
        message.update({"status": message_out["status"]})
        #ANIMATION
        player_rect = player_rect.move(location)
        ballrect = ballrect.move(datarecv["speed"][0], datarecv["speed"][0])

        #COLLISION
        #   colide player
        if (ballrect.left == player_rect.right and (ballrect.bottom >= player_rect.top and ballrect.top <= player_rect.bottom) )or  ballrect.colliderect(enemy_rect):
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]

        #DRAW THE ASSETS
        screen.fill(black)

        screen.blit(goal1, goal1_rect)
        screen.blit(goal2, goal2_rect)
        screen.blit(midline, midline_rect)

        screen.blit(score1, (width / 2 - 200, 125))
        screen.blit(score2, (width / 2 + 150, 125))

        pygame.draw.rect(screen, YELLOW, [475, 25, 250, 75])
        screen.blit(timeMatch, (width / 2 - 25, 25))

        screen.blit(ball, ballrect)
        screen.blit(player, player_rect)
        screen.blit(enemy, enemy_rect)

        print(message)
        dataPickle = pickle.dumps(message)
        pygame.display.flip()
        s.send(dataPickle)
#yang dikirim ke server posisi player, status game
#yg diterima dari server posisi musuh, status game


def main():
    blink = 1
    enter_msg = "Hit Space to Start"
    while 1:
        #TIME MATCH
        msg_welcome = myfont.render("PONG GAME", 1, WHITE)
        if(blink>=100 and blink <200):
            msg_enter = myfont.render(enter_msg, 1, WHITE)
        else:
            msg_enter = myfont.render(enter_msg, 1, BLACK)
        if blink>=200:
            blink = 0

        blink = blink+1

        #EVENT KEY DWN AND UP
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYUP:
                #print "berenti oi "+ str(location[1])
                location[1] = 0


        #EVENT KEY PRESSED BUFFERED
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            loading_page()

        #DRAW THE ASSETS
        screen.fill(black)
        screen.blit(msg_welcome, (width / 2 - 150, 125))
        screen.blit(msg_enter, (width / 2 - 200, 400))
        pygame.display.flip()

if __name__=='__main__':
    main()
