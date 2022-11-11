import pygame, sys
from pygame.locals import QUIT
import time
import random
import button

pygame.init()
pygame.display.set_caption("Life In Turmoil")

# colors
BLACK = (0, 0, 0)
RED = (150, 0, 0)
GREENBLUE = (0, 200, 100)

# fonts
athena1 = pygame.font.Font("AthenaRustic.ttf", 32)
athena2 = pygame.font.Font("AthenaRustic.ttf", 18)


###############
# SCREEN SIZE #
###############

screen_width = 20
screen_height = 20

screenStepX = 16
screenStepY = 16

sFactor = 17

realScreenWidth = screen_width * (sFactor + 1)
realScreenHeight = screen_height * (sFactor + 2)


#############
# MAIN MENU #
#############

playing = False
options = False

# text
menuText = athena1.render("LIFE IN TURMOIL", True, BLACK)

# text position (title)
titleX = realScreenWidth // 2
titleY = realScreenHeight // 2 - 1 / 4 * realScreenHeight

menuTextRect = menuText.get_rect()
menuTextRect.center = (titleX, titleY)

# menu buttons - images
startButtonImg = pygame.image.load("img/button/StartButton.png")
optionsButtonImg = pygame.image.load("img/button/OptionsButton.png")

buttonScale = 0.22

# menu buttons - definitions
startBTN = button.Button(titleX // 2, titleY * 1.5, startButtonImg,
                         buttonScale)
optionsBTN = button.Button(titleX // 2 + sFactor // 3, titleY * 2.3,
                           optionsButtonImg, buttonScale)

# decorations - images
decorIMG1 = pygame.image.load("img/decor/decor1.png")


################
# OPTIONS MENU #
################

options = False

showGenCounts = False
showPopulation = True

# text
optionsText = athena1.render("OPTIONS OPTIONS OPTIONS OPTIONS", True, RED)

optionsTextRect = optionsText.get_rect()
optionsTextRect.center = (titleX, titleY * 2)

# buttons - images
genOnImg = pygame.image.load("img/button/genCountOn.png")
genOffImg = pygame.image.load("img/button/genCountOff.png")

popOnImg = pygame.image.load("img/button/popCountOn.png")
popOffImg = pygame.image.load("img/button/popCountOff.png")

# buttons - definitions
startBTN2 = button.Button(titleX * 1.4, titleY * 3.4, startButtonImg, buttonScale*0.6)
showGenCountsBTN = button.Button(titleX // 3, titleY *0.8, genOffImg, buttonScale * 8)
showPopCountsBTN = button.Button(titleX // 3, titleY * 2.5, popOffImg, buttonScale * 8)


##############
# ABOUT MENU #
##############

# are we in this menu?
about = False

# buttons - images
aboutIMG = pygame.image.load("img/button/aboutBTN.png")

# buttons - definitions
aboutBTN = button.Button(titleX * 0.73, titleY * 2.69, aboutIMG, buttonScale)


########
# GAME #
########

# text objects
popText = athena1.render("Population Count:", True, BLACK)

popTextRect = popText.get_rect()
popTextRect.center = (titleX * 0.9, titleY * 3.8)


##########
# PIXELS #
##########

#text display
textOffset = -12

# time
discreteStep = .8

# for random movement
stepListX = [screenStepX, -screenStepX]
stepListY = [screenStepY, -screenStepY]

offsetX = 10
offsetY = 10

# set the screen
screen = pygame.display.set_mode((realScreenWidth, realScreenHeight))

# pixels
pixelsList = []

baseImg = pygame.image.load('img/pixel/1.png')
redImg = pygame.image.load('img/pixel/red.png')

oldAgeThresh = 80  # pixels die after this many gens

populationCount = 0

# probability ( (1/num) + 1 ) that gen counters of pixels
# decrease 
deAgeProbability = 100

# increase
preAgeProbability = 100

# maximum modifier to gen counter
maxGenMod = 80

###########
# Classes #
###########

class Pixel():

    def __init__(self, iX, iY):
        self.iX = iX  # x index (in list)
        self.iY = iY  # y index

        self.genCount = 0
        self.genDisplay = athena2.render(str(self.genCount), True, RED)
      
        self.alive = random.randint(0, 1)  # random seed for each pixel
        self.diseased = False

        self.dY = 0
        self.dX = 0

    def Update(self):
        if (self.genCount >= oldAgeThresh):
            self.alive = 0

        self.genCount += 1

        if (random.randint(0, preAgeProbability) == 0):  # 1 in preAgeProb chance
            self.genCount -= random.randint(0, maxGenMod)  # to lower gen count

        if (random.randint(0, deAgeProbability) == 0):
            self.genCount += random.randint(0, maxGenMod)

        # update display number to match gen
        if (showGenCounts):
          self.genDisplay = athena2.render(str(self.genCount), True, GREENBLUE)

    def CalcMoveAmounts(self, x, y):
        self.dX = random.choice(stepListX)
        self.dY = random.choice(stepListY)

        return self.dX, self.dY


################
# PIXELS STUFF #
################

def Set_Pixel_Array():
    # list that pixels are stored in
    pixelsList = [[Pixel(x, y) for x in range(screen_width)]
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

            #####
            ############# X #############
            #####
            # if we are moving off screen (right)
            if (y * screenStepX + localDX >= screen_width * sFactor):
                localDX = 0

            # if we are moving off screen (left)
            if (x * screenStepX + localDX <= 0):
                localDX = 0


            ########
            # BLIT #
            ########

            # show them on screen
            if pixelsList[y][x].alive == 1:
                # pixels
                screen.blit(baseImg,
                            (((x * screenStepX) + offsetX) + localDX,
                             ((y * screenStepY) + offsetY) + localDY))
                
                # generation counters per pixel
                if (showGenCounts):
                  screen.blit(pixelsList[y][x].genDisplay, (((x * screenStepX) + offsetX) + localDX,
                             ((y * screenStepY) + offsetY) + localDY + textOffset))

def CalcPopulation():
    popCount = 0
    for y in range(screen_height):
        for x in range(screen_width):
            if pixelsList[y][x].alive == 1:
                popCount += 1

    return popCount

##################
# MENU FUNCTIONS #
##################

def BlitMenuObjects():
    screen.fill((211, 0, 128))

    # decor
    screen.blit(decorIMG1, (-titleX + 0.7 * titleX, titleY * 1.6))
    screen.blit(rotatedDecorIMG1, (titleX // 2 + 0.18 * titleX, -80))

    # text objects
    screen.blit(menuText, menuTextRect)


def BlitOptionsObjects():
    screen.fill((180, 100, 15))

    # text objects
    screen.blit(optionsText, optionsTextRect)

def PlayGame():
    screen.fill((211, 211, 211))

    # update all pixels
    Pixels()

    # text and counters
    if (showPopulation):
        screen.blit(popText, popTextRect)

        populationCount = CalcPopulation()

        popNumText = athena1.render(str(populationCount), True, RED)
        popNumTextRect = popNumText.get_rect()
        popNumTextRect.center = (titleX * 1.75, titleY * 3.8)

        screen.blit(popNumText, popNumTextRect)

########
# LOOP #
########

# Transform images as needed
rotatedDecorIMG1 = pygame.transform.rotate(decorIMG1, 210)

pixelsList = Set_Pixel_Array()

while True:
    # MAIN MENU
    if (playing == False):
      if (options == False):
        # main menu stuff + options
        BlitMenuObjects()
        playing = startBTN.draw(screen, "startBTN")
        options = optionsBTN.draw(screen, "optionsBTN")
        about = aboutBTN.draw(screen, "aboutBTN")

    # GAME
    if (playing):
        # make sure we don't slip into 
        # other menus (options...)
        options = False
        about = False
        PlayGame()

    # OPTIONS MENU
    if (options):
        BlitOptionsObjects()
        
        if (showGenCountsBTN.draw(screen, "genCountBTN")):
            showGenCounts = not showGenCounts
            # update clicked button imgs
            if (showGenCounts):
                showGenCountsBTN.update_img(genOnImg)
            if (not showGenCounts):
                showGenCountsBTN.update_img(genOffImg)

        if (showPopCountsBTN.draw(screen, "popCountBTN")):
            showPopulation = not showPopulation

            if (showPopulation):
                showPopCountsBTN.update_img(popOnImg)
            if (not showPopulation):
                showPopCountsBTN.update_img(popOffImg)

        playing = startBTN2.draw(screen, "startBTN")
    
    # ABOUT MENU
    if (about):
        pass
      
        

    # closing the window?
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()