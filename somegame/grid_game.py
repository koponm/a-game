import pygame
import sys
import time
import random
import os

pygame.init()


#Constants
display_width = 800
display_height = 600
FPS=100
tile_size = 50
width = 16
height = 12
difficulty=1.5 #seconds to press the button

score = 0 #Game score
startTime = 30
#starting time, how long the game lasts

#Colors
black  = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
dim_gray = (105,105,105)


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Simple grid game')
clock = pygame.time.Clock()

time=startTime
highscore =0
#checking the previous highscore
f= open("highscore.txt","w+") # finding out the previous highscore
contents= f.read()
if os.stat("highscore.txt").st_size != 0:
	highscore=int(contents)
f.close()

#Creating the gameboard wich is tile_size*tile_size pixels
x_count=0
y_count=0
board = []
for col in range(height):
    column = []
    y_min = y_count
    for row in range(width):
        x_min = x_count
        x_count = x_count+tile_size
        ob=[x_min,y_min,0]
        column.append(ob)
    board.append(column)
        
    x_count = 0
    y_count = y_count + tile_size


#Random tile location
random_x = None
random_y = None
random_tile = False

    
    
again = False # determines whether the game has been restarted
crashed = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
            
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    gameDisplay.fill(black) # color can be changed
    ended = False # determines whether the game has ended
    if time<=0:
        ended = True
   
    if random_tile and not ended and not again:
        pygame.draw.rect(gameDisplay,blue,(random_x*tile_size,random_y*tile_size,tile_size,tile_size))
   
    if not random_tile:
        random_x = random.randint(1,width-2)
        random_y = random.randint(1,height-2) #no sidegrids
        board[random_y][random_x][2]= difficulty*FPS
        random_tile=True
    elif board[random_y][random_x][2]<= 0:
        random_x = random.randint(1,width-2)
        random_y = random.randint(1,height-2)
        board[random_y][random_x][2]= difficulty*FPS
        random_tile=True
    else:
        board[random_y][random_x][2] -= 1

    #mouse location tile
    xp=mouse[0]//tile_size
    yp=mouse[1]//tile_size
    loc = board[yp][xp]
    clicked = False
    if click[0]==1:
        clicked = True
        if yp==0 or yp==height-1 or xp==0 or xp == width-1 or ended or  again:
            clicked = False
        elif xp==random_x and yp==random_y: 
            pygame.draw.rect(gameDisplay,green,(loc[0],loc[1],tile_size,tile_size))
            score += 10
            score += int(round(((board[random_y][random_x][2])/FPS*10)))
            board[random_y][random_x][2]=0
            random_tile=False
        else:
            pygame.draw.rect(gameDisplay,red,(loc[0],loc[1],tile_size,tile_size))
            board[random_y][random_x][2]=0
            random_tile= False
            score -= 10


    
    for col in range(50, display_width-50, tile_size):
        for row in range(50, display_height-50, tile_size):
            pygame.draw.rect(gameDisplay, white, (col,row,tile_size + 1,tile_size + 1),1)


    myfont = pygame.font.Font('freesansbold.ttf', 30)
    text1= "Time left: "+str(int(round(time)))
    text2= "Score: "+str(score)
    textsurface1 = myfont.render(text1, True, red)
    textsurface2 = myfont.render(text2, True, red)
    gameDisplay.blit(textsurface2,(display_width-200,10))
    gameDisplay.blit(textsurface1,(100,10))
        
    #Game ended/restart
    if ended:
        textsurface3 = myfont.render("Your score: "+str(score),True,red)
        if highscore<score:
            highscore=score
            f= open("highscore.txt", "a+")
            f.truncate(0)
            f.write(str(highscore))
            f.close()
		
        txt5 = pygame.font.Font('freesansbold.ttf', 25).render("Highscore: "+str(highscore),True,red)
        


        pygame.draw.rect(gameDisplay,black,(250,200,300,200))
        gameDisplay.blit(textsurface3,(300,275))
        gameDisplay.blit(txt5,(320,230))
        pygame.draw.rect(gameDisplay, red, (250,200,tile_size*6 + 1,tile_size*4 + 1),1)
        font2 = pygame.font.Font('freesansbold.ttf',20)
        textsurface4 = font2.render("Try again",True,red)
        textsurface5 = font2.render("Quit game",True,red)
		


        if 100+410>mouse[0]>410 and 40+320>mouse[1]>320:
            pygame.draw.rect(gameDisplay,dim_gray,(410,320,100,40))
            pygame.draw.rect(gameDisplay,red,(280,320,110,40),1)
            if click[0]==1:
              again=True
        elif 100+280>mouse[0]>280 and 40+320>mouse[1]>320:
            pygame.draw.rect(gameDisplay,dim_gray,(280,320,110,40))
            pygame.draw.rect(gameDisplay,red,(410,320,100,40),1)
            if click[0]==1:
               pygame.quit()
        else:           
		
            pygame.draw.rect(gameDisplay,red,(410,320,100,40),1)
            pygame.draw.rect(gameDisplay,red,(280,320,110,40),1)
        gameDisplay.blit(textsurface4,(415,330))
        gameDisplay.blit(textsurface5,(285,330))

		
        
		
        

    pygame.display.update()
    
    if not ended and not again:
        #Time stuff
        if clicked:
            pygame.time.wait(500) #Wait time between clicks
            time-=0.5 #time goes on even when time "stops"
        time -= 1/FPS
    if again:
        score=0
        time=startTime
        pygame.time.wait(500)
        again=False
    
    clock.tick(FPS) #fps


    
    

pygame.quit()
quit()
