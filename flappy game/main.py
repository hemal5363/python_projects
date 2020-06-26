import random
import pygame
from pygame.locals import *
import sys


# global variabl
FPS = 32
SCREENWIDTH = 600
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'Gallery/sprites/bird.png'
BACKGROUND = 'Gallery/sprites/background.png'
PIPE = 'Gallery/sprites/pipe.png'


def welcomeScreen():
    """
    Shows welcome images on the screen
    """

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    # messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    # messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['message'], (0,0 ))    
                # SCREEN.blit(GAME_SPRITES['pipe'][0], (0,0 ))    
                # SCREEN.blit(GAME_SPRITES['pipe'][1], (0,600-int(GAME_SPRITES['pipe'][1].get_height()) ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                    
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = 0
    playerMaxVelY = 10
    # playerMinVelY = 0
    playerAccY = 1

    playerFlapAccv = -10 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            return     

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()

        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False    

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)
        
        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()

        Xoffset = (SCREENWIDTH - width)/2
        
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset,SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery>= GROUNDY - int(GAME_SPRITES['player'].get_height())  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    
        if(playery < pipeHeight + pipe['y'] and (playerx + int(GAME_SPRITES['player'].get_width()))>pipe['x'] and (playerx <= (pipe['x'] + GAME_SPRITES['pipe'][0].get_width()))): #abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['die'].play()
            return True
            
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and (playerx + int(GAME_SPRITES['player'].get_width()))>pipe['x'] and (playerx <= (pipe['x'] + GAME_SPRITES['pipe'][0].get_width())): #abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['die'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(GAME_SPRITES["pipe"][0].get_height()))
    pipeX = SCREENWIDTH
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird by Hemal")
    
    GAME_SPRITES["numbers"] = (
        pygame.image.load("Gallery/sprites/0.png").convert_alpha(),
        pygame.image.load("Gallery/sprites/1.png").convert_alpha(),
        pygame.image.load("Gallery/sprites/2.png").convert_alpha(),
        pygame.image.load("Gallery/sprites/3.png").convert_alpha(),
        pygame.image.load("Gallery/sprites/4.png").convert_alpha(),
        pygame.image.load("Gallery/sprites/5.png").convert_alpha(),
        pygame.image.load("Gallery/sprites/6.png").convert_alpha(),
        pygame.image.load("Gallery/sprites/7.png").convert_alpha(),
        pygame.image.load("Gallery/sprites/8.png").convert_alpha(),
        pygame.image.load("Gallery/sprites/9.png").convert_alpha(),
    )

    GAME_SPRITES["message"] = pygame.image.load("Gallery/sprites/welcome.png").convert_alpha()
    GAME_SPRITES["base"] = pygame.image.load("Gallery/sprites/base.png").convert_alpha()
    GAME_SPRITES["pipe"] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    GAME_SPRITES["background"] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES["player"] = pygame.image.load(PLAYER).convert_alpha()
    
    GAME_SOUNDS["die"] = pygame.mixer.Sound("Gallery/audio/die.wav")
    GAME_SOUNDS["hit"] = pygame.mixer.Sound("Gallery/audio/hit.wav")
    GAME_SOUNDS["point"] = pygame.mixer.Sound("Gallery/audio/point.wav")
    GAME_SOUNDS["swoosh"] = pygame.mixer.Sound("Gallery/audio/swoosh.wav")
    GAME_SOUNDS["wing"] = pygame.mixer.Sound("Gallery/audio/wing.wav")

    while True:
        welcomeScreen()
        mainGame()