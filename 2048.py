import pygame, sys, random, time
from pygame.locals import *
highscore=[]
score=0
Board=[[0 for x in range(0,4)] for x in range (0,4)]
pygame.init()
#file for storing the highscores
f=open("scores.txt","a")
f.close()
# set up the window
DISPLAYSURF = pygame.display.set_mode((800, 800),0, 32)
pygame.display.set_caption('Animation')
IsCombined=[[0 for x in range(0,4)] for x in range (0,4)]
BASICFONT=pygame.font.Font('freesansbold.ttf',40)
GAMEFONT=pygame.font.Font('freesansbold.ttf',80)
full=255
half=128
def newboard():
	"""Sets up a new board when the user wants to play again."""
	score=0
	Board=[[2 for x in range(0,4)] for x in range (0,4)]
def TileColours(n,full,half):
	"""To assign a numbered tile a specific colour"""
	if n==2:return (full,full,full)
	elif n==4:return (full,0,0)
	elif n==8:return (0,full,0)
	elif n==16:return (0,0,full)
	elif n==32:return (0, full,full)
	elif n==64:return (full, 0,full)
	elif n==128:return (full,full, 0)
	elif n==256:return (  0, half, full)
	elif n==512:return (full,0,half)
	elif n==1024:return (half, full,0)
	else :return (half,half,half)

def welcome():
	"""This is the welcome screen"""
	DISPLAYSURF = pygame.display.set_mode((800, 800),0, 32)
	text="Welcome to 2048.Press the arrow keys to move the tiles.Hit Spacebar to start playing."
	line=text.split('.')
	y=150
	for i in range(0,3):
		welSurf=BASICFONT.render(line[i],True,(0,full,0))
		welRect=welSurf.get_rect()
		welRect.center=(400,y)
		DISPLAYSURF.blit(welSurf,welRect)
		y+=75
	pygame.display.update()


def DrawBoard(text):
	"""This function draws the whole 2048 board"""
	DISPLAYSURF = pygame.display.set_mode((800, 800), 0, 32)
	pygame.draw.rect(DISPLAYSURF,(100,100,100),((150,270,500,500)))
	gameSurf=GAMEFONT.render(text,True,(full,full,0))
	gameRect=gameSurf.get_rect()
	gameRect.center=(400,150)
	DISPLAYSURF.blit(gameSurf,gameRect)
	
	pointSurf=BASICFONT.render("Score: "+str(score),True,(full,full,0))
	pointRect=pointSurf.get_rect()
	pointRect.left=550
	pointRect.top=50
	DISPLAYSURF.blit(pointSurf,pointRect)
	for i in range(0,4):
		for j in range(0,4):
			LOST=True
			if Board[i][j]==0:
				pygame.draw.rect(DISPLAYSURF,(150,150,150),((180+110*j,300+110*i,100,100)))
				LOST=False
			else:
				makeTile(180+110*j,300+110*i,Board[i][j], TileColours(Board[i][j],255,128))

				
def number_generate():
	"""Randomly generates a tile with number 2 at each turn."""
	newx=random.randrange(0,4)
	newy=random.randrange(0,4)
	while Board[newx][newy]!=0:
		newx=random.randrange(0,4)
		newy=random.randrange(0,4)
	makeTile(180+110*newy,300+110*newx,2,(240,240,240))
	Board[newx][newy]=2

		
def makeTile(x,y,n,colour,size=100):
	"""For drawing a tile. This function is used by DrawBoard()"""
	pygame.draw.rect(DISPLAYSURF,colour, (x,y, size,size))
	textSurf=BASICFONT.render(str(n),True,(0,0,0))
	textRect=textSurf.get_rect()
	textRect.center=(x+50,y+50)
	DISPLAYSURF.blit(textSurf, textRect)

def expandTile(i,j):
	"""To create the combining effect when two tiles clash"""
	makeTile(175+110*j,295+110*i,Board[i][j], TileColours(Board[i][j],128,64),110)
	pygame.display.update()
	time.sleep(0.05)

def update_highscores():
	"""Updates the highscores in the file"""
	written=False
	counter=0
	contents=[]
	f=open("scores.txt","r")
	for line in f:
		contents.append(line)
		print line
		if int(line)>score:
			counter+=1
	print counter
	print contents
	f.close()
	if counter<5:
		contents.insert(counter,str(score)+"\n")

		f = open("scores.txt", "w")
		contents = "".join(contents)
		f.write(contents)
		f.close()
	print contents

def endscreen():
	"""Displays the highscores"""
	DISPLAYSURF = pygame.display.set_mode((800, 800),0, 32)
	text="Hit Spacebar to play again"
	file=open("scores.txt","r")
	highscore = [line.strip() for line in file if line.strip()]
	y=100
	for i in range(-1,min(5,len(highscore))):
		if i==-1:
			welSurf=BASICFONT.render(text,True,(full,full,0))
			lx=150
		else:
			welSurf=BASICFONT.render("#"+str(i+1)+". "+str(highscore[i]),True,(0,full,0))
			lx=300
		welRect=welSurf.get_rect()
		welRect.left=lx
		welRect.top=y
		DISPLAYSURF.blit(welSurf,welRect)
		y+=100
	pygame.display.update()
	file.close()

def MoveTiles(key,exc):
	"""The whole algorithm of 2048"""
	global score
	
	if key==K_UP:
		for j in range(0,4):
			for i in range(0,3):
				if Board[i][j]==0 and Board[i+1][j]!=0:
					if exc==0:
						Board[i][j],Board[i+1][j]=Board[i+1][j],Board[i][j]
					return True
				elif Board[i][j]==Board[i+1][j] and Board[i][j]!=0 and IsCombined[i][j]==0 and IsCombined[i+1][j]==0:
					if exc==0:
						Board[i][j]*=2
						Board[i+1][j]=0
						IsCombined[i][j]=1
						score+=Board[i][j]
						expandTile(i,j)
					return True	
				
					
	elif key==K_DOWN:
		for j in range(0,4):
			for i in range(3,0,-1):
				if Board[i][j]==0 and Board[i-1][j]!=0:
					if exc==0:
						Board[i][j],Board[i-1][j]=Board[i-1][j],Board[i][j]
					return True
					
				elif Board[i][j]==Board[i-1][j] and Board[i][j]!=0 and IsCombined[i][j]==0 and IsCombined[i-1][j]==0:
					if exc==0:
						Board[i][j]*=2
						Board[i-1][j]=0
						IsCombined[i][j]=1
						score+=Board[i][j]
						expandTile(i,j)
					return True	
					
	elif key==K_LEFT:
		for i in range(0,4):
			for j in range(0,3):
				if Board[i][j]==0 and Board[i][j+1]!=0:
					if exc==0:
						Board[i][j],Board[i][j+1]=Board[i][j+1],Board[i][j]
					return True
				elif Board[i][j]==Board[i][j+1] and Board[i][j]!=0 and IsCombined[i][j]==0 and IsCombined[i][j+1]==0:

					if exc==0:
						Board[i][j]*=2
						Board[i][j+1]=0
						IsCombined[i][j]=1
						score+=Board[i][j]
						expandTile(i,j)
					return True	
					
	elif key==K_RIGHT:
		for i in range(0,4):
			for j in range(3,0,-1):
				if Board[i][j]==0 and Board[i][j-1]!=0:
					if exc==0:
						Board[i][j],Board[i][j-1]=Board[i][j-1],Board[i][j]
					return True
					
				elif Board[i][j]==Board[i][j-1] and Board[i][j]!=0 and IsCombined[i][j]==0 and IsCombined[i][j-1]==0:
					if exc==0:
						Board[i][j]*=2
						Board[i][j-1]=0
						IsCombined[i][j]=1
						score+=Board[i][j]
						expandTile(i,j)
					return True
					
	return False
newboard()
welcome()

WHITE = (full, full, full)
started=False
while True:


	for event in pygame.event.get():
		if event.type==KEYUP:
			if started==False and event.key==K_SPACE:
				DrawBoard("2048")
				number_generate()
				started=True
				pygame.display.update()
				break
			if started==True:
									

				move=False
				while MoveTiles(event.key,0)==True:
					time.sleep(0.01)
					DrawBoard("2048")
					move=True
					pygame.display.update()

				if move==True:						
					time.sleep(0.01)
					number_generate()
					DrawBoard("2048")
					pygame.display.update()

				IsCombined=[[0 for x in range(0,4)] for x in range (0,4)]
				if MoveTiles(K_UP,1)==False and MoveTiles(K_DOWN,1)==False and MoveTiles(K_LEFT,1)==False and MoveTiles(K_RIGHT,1)==False:
					pygame.display.set_caption("LOST")
					DrawBoard("GAME OVER.")
					pygame.display.update()
					time.sleep(3)
					
					update_highscores()
					endscreen()
					newboard()
					score=0
					Board=[[0 for x in range(0,4)] for x in range (0,4)]
					started=False
					
			
		elif event.type==QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()