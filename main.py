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
bulletY_change = -7
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
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    janela.blit(score, (x, y))

#Game over message
wasted_font = pygame.font.Font('freesansbold.ttf', 50)

def game_over_text():
    janela.fill((0, 0, 0))
    message = wasted_font.render("GAME OVER", True, (255, 0, 0))
    janela.blit(message, (X/3.5, Y/2.5))
    show_score(X/2.4, Y/2)

#configurando velocidade
clock = pygame.time.Clock()

#Game loop
running = True
while running:

    clock.tick(60)

    janela.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type ==pygame.KEYDOWN: #Checando se alguma tecla foi pressionada
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
    