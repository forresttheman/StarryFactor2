import pygame, sys
from pygame.locals import QUIT
import time
import random
import button
from pygame import mixer

mixer.init()
pygame.init()
pygame.display.set_caption("Life In Turmoil")

# time 
FRAME_RATE = 60
clock = pygame.time.Clock()

# music - audio files
gameMusic = mixer.music.load("audio/GameMusic.mp3")

# colors
BLACK = (0, 0, 0)
RED = (150, 0, 0)
TEAL = (0, 100, 100)

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

# are we in this menu
options = False

# settings
showGenCounts = False
showPopulation = True

# text
optionsText = athena1.render("OPTIONS OPTIONS OPTIONS OPTIONS", True, RED)

optionsTextRect = optionsText.get_rect()
optionsTextRect.center = (titleX, titleY * 0.5)

# buttons - images
genOnImg = pygame.image.load("img/button/genCountOn.png")
genOffImg = pygame.image.load("img/button/genCountOff.png")

popOnImg = pygame.image.load("img/button/popCountOn.png")
popOffImg = pygame.image.load("img/button/popCountOff.png")

# volume button stuff
audioHighImg = pygame.image.load("img/audio/audioFull.png")
audioMedImg = pygame.image.load("img/audio/audioMed.png")

audioLowImg = pygame.image.load("img/audio/audioLow.png")
audioOffImg = pygame.image.load("img/audio/audioOff.png")


# buttons - definitions
startBTN2 = button.Button(titleX * 1.4, titleY * 3.4, startButtonImg, buttonScale * 0.6)

showGenCountsBTN = button.Button(titleX // 3, titleY *0.8, genOffImg, buttonScale * 8)
showPopCountsBTN = button.Button(titleX // 3, titleY * 2.7, popOffImg, buttonScale * 8)

# volume btn
volumeBTN = button.Button(titleX * 0.22, titleY * 1.5, audioHighImg, buttonScale * 1.2)


# audio settings (adjust in options)
volumeValueList = [0.2, 0.15, 0.1, 0, 0.1, 0.15, 0.2] # highest to lowest to highest
volumeImgList = [audioHighImg, audioMedImg, audioLowImg, audioOffImg, audioLowImg, audioMedImg, audioHighImg]

# set default volume(highest)
mixer.music.set_volume(volumeValueList[0])

# how many times we have pressed button
# start at 0 (-1 + 1 = 0)
volumeBTN_counter = -1


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

gameMusicCounter = 0


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

# keep track of population!
populationCount = 0

# probability ( (1/num) + 1 ) that gen counters of pixels
# decrease 
deAgeProbability = 100

# increase
preAgeProbability = 100

# pixels die after this many gens
oldAgeThresh = 10

# maximum modifier to gen counter
maxGenMod = oldAgeThresh // 2

###########
# Classes #
###########

class Pixel():
    def __init__(self, iX, iY, img):
        self.iX = iX  # x index (in list)
        self.iY = iY  # y index


        self.genCount = 0
        self.genDisplay = athena2.render(str(self.genCount), True, RED)
      
        self.alive = random.randint(0, 1)  # random seed for each pixel
        self.diseased = False

        # movement - deltas
        self.dY = 0
        self.dX = 0

        # collision
        self.img = img
        self.rect = self.img.get_rect()

    def Update(self):
        # move this pixel's rectangle
        self.dX, self.dY = self.CalcMoveAmounts()
        self.rect.move(self.dX, self.dY)

        # are we dying of old age?
        if (self.genCount >= oldAgeThresh):
            self.alive = 0

        # manipulate generation counters
        self.genCount += 1

        if (random.randint(0, preAgeProbability) == 0):  # 1 in preAgeProb chance
            self.genCount -= random.randint(0, maxGenMod)  # to lower gen count

        if (random.randint(0, deAgeProbability) == 0):
            self.genCount += random.randint(0, maxGenMod)

        # update display number to match gen
        if (showGenCounts):
          self.genDisplay = athena2.render(str(self.genCount), True, TEAL)

    def CalcMoveAmounts(self):
        self.dX = random.choice(stepListX)
        self.dY = random.choice(stepListY)

        return self.dX, self.dY


################
# PIXELS STUFF #
################

def Set_Pixel_Array():
    # list that pixels are stored in
    pixelsList = [[Pixel(x, y, baseImg) for x in range(screen_width)]
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
            localDX, localDY = pixelsList[y][x].CalcMoveAmounts()

            
            ############# Y #############
            
            # if we are moving off screen (down)
            if (y * screenStepY + localDY >= screen_height * sFactor):
                localDY = 0

            # if we are moving off screen (up)
            if (y * screenStepY + localDY <= 0):
                localDY = 0

            
            ############# X #############
            
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
                screen.blit(pixelsList[y][x].img,
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

    # animations
    # asyncio.run(PlayAnimsTask())

def BlitOptionsObjects():
    screen.fill((120, 176, 255))

    # text objects
    screen.blit(optionsText, optionsTextRect)

def PlayGame():
    screen.fill((211, 211, 211))

    global gameMusicCounter
    
    # music
    if (gameMusicCounter == 0):
        mixer.music.load("audio/GameMusic.mp3")
        mixer.music.play(-1, 0, 150)

    gameMusicCounter += 1

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

# music - main menu
mixer.music.load("audio/MenuMusic.mp3")
mixer.music.play(-1, 0, 150)

# forever loop
while True:
    # MAIN MENU #
    if (playing == False):
      if (options == False):
            # main menu stuff
            BlitMenuObjects()

            # buttons
            playing = startBTN.draw(screen, "startBTN")
            options = optionsBTN.draw(screen, "optionsBTN")
            about = aboutBTN.draw(screen, "aboutBTN")

    # GAME #
    if (playing):
        # make sure we don't slip into other menus (options...)
        options = False
        about = False

        PlayGame()

    # OPTIONS MENU #
    if (options):
        # objects
        BlitOptionsObjects()
        
        # buttons - toggles
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

        # buttons - click
        playing = startBTN2.draw(screen, "startBTN")

        # buttons - volume
        changeVolume = volumeBTN.draw(screen, "volumeBTN")

        if (changeVolume):
            volumeBTN_counter += 1

            if (volumeBTN_counter < len(volumeValueList)):
                volumeBTN.update_img(volumeImgList[volumeBTN_counter])
            else:
                volumeBTN_counter = 0
            
            mixer.music.set_volume(volumeValueList[volumeBTN_counter])
    
    # ABOUT MENU #
    if (about):
        pass
      
    # closing the window?
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # update display and clock
    clock.tick(FRAME_RATE)
    pygame.display.update()