#pip instal pygame 
import pygame 
import random
import sys
from pygame.locals import *

#screen dimensions acc to classic mobile look
SCREENWIDTH = 289                                                                                                       
SCREENHEIGHT=520

#fixixng the maximmu frames per second
FPS=40

#creating instance of screen
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))

#static y for ground layer
GROUNDY= SCREENHEIGHT*0.8

#dit contaninig sprites addresses relative to current directory
GAME_SPRITES={}
GAME_SOUNDS={}

#global png holders
PLAYER='gallery/sprites/bird.png'
BACKGROUND= 'gallery/sprites/background.png'
PIPE='gallery/sprites/pipe.png'


def welcomeScreen():
    """
    Shows welcome images on the screen with flappy bird logo
    """
    
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==pygame.KEYDOWN and (event.key==pygame.K_SPACE or event.key == pygame.K_UP):
                return
            #otherwise blit the welcome screen waititng for user event
            else:
                FPSCLOCK.tick(FPS)
                SCREEN.blit(GAME_SPRITES['welcome'], (0,0) ) 
                pygame.display.update()
                

def mainGame():
    """
        main logic for the game
    """
    #initializizng score 
    score = 0
    #initializng player(BIRD) cooridnates
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    #static x for base(GROUND)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #  List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]
    #initializizng pipe velocity to create a moving illusion
    pipeVelX = -4
    #initial velocity to go upwards
    playerVelY = -9
    #limit of velocity in downward dir
    playerMaxVelY = 10
    #gravity for game
    playerAccY = 1
    # velocity while flapping
    playerFlapAccv = -8 
    playerFlapped = False # It is true only when the bird is flapping

    #game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()   #quiting pygame screen
                sys.exit()      #closing the program
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                if playery > 0:                          #if bird is in the screen
                    playerVelY = playerFlapAccv
                    playerFlapped = True                #changing the flap state
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            #blitting the gameover screen till user press any key and then return to main menu or else close the window
            while True:
                for event in pygame.event.get():
                    if  event.type == pygame.KEYDOWN :
                        return
                    if event.type == pygame.QUIT:
                        pygame.quit()   #quiting pygame screen
                        sys.exit()      #closing the program
                SCREEN.blit(GAME_SPRITES['gameover'], (0, 0))       
                pygame.display.update()
                FPSCLOCK.tick(FPS)

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
        
        #  blit our sprites now
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
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    """
    function to check collision by analysing the mid pos of pipe and its height with respect to bird pos
    """
    #if it touches bottom or top
    if playery> GROUNDY - 25  or playery<0: 
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe




if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock() #instance to clock for the game
    #setting caption for fun
    pygame.display.set_caption('Flappy Bird by Himanshu')
    #setting sprites for the numbers 0-9
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )
    #for welcome screen,gameover screen,ground(base),pipe(in both straigh and rotated fashion)
    GAME_SPRITES['welcome'] =pygame.image.load('gallery/sprites/welcome.png').convert_alpha()
    GAME_SPRITES['gameover'] =pygame.image.load('gallery/sprites/gameover.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    #infinite loop to switch between welcome screen and game window
    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 





