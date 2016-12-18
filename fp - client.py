import sys, pygame, time
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

ball = pygame.image.load("assets/ball.png")
ballrect = ball.get_rect()
ballrect.move_ip(400, 350)

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
player_rect = player.get_rect()
player_rect = player_rect.move(player_offset,0)

#posisi player Y diambil posisi di paling atas dari pemain. Min 0, max 50
player_posY = str(player_rect.move(location)).split(',')[1]

#Create Enemy
enemy = pygame.image.load("assets/player.png")
enemy = pygame.transform.scale(enemy, (28, 150))
enemy_rect = enemy.get_rect()
enemy_rect = enemy_rect.move(width-(3*player_offset),0)




while 1:
    player_posY = str(player_rect.move(location)).split(',')[1]
    player_posY = int(player_posY)

    #TIME MATCH
    seconds = divmod(pygame.time.get_ticks(),1000)
    timeMatch = myfont.render(str(seconds[0]), 1, BLACK)

    #SCORE
    score1_val = 1
    score2_val = 2
    score1 = myfont.render(str(score1_val), 1, WHITE)
    score2 = myfont.render(str(score2_val), 1, WHITE)

    #EVENT KEY DWN AND UP
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                print player_posY
            if event.key == pygame.K_UP:
                print player_posY
        if event.type == pygame.KEYUP:
            #print "berenti oi "+ str(location[1])
            location[1] = 0


    #EVENT KEY PRESSED BUFFERED
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        print player_posY
        if player_posY <= 500 :
            location[1] = 1
        else:
            location[1] = 0
    if keys[pygame.K_UP]:
        print player_posY
        if player_posY >= 0:
            location[1] = -1
        else:
            location[1] = 0

    #ANIMATION
    player_rect = player_rect.move(location)
    ballrect = ballrect.move(speed)

    #COLLISION
    if ballrect.colliderect(player_rect) or  ballrect.colliderect(enemy_rect) or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    #DRAW THE ASSETS
    screen.fill(black)


    screen.blit(goal1, goal1_rect)
    screen.blit(goal2, goal2_rect)
    screen.blit(midline, midline_rect)

    screen.blit(score1, (width/2-200, 125))
    screen.blit(score2, (width/2+150, 125))



    pygame.draw.rect(screen, YELLOW, [475, 25, 250, 75])
    screen.blit(timeMatch, (width/2-25, 25))


    screen.blit(ball, ballrect)
    screen.blit(player, player_rect)
    screen.blit(enemy, enemy_rect)
    pygame.display.flip()
#yang dikirim ke server posisi player, status game
#yg diterima dari server posisi musuh, status game
