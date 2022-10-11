import pygame, sys
from pygame.locals import QUIT
import time
import random

pygame.init()

#screen size variables
w_mult = 80
h_mult = 80

screen_width = 10
screen_height = 1

# set the screen
screen = pygame.display.set_mode((screen_width * w_mult, screen_height * h_mult))
pygame.display.set_caption('StarryFactory')


# rules for pixel interpretation
neighborsToLive = 1
neighborsToDie = 2

# the amount of distance between the pixels
screenStepX = 10
screenStepY = 10

# list that pixels are stored in
pixelsList = []

# pixel images
pixelImg = pygame.image.load('pixelImg.png')

################
# PIXELS STUFF #
################

def Run():
    #print updated pixels
    time.sleep(0.01)
    InterpretPixels(pixelsList)
    BlitPixels()


def Set_Pixel_Array():
  print("pixels SET")
  # list that pixels are stored in
  pixelsList = [[random.randint(0, 1) for x in range (screen_width)] for y in range (screen_height)]
  return pixelsList


def BlitPixels(list):
  print("BLIT")
  screen.fill((0, 0, 0))
  for y in range (screen_height):
    for x in range (screen_width):
      if list[y][x] == 1:
        screen.blit(pixelImg, (x * screenStepX, y * screenStepY))

######
######

def InterpretPixels(list):
  # iterate through pixels
  time.sleep(1)
  for y in range (screen_height):
    for x in range (screen_width):
      
      # Check neighbor pixel states (1 or 0?)
      neighbors = 0
  
      # First neighbor: index +1
      unNormalizedIndex = i + 1
      if (unNormalizedIndex > len(list) - 1):
        normalizedIndex = 0
      else:
        normalizedIndex = i + 1
  
      if list[normalizedIndex] == 1:
        neighbors += 1
  
      # Second neighbor: index - 1
      #make sure that that index exists!
      if (list[i - 1] != None):
        if list[i - 1] == 1:
          neighbors += 1
  
      # Third neighbor: index + screen width
      #check if that index exists!
      unNormalizedIndex = i + screen_width
  
      if unNormalizedIndex > len(list):
        normalizedIndex = 1
      else:
        normalizedIndex = i
  
      if list[normalizedIndex] == 1:
        neighbors += 1
  
      # Fourth neighbor: index - screen width
      unNormalizedIndex = i - screen_width
  
      if unNormalizedIndex < len(list):
        normalizedIndex = 0
      else:
        normalizedIndex = i
  
      if list[normalizedIndex] == 1:
        neighbors += 1
  
      # Toggle pixel state based on neighbors
      pixel = list[i]
  
      # Loneliness....
      if neighbors < neighborsToLive:
        pixel = 0
  
      # Good amount of neighbors!
      if neighbors >= neighborsToLive & neighbors < neighborsToDie:
        pixel = 1
  
      # Overcrowding
      if neighbors >= neighborsToDie:
        pixel = 0
  
      # change pixel's value in list
      list[i] = pixel

########
# LOOP #
########
pixelsList = Set_Pixel_Array()
while True:
    # update the pixels
    Run()

    # closing the window?
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
          
    pygame.display.update()

  
