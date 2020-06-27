import pygame
import random
import sys
import time
from pygame.locals import *

pygame.init()  # pygame initlise
screenheight = 600
screenwidth = 400
carXPeding = 25  # car distance to the road from x-axis
carYPeding = 22.5 # car distance to the slide from y-axis
roadX = {1: 0, 2: 100, 3: 200, 4: 300}  # road x distances
roadY = 0
slideX = 0
slideY = {1: 0, 2: 120, 3: 240, 4: 360, 5: 480} # screen height divider

# initialization
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption("Racing Game")
photos = {}
music = {}
clock = pygame.time.Clock()
text = pygame.font.SysFont(None, 60)
fps = 32

# photos loads
photos["road"] = pygame.image.load('photos/road.png').convert_alpha()
photos["welcome"] = pygame.image.load('photos/welcome.png').convert_alpha()
photos["player"] = pygame.image.load('photos/player.png').convert_alpha()
photos["car"] = (
    pygame.image.load("photos/car1.png").convert_alpha(),
    pygame.image.load("photos/car2.png").convert_alpha(),
    pygame.image.load("photos/car3.png").convert_alpha(),
    pygame.image.load("photos/car4.png").convert_alpha(),
    pygame.image.load("photos/car5.png").convert_alpha(),
    pygame.image.load("photos/car6.png").convert_alpha(),
    pygame.image.load("photos/car7.png").convert_alpha(),
    pygame.image.load("photos/car8.png").convert_alpha()
)

# musics loads
music["acc"] = pygame.mixer.Sound("sound/acc.wav")
music["crash"] = pygame.mixer.Sound("sound/crash.wav")

def welcome():
    '''
    display welcome screen
    :return:
    '''
    screen.blit(photos["welcome"], (0, 0))
    pygame.display.update()
    clock.tick(fps)

def mainGame():
    '''
    coding for main game
    :return:
    '''
    # initialization
    score = 0
    playerX = roadX[random.randrange(1, 5)] + carXPeding
    playerY = slideY[5] + carYPeding
    carDrive = False

    playerValY = 0
    playerValX = 0
    playerAccY = 25
    playerAccX = 25

    carValY = 4

    # create cars
    newCar1 = car_genrate()
    newCar2 = car_genrate()
    newCar3 = car_genrate()
    newCar4 = car_genrate()
    newCar5 = car_genrate()

    cars_list = [
        [{'x': i['x'], 'y': i['y']+carYPeding, 'car': i['car'], 'flag' : i['flag']} for i in newCar1], # ({'x' = x1, 'y':-y , 'car'= car1})
        [{'x': i['x'], 'y': i['y']-slideY[2]+carYPeding, 'car': i['car'], 'flag' : i['flag']} for i in newCar2],#({'x' = x1, 'y':-y , 'car'= car1},{'x'=x2
        [{'x': i['x'], 'y': i['y']-slideY[3]+carYPeding, 'car': i['car'], 'flag' : i['flag']} for i in newCar3],
        [{'x': i['x'], 'y': i['y']-slideY[4]+carYPeding, 'car': i['car'], 'flag' : i['flag']} for i in newCar4],
        [{'x': i['x'], 'y': i['y']-slideY[5]+carYPeding, 'car': i['car'], 'flag' : i['flag']} for i in newCar5],
    ]

    # game loop
    while True:
        # keys function
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RIGHT and playerX < screenwidth-photos['car'][0].get_width():
                    playerValX = playerAccX
                    music["acc"].play()
                    carDrive = True

                if event.key == K_LEFT and playerX > 0:
                    playerValX = -playerAccX
                    music["acc"].play()
                    carDrive = True

                if event.key == K_UP and playerY > 0:
                    playerValY = -playerAccY
                    music["acc"].play()
                    carDrive = True

                if event.key == K_DOWN and playerY < screenheight-photos['car'][0].get_height():
                    playerValY = playerAccY
                    carDrive = True

        # moves player or cars
        playerX = playerX + playerValX
        playerY = playerY + playerValY

        for i in cars_list:
            for j in i:
                j['y']+=carValY

        # car is not drive
        if carDrive:
            carDrive = False

        if not carDrive:
            playerValX = 0
            playerValY = 0

        # addition or delete of cars
        if screenheight - photos['car'][0].get_width() - carYPeding + 5 > cars_list[0][0]['y'] > screenheight - photos['car'][0].get_width() - carYPeding:
            newCar = car_genrate()
            cars_list.append([{'x': i['x'], 'y': i['y'], 'car': i['car'], 'flag' : i['flag']} for i in newCar])

        if cars_list[0][0]['y'] > screenheight:
            cars_list.__delitem__(0)

        # calculation of scores
        hscore = 0
        with open("heigh_score.txt", 'r') as f:
            hscore = int(f.read())
        for i in cars_list:
            for j in i:
                if j['y'] > playerY + photos['player'].get_height()/2 and j['flag'] == 0:
                    score+=1
                    j['flag'] = 1
        if score>hscore:
            hscore = score
        display_score = text.render(str(score), True, (0, 255, 0))
        heigh_score = text.render(f"H.S. : {hscore}", True, (0,255,0) )

        # check car crash or not
        testcase = isCollide(playerX, playerY, cars_list)
        if testcase:
            time.sleep(4)
            gameOver(score, hscore)
            return

        # display
        screen.blit(photos["road"], (roadX[1], roadY))
        screen.blit(photos["road"], (roadX[2], roadY))
        screen.blit(photos["road"], (roadX[3], roadY))
        screen.blit(photos["road"], (roadX[4], roadY))
        for i in cars_list:
            for j in i:
                screen.blit(photos["car"][j['car']], (j['x'], j['y']))
        screen.blit(display_score, (5,5))
        screen.blit(heigh_score, (200,5))
        screen.blit(photos["player"], (playerX, playerY))
        pygame.display.update()
        clock.tick(fps)

def isCollide(playerX, playerY, cars_list):
    '''
    crash function
    :param playerX:
    :param playerY:
    :param cars_list:
    :return:
    '''
    for i in cars_list:
        for j in i:
            if playerY < j['y'] < playerY + int(photos["player"].get_height())/2 and abs(playerX - j['x']) < 51:
                music["acc"].stop()
                music["crash"].play()
                return True
    return False

def car_genrate():
    '''
    genrate a new car
    :return:
    '''
    road_list = [1, 2, 3, 4]
    car_list = [0, 1, 2, 3, 4, 5, 6, 7]
    y = int(photos['car'][0].get_height())
    x = carXPeding + roadX[random.choice(road_list)]
    car = random.choice(car_list)
    cars = [
        {'x' : x, 'y' : -y, 'car' : car, 'flag' : 0}
    ]
    return cars

def gameOver(score, hscore):
    '''
    display of game over page
    :return:
    '''
    with open("heigh_score.txt", "w") as f:
        f.write(str(hscore))

    display = text.render("GAME OVER", True, (255, 0, 0))
    display_score = text.render(f"Your Score is : {score}", True, (0, 0, 255))
    heighscore = text.render(f"Heigh score is : {hscore}", True, (0,255,0))

    screen.fill((255,255,255))
    screen.blit(display, (70, (screenheight-120)/2))
    screen.blit(display_score, (30 , (screenheight-120)/2 + 70))
    screen.blit(heighscore, (5, (screenheight-120)/2 + 140))
    pygame.display.update()
    clock.tick(fps)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return

if __name__ == '__main__':
    while True:
        welcome() # display welcome page
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    mainGame() # main game start