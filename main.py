import pygame, sys
from pygame.locals import QUIT
import time
import random

pygame.init()

# time
discreteStep = .8

# screen size variables
screen_width = 20
screen_height = 20

screenStepX = 16
screenStepY = 16

sFactor = 17

# for random movement
stepListX = [screenStepX, -screenStepX]
stepListY = [screenStepY, -screenStepY]

offsetX = 10
offsetY = 10

# set the screen
screen = pygame.display.set_mode(
    (screen_width * (sFactor + 1), screen_height * (sFactor + 1)))
pygame.display.set_caption('Starry Factor')

# pixels
pixelsList = []

baseImg = pygame.image.load('img/1.png')
greenImg = pygame.image.load('img/green.png')
blueImg = pygame.image.load('img/blue.png')
purpleImg = pygame.image.load('img/purple.png')
yellowImg = pygame.image.load('img/yellow.png')
redImg = pygame.image.load('img/red.png')


oldAgeThresh = 60 # pixels die after this many gens

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

    self.dY = 0
    self.dX = 0

  def Update(self):
    if (self.genCount >= oldAgeThresh):
      self.alive = 0
      
    self.genCount += 1

    if (random.randint(0, 150) == 0): # 1 in 151 chance
      self.genCount -= random.randint(0, 5) # to lower gen count

  def CalcMoveAmounts(self, x, y):
    self.dX = random.choice(stepListX)
    self.dY = random.choice(stepListY)
    
    return self.dX, self.dY

################
# PIXELS STUFF #
################

def ChooseImageBasedOnGen(gen):

  if gen > 10 & gen < 15:
    imgLocal = greenImg

  if gen >= 15 & gen < 20:
    imgLocal = blueImg

  if gen >= 20 & gen < 30:
    imgLocal = purpleImg

  if gen >= 30 & gen < 40:
    imgLocal = yellowImg

  if gen >= 40:
    imgLocal = redImg

  else:
    imgLocal = baseImg
    
  return imgLocal

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

          # calculate the movement of each pixel
          localDX, localDY = pixelsList[y][x].CalcMoveAmounts(x, y)

                          #####
              ############# Y #############
                          #####
          # if we are moving off screen (down)
          if (y * screenStepY + localDY >= screen_height * sFactor):
            localDY = 0

           # if we are moving off screen (up)
          if (y * screenStepY + localDY <= 0):
            localDY = 0

          # if we are hitting another pixel
            
                          #####
              ############# X #############
                          #####
          # if we are moving off screen (right)
          if (y * screenStepX + localDX >= screen_width * sFactor):
            localDX = 0

           # if we are moving off screen (left)
          if (x * screenStepX + localDX <= 0):
            localDX = 0

          # if we are hitting another pixel

                        ########
              ########### BLIT #############
                        ########   
            
          # select image based on generation
          pixelsList[y][x].image = ChooseImageBasedOnGen(pixelsList[y][x].genCount)
        
          # show them on screen
          if pixelsList[y][x].alive == 1:
              screen.blit(pixelsList[y][x].image, (((x * screenStepX) + offsetX) + localDX, ((y * screenStepY) + offsetY) + localDY))

  
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
    print("LOOP")

