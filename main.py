import pygame, sys
from pygame.locals import QUIT
import time
import random

pygame.init()

#screen size variables
screen_width = 300
screen_height = 300

# the amount of distance between the pixels
screenStepX = 16
screenStepY = 16

# the distance the entire 
# pixel zone will be shifted
offsetX = 10
offsetY = 10

# set the screen
screen = pygame.display.set_mode(
    (screen_width, screen_height))
pygame.display.set_caption('StarryFactory')

# rules for pixel interpretation
neighborsToLive = 2
neighborsToDie = 4



# list that pixels are stored in
pixelsList = []

# pixel images
pixelImg = pygame.image.load('1.png')

################
# PIXELS STUFF #
################

def Run():
    #print updated pixels
    time.sleep(0.01)
    InterpretPixels(pixelsList)
    BlitPixels()

def SetScreenSpacing():
  pass

def Set_Pixel_Array():
    # list that pixels are stored in
    pixelsList = [[random.randint(0, 1) for x in  range(screen_width)]
                  for y in range(screen_height)]
    return pixelsList


def BlitPixels():
  print("BLIT")
  screen.fill((255, 255, 255))
  for y in range(screen_height):
      for x in range(screen_width):
          if pixelsList[y][x] == 1:
              screen.blit(pixelImg, ((x * screenStepX) + offsetX, (y * screenStepY) + offsetY))


              
########################
# PIXEL INTERPRETATION #
########################

def InterpretPixels(list):
    # iterate through pixels
    time.sleep(1)
    for y in range(screen_height):
        for x in range(screen_width):
          
            # Check neighbor pixel states (1 or 0?)
            neighbors = 0

            ###########################
            #   NEIGHBOR BLOCK 1      #
            ###########################
              # x index +1

            # does this element even exist here?
            if (x + 1 > len(list[y]) -1):
                hasNeighbor = False
                #  nope!
            else:
                hasNeighbor = True
                # it does!

            if hasNeighbor:
              if list[y][x + 1] == 1:
                neighbors += 1

                
            ###########################
            #   NEIGHBOR BLOCK 2      #
            ###########################
              # x index - 1
                

            # does this element even exist here?
            if (x - 1 < 0):
                hasNeighbor = False
                #  nope!
            else:
                hasNeighbor = True
                # it does!

            if hasNeighbor:
              if list[y][x - 1] == 1:
                neighbors += 1

                  
            ###########################
            #   NEIGHBOR BLOCK 3      #
            ###########################    
              # y index - 1

            # does this element even exist here?
            if (y - 1 < 0):
                hasNeighbor = False
                #  nope!
            else:
                hasNeighbor = True
                # it does!

            if hasNeighbor:
              if (list[y - 1][x] == 1):
               neighbors += 1

              
            ###########################
            #   NEIGHBOR BLOCK 4      #
            ###########################
              # y index + 1
                
            #does this element even exist here?
            if (y + 1 > len(list) - 1):
                hasNeighbor = False
                #  nope!
            else:
                hasNeighbor = True
                # it does!

            if hasNeighbor:
              if list[y + 1][x] == 1:
                neighbors += 1


              
            ###########################
            #   MANAGE PIXEL STATES   #
            ###########################
              
            # Toggle pixel state based on neighbors
            pixel = list[y][x]
            if (pixel == 1):
              aliveForOneGen = True
            elif (pixel == 0):
              aliveForOneGen = False

            # Loneliness....
            if neighbors < 2:
                pixel = 0

            # Good amount of neighbors!
            if neighbors >= 2 & neighbors <= 3:
                pixel = 1
 
            # Overcrowding
            if neighbors > 3:
                pixel = 0

            # Pixel has been alive for a gen?
            if (aliveForOneGen):
              pixel = 0
            # if its dead and has 3 neighbors, resurerect!
            elif (neighbors == 3) & aliveForOneGen == False:
              pixel = 1
              
            # change pixel's value in list
            list[y][x] = pixel


########
# LOOP #
########

pixelsList = Set_Pixel_Array()

while True:
    screen.fill((0, 0, 255))
    # update the pixels
    Run()

    # closing the window?
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
