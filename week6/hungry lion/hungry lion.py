import pygame
import random
import sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
EnemyMINSIZE = 10
EnemyMAXSIZE = 40
EnemyMINSPEED = 1
EnemyMAXSPEED = 8
ADDNEWEnemyRATE = 6
PLAYERMOVERATE = 5

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def playerHasHitEnemy(playerRect, enemies):
    for b in enemies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Hungry lion')
pygame.mouse.set_visible(False)

# font
font = pygame.font.SysFont('arial', 48)

# sounds
gameOverSound = pygame.mixer.Sound('over.wav')
pygame.mixer.music.load('background og.mid')

# img
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
EnemyImage = pygame.image.load('Enemy.png')

# menu
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Hungry Lion', font, windowSurface, (WINDOWWIDTH / 3) - 15, (WINDOWHEIGHT / 3))
drawText('Press any key to start', font, windowSurface, (WINDOWWIDTH / 3) - 85, (WINDOWHEIGHT / 3) + 70)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    enemies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    EnemyAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # igra v loop
        score += 1 # uvelichivaet schet

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEMOTION:
                # cursor
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]
        # adding new enemies if needed
        if not reverseCheat and not slowCheat:
            EnemyAddCounter += 1
        if EnemyAddCounter == ADDNEWEnemyRATE:
            EnemyAddCounter = 0
            enemiesize = random.randint(EnemyMINSIZE, EnemyMAXSIZE)
            newEnemy = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - enemiesize), 0 - enemiesize, enemiesize, enemiesize),
                        'speed': random.randint(EnemyMINSPEED, EnemyMAXSPEED),
                        'surface':pygame.transform.scale(EnemyImage, (enemiesize, enemiesize)),
                        }

            enemies.append(newEnemy)

        # moving player
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # moving enemies
        for b in enemies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # deleting enemies
        for b in enemies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                enemies.remove(b)

        windowSurface.fill(BACKGROUNDCOLOR)

        # score draw
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # player draw
        windowSurface.blit(playerImage, playerRect)

        # enemy draw
        for b in enemies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # checks hitting enemies
        if playerHasHitEnemy(playerRect, enemies):
            if score > topScore:
                topScore = score # new score
            break

        mainClock.tick(FPS)

    # gameover screen
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()