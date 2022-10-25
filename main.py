import pygame, sys
from pygame.locals import QUIT
import time
import random

pygame.init()


# diseases and plagues
diseaseStatusList = []

# screen size variables
screen_width = 20
screen_height = 20

# the amount of distance between the pixels
screenStepX = 16
screenStepY = 16

# the distance the entire
# pixel zone will be shifted (padding)
offsetX = 10
offsetY = 10

# set the screen
screen = pygame.display.set_mode(
    (screen_width * 17, screen_height * 17))
pygame.display.set_caption('Starry Factor')

# list that pixels are stored in
pixelsList = []

# list of generation counts for corresponding pixels
generationCounters = []

# pixel images
pixelImg = pygame.image.load('1.png')
diseasedImg = pygame.image.load('diseased.png')

imgList = [pixelImg, diseasedImg]

###########
# Classes #
###########

class Pixel():
  def __init__(self, iX, iY):
    self.iX = iX # x index (in list)
    self.iY = iY # y index

    self.genCount = 0
    self.diseased = False
    
  
################
# PIXELS STUFF #
################

def Run():
    #print updated pixels
    time.sleep(0.01)
    InterpretPixels(pixelsList)
    BlitPixels()


def Set_Pixel_Array():
    # list that pixels are stored in
    pixelsList = [[random.randint(0, 1) for x in  range(screen_width)]
                  for y in range(screen_height)]

    generationCounters = [[0 for x in  range(screen_width)]
                  for y in range(screen_height)]
    return pixelsList, generationCounters


def BlitPixels():
  print("BLIT")
  screen.fill((255, 255, 255))
  for y in range(screen_height):
      for x in range(screen_width):
          if pixelsList[y][x] == 1:
              screen.blit(random.choice(imgList), ((x * screenStepX) + offsetX, (y * screenStepY) + offsetY))


              
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

            CheckNeighbors(neighbors, x, y, list)


            ###########################
            #   MANAGE PIXEL STATES   #
            ###########################
              
            # Find pixel and check if it 
              # has been alive for two gens
            pixel = list[y][x]
          
            aliveTwoGen = False

            # if it has, kill it 
            if generationCounters[y][x] == 2:
              pixel = 0
              aliveTwoGen = True
              generationCounters[y][x] = 0
              
            # if the pixel is alive, 
              # add to generation counter 
            elif (pixel == 1):
              generationCounters[y][x] += 1
              
            # Loneliness....
            if neighbors < 2:
                pixel = 0

            # Good amount of neighbors!
            if neighbors >= 2 & neighbors <= 3:
                pixel = 1
 
            # Overcrowding
            if neighbors > 3:
                pixel = 0

            
            # if its dead and has 3 neighbors, resurrect!
            elif (neighbors == 3) &  pixel == 0:
              pixel = 1
              
            # Pixel has been alive for a gen?
            if (aliveTwoGen):
              pixel = 0
                
            # change pixel's value in list
            list[y][x] = pixel


def CheckNeighbors(neighbors, x, y, list):
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
      
  # does this element even exist here?
  if (y + 1 > len(list) - 1):
      hasNeighbor = False
      #  nope!
  else:
      hasNeighbor = True
      # it does!

  if hasNeighbor:
    if list[y + 1][x] == 1:
      neighbors += 1

      
########
# LOOP #
########

pixelsList, generationCounters = Set_Pixel_Array()

while True:
    screen.fill((211,211,211))
    # update the pixels
    Run()

    # closing the window?
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
