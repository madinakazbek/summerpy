import pygame
import sys
import random
from pygame.locals import *


pygame.init()
fpsClock = pygame.time.Clock()
pygame.display.set_caption('snake')
surface = pygame.display.set_mode((640, 480))

font = pygame.font.Font(None, 32)

class Position:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class GameData:

	def __init__(self):
		self.lives = 3
		self.isDead = False
		self.blocks = []
		self.tick = 250
		self.speed = 250
		self.level = 1
		self.fruitcount = 0
		self.segments = 1
		self.frame = 0
		
		bx = random.randint(1, 38)
		by = random.randint(1, 28)
		
		self.fruit = Position(bx, by)
		self.blocks.append(Position(20,15))
		self.blocks.append(Position(19,15))
		self.direction = 0

def loseLife(gamedata):
	gamedata.lives -= 1
	gamedata.direction = 0
	gamedata.blocks[:] = []
	gamedata.blocks.append(Position(20,15))
	gamedata.blocks.append(Position(19,15))

def positionfruit(gamedata):
	bx = random.randint(1, 38)
	by = random.randint(1, 28)
	found = True
	
	while (found):
		found = False
		for b in gamedata.blocks:
			if (b.x == bx and b.y == by):
				found = True
				
		if (found):
			bx = random.randint(1, 38)
			by = random.randint(1, 28)				
			
	gamedata.fruit = Position(bx, by)


def loadMapFile(fileName):
	f = open(fileName, 'r')
	content = f.readlines()
	f.close()
	return content
	
def headHitBody(gamedata):
	head = gamedata.blocks[0]
	
	for b in gamedata.blocks:
		if (b != head):
			if (b.x == head.x and b.y == head.y):
				return True
				
	return False
	
def headHitWall(map, gamedata):
	row = 0

	for line in map:
		col = 0
		for char in line:
			if ( char == '1'):	
				if (gamedata.blocks[0].x == col and gamedata.blocks[0].y == row):
					return True

			col += 1

		row += 1	
		
	return False

def drawData(surface, gamedata):
	text = font.render("Lives left = %d, Level = %d" % ( gamedata.lives, gamedata.level ), 0, (255, 255, 255))
	textpos = text.get_rect(centerx=surface.get_width()/2, top=32)
	surface.blit(text, textpos)
	
def drawGameOver(surface):
	text1 = font.render("Game Over", 1, (255, 255, 255))
	text2 = font.render("Press space to continue", 1, (255, 255, 255))
	textpos1 = text1.get_rect(centerx=surface.get_width()/2, top=surface.get_height()/2 - 48)
	textpos2 = text2.get_rect(centerx=surface.get_width()/2, top=surface.get_height()/2)
	surface.blit(text1, textpos1)
	surface.blit(text2, textpos2)
	
	
def drawWalls(surface, img, map):

	row = 0

	for line in map:
		col = 0
		for char in line:
			if ( char == '1'):
				imgRect = img.get_rect()
				imgRect.left = col * 16
				imgRect.top = row * 16
				surface.blit(img, imgRect)
			col += 1

		row += 1

def drawSnake(surface, img, gamedata):
	first = True

	for b in gamedata.blocks:
		dest = (b.x * 16, b.y * 16, 16, 16)
		if ( first ):
			first = False
			src = (((gamedata.direction * 2) + gamedata.frame) * 16, 0, 16, 16)
		else:
			src = (8 * 16, 0, 16, 16)

		surface.blit(img, dest, src)
		
def updateGame(gamedata, gameTime):
	gamedata.tick -= gameTime
	
	head = gamedata.blocks[0]
	
	if (gamedata.tick < 0):
		gamedata.tick += gamedata.speed
		gamedata.frame += 1
		gamedata.frame %= 2
		if (gamedata.direction == 0):
			move = (1, 0)
		elif (gamedata.direction == 1):
			move = (-1, 0)
		elif (gamedata.direction == 2):
			move = (0, -1)
		else:
			move = (0, 1)
			
		newpos = Position(head.x + move[0], head.y + move[1])
		
		first = True
		for b in gamedata.blocks:
			temp = Position(b.x, b.y)
			b.x = newpos.x
			b.y = newpos.y
			newpos = Position(temp.x, temp.y)

	keys = pygame.key.get_pressed()
				
	if (keys[K_RIGHT] and gamedata.direction != 1):
		gamedata.direction = 0
	elif (keys[K_LEFT] and gamedata.direction != 0):
		gamedata.direction = 1
	elif(keys[K_UP] and gamedata.direction != 3):
		gamedata.direction = 2 
	elif(keys[K_DOWN] and gamedata.direction != 2):
		gamedata.direction = 3
		
	#коллизия фрукта
	if (head.x == gamedata.fruit.x and head.y == gamedata.fruit.y):
		lastIdx = len(gamedata.blocks) - 1
		for i in range(gamedata.segments):
			gamedata.blocks.append(Position(gamedata.blocks[lastIdx].x, gamedata.blocks[lastIdx].y))
	
		bx = random.randint(1, 38)
		by = random.randint(1, 28)
		gamedata.fruit = Position(bx, by)
		gamedata.fruitcount += 1
		if (gamedata.fruitcount == 10):
			gamedata.fruitcount = 0
			gamedata.speed -= 25
			gamedata.level += 1
			gamedata.segments *= 2
			if (gamedata.segments > 64):
				gamedata.segments = 64
			
			if (gamedata.speed < 100):
				gamedata.speed = 100

def loadImages():
	wall = pygame.image.load('wall.png')
	raspfruit = pygame.image.load('fruit.png')
	snake = pygame.image.load('snake.png')
	
	return {'wall':wall, 'fruit':raspfruit, 'snake':snake}

images = loadImages()

images['fruit'].set_colorkey((255, 0, 255))
snakemap = loadMapFile('map.txt')
data = GameData()

quitGame = False
isPlaying = False

while not quitGame:

	if isPlaying:
		x = random.randint(1, 38)
		y = random.randint(1, 28)
	
		rrect = images['fruit'].get_rect()
		rrect.left = data.fruit.x * 16
		rrect.top = data.fruit.y * 16
	
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		updateGame(data, fpsClock.get_time())
		crashed = headHitWall(snakemap, data) or headHitBody(data)
		if (crashed):
			loseLife(data)
			positionfruit(data)
			
		isPlaying = (data.lives > 0)
		
		if (isPlaying):	
			surface.fill((0, 0, 0))

			drawWalls(surface, images['wall'], snakemap)
			surface.blit(images['fruit'], rrect)
			drawSnake(surface, images['snake'], data)
			drawData(surface, data)
	else:
		keys = pygame.key.get_pressed()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		
		if (keys[K_SPACE]):
			isPlaying = True
			data = None
			data = GameData()
			
		drawGameOver(surface)

	pygame.display.update()
	fpsClock.tick(50)