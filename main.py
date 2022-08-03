import pygame
import random
import math

#Iniciar o pygame
pygame.init()

#criando a janela
X = 700
Y = 500
janela = pygame.display.set_mode((X, Y))

#Background
background = pygame.image.load("fundoespaco.jpg")
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

#Titulo e icone (Tipo o head do html)
pygame.display.set_caption("Space Invaders - Pedro's version")
icon = pygame.image.load("nave.png")
pygame.display.set_icon(icon)

#Menu inicial
font_basica = pygame.font.Font('freesansbold.ttf', 32)
Start = font_basica.render("Start", True, (0, 0, 0), (255, 255, 255))
Options = font_basica.render("Options", True, (0, 0, 0), (255, 255, 255))
Exit = font_basica.render("Exit", True, (0, 0, 0), (255, 255, 255))

def Menu(x, y):
    global running
    global Game_state
    janela.blit(Start, (X/2 - 37, Y/1.5))
    janela.blit(Options, (X/5 - 64, Y/1.5))
    janela.blit(Exit, (X/1.3 - 32, int(Y/1.5)))
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if y >= Y/1.5 and y <= Y/1.5 + 32:
                if x >= (X/2 - 37) and x <= (X/2 + 37):
                    Game_state = "Game"
                if x >= (X/5 - 64) and x <= (X/5 + 64):
                    Game_state = "Menu"
                if x >= (X/1.3 - 32) and x <= (X/1.3 + 32):
                    running = False
                

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load("002-aircraft.png"))
    enemyX.append(random.randint(0, X - 64))
    enemyY.append(random.randint(0, int(Y/5)))
    enemyX_change.append(3)
    enemyY_change.append(Y/15)

    def enemy(x, y):
        janela.blit(enemyImg[i], (x, y))

#Player
playerImg = pygame.image.load("001-spaceship.png")
playerX = X/2 - 32
playerX_change = 0
playerY = Y - 100

def player(x, y):
    janela.blit(playerImg, (x, y))

#Bullet
bulletImg = pygame.image.load("bullet32.png")
bulletY = playerY
bulletX = 0
bulletY_change = Y/(-60)
bullet_sound = pygame.mixer.Sound('laser.wav')
bullet_state = "ready"
#Ready - No bullet in the screen
#Fire - Bullet moving

def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    janela.blit(bulletImg, (x + 16, y))

#Colisões
def Colisao(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    if distance < 27 and bullet_state == "fire":
        return True
    else:
        return False

explosion_sound = pygame.mixer.Sound("explosion.wav")

#Score
score_value = 0
textX = 10
textY = 10

def show_score(x, y):
    score = font_basica.render("Score : " + str(score_value), True, (255, 255, 255))
    janela.blit(score, (x, y))

#Game over message
over_font = pygame.font.Font('freesansbold.ttf', 50)

def game_over_text():
    global over_condition
    over_condition = True
    janela.fill((0, 0, 0))
    message = over_font.render("GAME OVER", True, (255, 0, 0))
    janela.blit(message, (X/3.5, Y/2.5))
    show_score(X/2.4, Y/2)

#configurando velocidade
clock = pygame.time.Clock()

#Variaveis de estado
Game_state = "Main"
running = True
over_condition = False

#Game loop----------------------------------------------------------------------------------------------------------
while running:

    clock.tick(60)

    mouse = pygame.mouse.get_pos()
    print(mouse)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if Game_state == "Main":
            Menu(mouse[0], mouse[1])

        if Game_state == "Game":

            janela.blit(background, (0, 0))

            for event in pygame.event.get():

                #Checando se alguma tecla foi pressionada
                if event.type ==pygame.KEYDOWN and not over_condition: 
                    #Checando qual tecla foi pressionada
                    if event.key == pygame.K_LEFT:
                        playerX_change -= 5
                    if event.key == pygame.K_RIGHT:
                        playerX_change += 5
                    if event.key == pygame.K_SPACE and bullet_state == "ready":
                        bulletX = playerX
                        bullet_sound.play()
                        fireBullet(bulletX, bulletY)
                

                if event.type == pygame.KEYUP: #Checando se a tecla foi solta (deixou de ser pressionada)
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        playerX_change = 0

            #Colocando limites ao movimento
            if playerX < 0:
                playerX = 0
            elif playerX > X-64:
                playerX = X-64

            playerX += playerX_change
            player(playerX, playerY) #Colocando o player na tela

            #Controlando movimento dos inimigos
            for i in range(num_enemies):
                if enemyX[i] <= 1 or enemyX[i] >= X-64:
                    enemyX_change[i] *= -1
                    enemyY[i] += enemyY_change[i]

                #Game over conditions
                if enemyY[i] > playerY - 64:
                    for j in range(num_enemies):
                        enemyY[j] = Y*2
                    game_over_text()
                    break
    
                enemyX[i] += enemyX_change[i]  
                enemy(enemyX[i], enemyY[i])

                #Efetividade das colisões
                if Colisao(enemyX[i], enemyY[i], bulletX, bulletY):
                    bulletY = playerY
                    bullet_state = "ready"
                    explosion_sound.play()
                    score_value += 1
                    enemyX[i] = random.randint(0, X-64)
                    enemyY[i] = random.randint(0, int(Y/5))
    
            show_score(textX, textY)

            #Movimento das balas
            if bullet_state == "fire":
                fireBullet(bulletX, bulletY)
                bulletY += bulletY_change

            if bulletY <= 0:
                bullet_state = "ready"
                bulletY = playerY

    pygame.display.update() #Atualizando a janela
    