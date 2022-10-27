import pygame, sys
from pygame.locals import QUIT
import time
import random

pygame.init()

# time
discreteStep = 1

# screen size variables
screen_width = 20
screen_height = 20

screenStepX = 16
screenStepY = 16

offsetX = 10
offsetY = 10

# set the screen
screen = pygame.display.set_mode(
    (screen_width * 17, screen_height * 17))
pygame.display.set_caption('Starry Factor')

# pixels
pixelsList = []

pixelImg = pygame.image.load('1.png')
diseasedImg = pygame.image.load('diseased.png')

oldAgeThresh = 10 # pixels die after this many gens

###########
# Classes #
###########

class Pixel():
  def __init__(self, iX, iY):
    self.iX = iX # x index (in list)
    self.iY = iY # y index

    self.genCount = 0
    self.alive = random.randint(0, 1) # random seed for each pixel
    self.diseased = False

    self.moveDir = random.randint(1, 4) # where will they try to move?

  def Update(self):
    if (self.genCount >= oldAgeThresh):
      self.alive = 0
      
    self.genCount += 1

  def MovePixel(self, x, y):
    # normalize accessible indices for overwrite
    indexX = 0
    indexY = 0
  
    if (self.moveDir == 1): # moving right
      # if x + 1 is out of range 
      # (all rows EXCEPT last bottom row)
      if (x + 1 >= len(pixelsList[y]) - 1):
        indexX = 0
        indexY = y + 1

      # Bottom Row
      if (y == screen_height & x + 1 >= len(pixelsList[y]) - 1):
        indexX = 0
        indexY = 0
        

    elif (self.moveDir == 2): # moving left
      # if x - 1 is out of range
      # (all rows EXCEPT top row))
      if (x - 1 < 0):
        indexX = 0

      # top row (going to the bottom last x)
      if (y == 0 & x - 1 < 0):
        indexX = screen_width
        indexY = screen_height
        
    # finally, overwrite the proposed pixel with 
      # the information from the current pixel
    OverWriteDeadPixel(indexX, indexY, self.moveDir)

  
################
# PIXELS STUFF #
################

def Set_Pixel_Array():
    # list that pixels are stored in
    pixelsList = [[Pixel(x, y) for x in  range(screen_width)]
                  for y in range(screen_height)]
  
    return pixelsList


def Pixels():
  time.sleep(discreteStep)

  # iterate through matrix
  for y in range(screen_height):
      for x in range(screen_width):
        
          # update each pixel instance
          pixelsList[y][x].Update()

          # move each pixel
          pixelsList[y][x].MovePixel(x, y)

          # show them on screen
          if pixelsList[y][x].alive == 1:
              screen.blit(pixelImg, ((x * screenStepX) + offsetX, (y * screenStepY) + offsetY))

def OverWriteDeadPixel(x, y, MoveDir):
  if (MoveDir == 1):
    # transfer all information over to the right pixel
    pixelsList[y][x + 1].genCount = pixelsList[y][x].genCount
    pixelsList[y][x + 1].diseased = pixelsList[y][x].diseased
    pixelsList[y][x + 1].moveDir = random.randint(1, 4)
    pixelsList[y][x + 1].alive = 1

  if (MoveDir == 2):
    # transfer all information over to the left pixel
    pixelsList[y][x - 1].genCount = pixelsList[y][x].genCount
    pixelsList[y][x - 1].diseased = pixelsList[y][x].diseased
    pixelsList[y][x - 1].moveDir = random.randint(1, 4)
    pixelsList[y][x - 1].alive = 1

  if (MoveDir == 3):
    # transfer all information over to the right pixel
    pixelsList[y - 1][x].genCount = pixelsList[y][x].genCount
    pixelsList[y - 1][x].diseased = pixelsList[y][x].diseased
    pixelsList[y - 1][x].moveDir = random.randint(1, 4)
    pixelsList[y - 1][x].alive = 1
  
  if (MoveDir == 4):
    # transfer all information over to the right pixel
    pixelsList[y + 1][x].genCount = pixelsList[y][x].genCount
    pixelsList[y + 1][x].diseased = pixelsList[y][x].diseased
    pixelsList[y + 1][x].moveDir = random.randint(1, 4)
    pixelsList[y + 1][x].alive = 1
    
  pixelsList[y][x].alive = 0 # kill original pixel

  
########
# LOOP #
########

pixelsList = Set_Pixel_Array()

while True:
    screen.fill((211,211,211))
    Pixels()

    # closing the window?
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
