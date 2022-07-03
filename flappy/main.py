import random
import sys
from turtle import Screen
import pygame
from pygame.locals import *

# Global variables for the game
FPS = 30
SIZE = SCREENWIDTH, SCREENHEIGHT = 289, 511
SCREEN = pygame.display.set_mode(SIZE)
GROUNDY = SCREENHEIGHT * 0.8
SPRITES = {}
SOUNDS = {}
PLAYER = 'sprites/bird.png'
PIPE = 'sprites/pipe.png'
BACKGROUND = 'sprites/background.png'


def welcomeScreen():
    """
    shows welcome screen to the user
    """
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - SPRITES['player'].get_height()) / 2)
    messagex = int((SCREENWIDTH - SPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_RETURN):
                return
            else:
                SCREEN.blit(SPRITES['background'], (0, 0))
                SCREEN.blit(SPRITES['player'], (playerx, playery))
                SCREEN.blit(SPRITES['message'], (messagex, messagey))
                SCREEN.blit(SPRITES['base'], (basex, GROUNDY))
                myfont = pygame.font.SysFont('monospace', 16, bold=True)
                text = myfont.render("Press 'Space' to play", True, (0,0,0))
                SCREEN.blit(text, (35, SCREENHEIGHT * 0.9))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - SPRITES['player'].get_height()) / 2)
    basex = 0

    # generate pipes
    pipe1 = getRandomPipe()
    pipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': pipe1[0]['y']},
        {'x': SCREENWIDTH + 225 + (SCREENWIDTH / 2), 'y': pipe2[0]['y']}
    ]

    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': pipe1[1]['y']},
        {'x': SCREENWIDTH + 225 + (SCREENWIDTH / 2), 'y': pipe2[1]['y']}
    ]

    pipeVelx = -4

    playervely = -9
    playeracc = 1
    playermaxvel = 10
    playerflapvel = -8
    playerflapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if playery > 0:
                    playervely = playerflapvel
                    playerflapped = True
                    SOUNDS['wing'].play()

        # Game over
        game_over = isGameOver(playerx, playery, upperPipes, lowerPipes)
        if game_over:
            SOUNDS['hit'].play()
            return

        # checking for score
        for pipe in upperPipes:
            pipe_edge = pipe['x'] + SPRITES['pipe'][0].get_width() / 2
            playerMidPos = playerx + SPRITES['player'].get_width() / 2
            if pipe_edge <= playerMidPos < (pipe_edge + 4):
                score += 1
                print(score)
                SOUNDS['point'].play()

        # gravity on player
        if playervely < playermaxvel and not playerflapped:
            playervely += playeracc

        if playerflapped:
            playerflapped = False
        playerheight = SPRITES['player'].get_height()
        # flapping the player
        playery = playery + min(playervely, GROUNDY - playery - playerheight)

        # blitting images on screen
        SCREEN.blit(SPRITES['background'], (0, 0))
        SCREEN.blit(SPRITES['player'], (playerx, playery))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(SPRITES['base'], (basex, GROUNDY))

        # blitting score
        myfont = pygame.font.Font("sprites/SfDigitalReadoutHeavy-AwVg.ttf", 60)
        text = myfont.render(str(score), 1, (255, 255, 255))
        SCREEN.blit(
            text, ((SCREENWIDTH - text.get_width()) / 2, SCREENHEIGHT / 8))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

        # moving pipes
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelx
            lowerPipe['x'] += pipeVelx
        # adding new pipes when first pipe get out of screen
        if upperPipes[0]['x'] < -SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])


def getRandomPipe():
    """
    returns a list of two dictionaries 
    containing x and y values of upper and lower pipes
    """
    offset = int(SCREENHEIGHT / 4)
    x = SCREENWIDTH + 10
    Ph = SPRITES['pipe'][0].get_height()
    #y2 = random.randint(offset, int(SCREENHEIGHT - GROUNDY + 1.2 * offset))
    y2 = random.randint(offset + 40, int(GROUNDY - 40))
    y1 = Ph - y2 + offset
    pipe = [
        {'x': x, 'y': -y1},  # upper pipe
        {'x': x, 'y': y2}  # lower pipe
    ]
    return pipe


def isGameOver(playerx, playery, upperPipes, lowerPipes):
    if playery < 0 or playery + SPRITES['player'].get_height() >= GROUNDY:
        return True

    for pipe in upperPipes:
        pipeHeight = SPRITES['pipe'][0].get_height()
        if playery < pipeHeight + pipe['y'] and (pipe['x'] < playerx + SPRITES['player'].get_width() * 0.9 < pipe['x'] + SPRITES['pipe'][0].get_width() + SPRITES['player'].get_width()):
            return True

    for pipe in lowerPipes:
        if (playery + SPRITES['player'].get_height() > pipe['y']) and (pipe['x'] < playerx + SPRITES['player'].get_width() * 0.9 < pipe['x'] + SPRITES['pipe'][1].get_width() + SPRITES['player'].get_width()):
            return True
    return False


if __name__ == '__main__':
    pygame.init()  # initializing the pygame modules
    FPSCLOCK = pygame.time.Clock()  # setting the fps of the game
    pygame.display.set_caption('Flappy Bird by Ganga Singh')

    # laoding the base  of the game
    SPRITES['base'] = pygame.image.load('sprites/base.png').convert_alpha()
    # loading the message screen of the game
    SPRITES['message'] = pygame.image.load(
        'sprites/message.png').convert_alpha()
    # loading the pipe in the game
    SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    SPRITES['background'] = pygame.image.load(BACKGROUND).convert()

    #set title icon
    pygame.display.set_icon(SPRITES['player'])

    # game sounds
    SOUNDS['die'] = pygame.mixer.Sound('audio/die.wav')
    SOUNDS['hit'] = pygame.mixer.Sound('audio/hit.wav')
    SOUNDS['point'] = pygame.mixer.Sound('audio/point.wav')
    SOUNDS['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    SOUNDS['wing'] = pygame.mixer.Sound('audio/wing.wav')

    while True:
        welcomeScreen()
        mainGame()
