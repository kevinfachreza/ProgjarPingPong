import sys, pygame
pygame.init()
location = [0, 0]
size = width, height = 1200, 650
speed = [1, 1]
black = 0, 0, 0
move_ticker = 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("assets/ball.png")
ballrect = ball.get_rect()
ballrect.move_ip(400, 350)

player = pygame.image.load("assets/player.png")
player = pygame.transform.scale(player, (28, 150))
player_rect = player.get_rect()

enemy = pygame.image.load("assets/enemy.png")
enemy_rect = enemy.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                location[1] = 1
            if event.key == pygame.K_UP:
                location[1] = -1
        if event.type == pygame.KEYUP:
            print "berenti oi "+ str(location[1])
            location[1] = 0

    player_rect = player_rect.move(location)
    ballrect = ballrect.move(speed)

    if ballrect.colliderect(player_rect) or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    screen.blit(player, player_rect)
    pygame.display.flip()

#yang dikirim ke server posisi player, status game
#yg diterima dari server posisi musuh, status game
