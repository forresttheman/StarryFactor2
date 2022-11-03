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

###############
# SCREEN SIZE #
###############

screen_width = 20
screen_height = 20

screenStepX = 16
screenStepY = 16

sFactor = 17

realScreenWidth = screen_width * (sFactor + 1)
realScreenHeight = screen_height * (sFactor + 1)

#############
# MAIN MENU #
#############

playing = False
options = False

athena1 = pygame.font.Font("AthenaRustic.ttf", 32)
genDisplayFont = pygame.font.Font("AthenaRustic.ttf", 21)
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

oldAgeThresh = 60  # pixels die after this many gens


###########
# Classes #
###########


class Pixel():

    def __init__(self, iX, iY):
        self.iX = iX  # x index (in list)
        self.iY = iY  # y index

        self.genCount = 0
        self.genDisplay = genDisplayFont.render(str(self.genCount), True, RED)
      
        self.alive = random.randint(0, 1)  # random seed for each pixel
        self.diseased = False

        self.dY = 0
        self.dX = 0

    def Update(self):
        if (self.genCount >= oldAgeThresh):
            self.alive = 0

        self.genCount += 1

        if (random.randint(0, 150) == 0):  # 1 in 151 chance
            self.genCount -= random.randint(0, 5)  # to lower gen count

        # update display number to match gen
        self.genDisplay = athena1.render(str(self.genCount), True, BLACK)

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
            # BLIT #
            ########

            # show them on screen
            if pixelsList[y][x].alive == 1:
                screen.blit(baseImg,
                            (((x * screenStepX) + offsetX) + localDX,
                             ((y * screenStepY) + offsetY) + localDY))
                screen.blit(pixelsList[y][x].genDisplay, (((x * screenStepX) + offsetX) + localDX,
                             ((y * screenStepY) + offsetY) + localDY - textOffset))


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
    screen.fill((0, 0, 255))


########
# LOOP #
########

# Transform images as needed
rotatedDecorIMG1 = pygame.transform.rotate(decorIMG1, 210)

pixelsList = Set_Pixel_Array()

while True:
    if (playing == False & options == False):
        # main menu stuff + options
        BlitMenuObjects()
        playing = startBTN.draw(screen, "startBTN")
        options = optionsBTN.draw(screen, "optionsBTN")

    if (playing):
        screen.fill((211, 211, 211))
        Pixels()

    if (options):
        BlitOptionsObjects()
        playing = startBTN.draw(screen, "startBTN")

    # closing the window?
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()