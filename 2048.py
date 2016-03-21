import pygame, sys, random, time
from pygame.locals import *

#global score
score=0
pygame.init()
# set up the window
DISPLAYSURF = pygame.display.set_mode((800, 800),0, 32)
pygame.display.set_caption('Animation')
Board=[[0 for x in range(0,4)] for x in range (0,4)]
#Board=[[32,4,2,0],[8,32,8,4],[128,64,32,8],[2048,1024,64,16]]
IsCombined=[[0 for x in range(0,4)] for x in range (0,4)]
BASICFONT=pygame.font.Font('freesansbold.ttf',50)
GAMEFONT=pygame.font.Font('freesansbold.ttf',100)

def TileColours(n):
	if n==2:return (255,255,255)
	elif n==4:return (255,0,0)
	elif n==8:return (0,255,0)
	elif n==16:return (0,0,255)
	elif n==32:return (0, 255,255)
	elif n==64:return (255, 0,255)
	elif n==128:return (255,255, 0)
	elif n==256:return (  0, 128, 255)
	elif n==512:return (255,0,128)
	elif n==1024:return (128, 255,0)
	elif n==2048:return (128,128,128)
	else:return (0,0,0)

def DrawBoard(text):
	DISPLAYSURF = pygame.display.set_mode((800, 800), 0, 32)
	pygame.draw.rect(DISPLAYSURF,(100,100,100),((150,270,500,500)))
#	pygame.draw.rect(DISPLAYSURF,(0,0,0), ((300,100, 200,100)))
#	pygame.draw.rect(DISPLAYSURF,(0,0,0), ((600,100, 200,100)))
	gameSurf=GAMEFONT.render(text,True,(255,255,0))
	gameRect=gameSurf.get_rect()
	gameRect.center=(400,150)
	DISPLAYSURF.blit(gameSurf,gameRect)
	pointSurf=BASICFONT.render("Score: "+str(score),True,(255,255,0))
	pointRect=pointSurf.get_rect()
	pointRect.right=750
	pointRect.top=50
	DISPLAYSURF.blit(pointSurf,pointRect)
	for i in range(0,4):
		for j in range(0,4):
			LOST=True
			if Board[i][j]==0:
				pygame.draw.rect(DISPLAYSURF,(150,150,150),((180+110*j,300+110*i,100,100)))
				LOST=False
			else:
				makeTile(180+110*j,300+110*i,Board[i][j], TileColours(Board[i][j]))
#			pygame.display.set_caption(str(Board[i][0]))
				
def number_generate():
#	numcount+=1
	newx=random.randrange(0,4)
	newy=random.randrange(0,4)
	while Board[newx][newy]!=0:
		newx=random.randrange(0,4)
		newy=random.randrange(0,4)
	makeTile(180+110*newy,300+110*newx,2,(255,255,255))
	Board[newx][newy]=2
		
def makeTile(x,y,n,colour):
	pygame.draw.rect(DISPLAYSURF,colour, (x,y, 100,100))
	textSurf=BASICFONT.render(str(n),True,(0,0,0))
	textRect=textSurf.get_rect()
	textRect.center=(x+50,y+50)
	DISPLAYSURF.blit(textSurf, textRect)


def MoveTiles(key,exc):
	
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
						Board[i+1][j]*=2
						Board[i][j]=0
						IsCombined[i+1][j]=1
						score+=Board[i+1][j]
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
						Board[i-1][j]*=2
						Board[i][j]=0
						IsCombined[i][j]=1
						score+=Board[i-1][j]
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
					return True
					
	return False
	
DrawBoard("2048")
number_generate()
WHITE = (255, 255, 255)


while True:
	for event in pygame.event.get():
		
		if event.type==KEYUP:
			IsCombined=[[0 for x in range(0,4)] for x in range (0,4)]
			if MoveTiles(K_UP,1)==False and MoveTiles(K_DOWN,1)==False and MoveTiles(K_LEFT,1)==False and MoveTiles(K_RIGHT,1)==False:
				pygame.display.set_caption("LOST")
				DrawBoard("GAME OVER.")
			else:
				

				move=False
				while MoveTiles(event.key,0)==True:
					
					DrawBoard("2048")
					move=True
					
					#pygame.display.set_caption(str(movecount))
				#time.sleep(1)
				if move==True:
					number_generate()
					
			
		elif event.type==QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()