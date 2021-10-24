import pygame
import pygame.freetype
from enum import Enum
from random import randint

global food
global foodLocation
global snakeDirection
global snake


class Mode(Enum):
    HARD = 0
    MEDIUM = 1
    EASY = 2


difficultyOptions = {
    Mode.HARD: 5,
    Mode.MEDIUM: 10,
    Mode.EASY: 25
}

# Modify this to change difficulty, size of map
difficulty = Mode.EASY


class Speed(Enum):
    FAST = 100
    NORMAL = 250
    SLOW = 500


speedOptions = {
    Speed.FAST: 100,
    Speed.NORMAL: 250,
    Speed.SLOW: 500
}

# MODIFY THIS TO CHANGE THE SPEED OF THE SNAKE
speedSetting = Speed.NORMAL


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


pygame.init()
pygame.freetype.init()

GAME_FONT = pygame.freetype.SysFont("calibri", 24)

screenSize = 500
totalSquare = difficultyOptions[difficulty]
frameDuration = speedOptions[speedSetting]
totalSquareOnBoard = totalSquare ** 2
squareWidth = int(screenSize / totalSquare)
snakeSize = 0
currentScreen = 0
speedMod = frameDuration / 25
numEaten = 0


def resetGame():
    global snakeDirection
    global snake
    global food
    global snakeSize
    global numEaten
    snakeDirection = Direction.SOUTH
    snake = []
    food = False
    snake.append([0, 1])
    snake.append([0, 0])
    snakeSize = 2
    numEaten = 0


def winGame():
    global currentScreen
    currentScreen = 3


def spawnFood():
    global foodLocation
    global food
    global snakeSize
    print("size " + str(snakeSize))
    rand = randint(0, totalSquareOnBoard - snakeSize)
    num = 0
    food = True

    for i in range(0, totalSquare):
        for j in range(0, totalSquare):
            if [i, j] not in snake:
                if num == rand:
                    foodLocation = [i, j]
                    return
                num += 1
    print("could not find")


def drawSnake():
    global food
    global foodLocation
    global snakeSize
    if snakeSize == totalSquareOnBoard:
        winGame()

    if not food:
        spawnFood()
    for s in snake:
        pygame.draw.rect(screen, (0, 0, 0), ((s[0] * squareWidth) + 1, (s[1] * squareWidth) + 1, squareWidth - 2,
                                             squareWidth - 2), 0)
        pygame.draw.rect(screen, (0, 0, 0), ((foodLocation[0] * squareWidth) + 3, (foodLocation[1] * squareWidth) + 3,
                                             squareWidth - 6, squareWidth - 6), 0)


def increaseLength():
    global numEaten
    global snakeSize
    if numEaten < 20:
        numEaten += 1
    s = snake[snakeSize - 1]
    if snake[snakeSize - 2][0] > s[0]:
        snake.append([s[0] - 1, s[1]])
    elif snake[snakeSize - 2][0] < s[0]:
        snake.append([s[0] + 1, s[1]])
    elif snake[snakeSize - 2][1] < s[1]:
        snake.append([s[0], s[1] + 1])
    elif snake[snakeSize - 2][1] > s[1]:
        snake.append([s[0], s[1] - 1])
    snakeSize += 1


def endGame():
    global currentScreen
    currentScreen = 2


def moveSnake():
    global food
    global snakeSize
    for i in range(snakeSize - 1, -1, -1):
        if i == 0:
            if snakeDirection == Direction.NORTH:
                snake[i][1] -= 1
            elif snakeDirection == Direction.EAST:
                snake[i][0] += 1
            elif snakeDirection == Direction.SOUTH:
                snake[i][1] += 1
            elif snakeDirection == Direction.WEST:
                snake[i][0] -= 1
            if snake[i] == foodLocation:
                food = False
                increaseLength()
        else:
            snake[i][0] = snake[i - 1][0]
            snake[i][1] = snake[i - 1][1]
        if snake[i][0] < 0 or \
                snake[i][0] >= totalSquare or \
                snake[i][1] < 0 or \
                snake[i][1] >= totalSquare:
            endGame()
            return
    headLocation = snake[0]
    for i in range(1, snakeSize):
        if headLocation == snake[i]:
            endGame()
            return


# Set up the drawing window
screen = pygame.display.set_mode([squareWidth * totalSquare, squareWidth * totalSquare])
pygame.display.set_caption("Snake")
screen.fill((255, 255, 255))

resetGame()

drawSnake()
currentTicks = pygame.time.get_ticks()
pygame.display.flip()

running = True
turning = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif currentScreen == 1 and event.type == pygame.KEYDOWN and not turning:
            if event.key == pygame.K_LEFT:
                turning = True
                if snakeDirection == Direction.NORTH:
                    snakeDirection = Direction.WEST
                elif snakeDirection == Direction.EAST:
                    snakeDirection = Direction.NORTH
                elif snakeDirection == Direction.SOUTH:
                    snakeDirection = Direction.EAST
                elif snakeDirection == Direction.WEST:
                    snakeDirection = Direction.SOUTH
            elif event.key == pygame.K_RIGHT:
                turning = True
                if snakeDirection == Direction.NORTH:
                    snakeDirection = Direction.EAST
                elif snakeDirection == Direction.EAST:
                    snakeDirection = Direction.SOUTH
                elif snakeDirection == Direction.SOUTH:
                    snakeDirection = Direction.WEST
                elif snakeDirection == Direction.WEST:
                    snakeDirection = Direction.NORTH
        elif currentScreen == 0 and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            resetGame()
            currentScreen = 1
        elif currentScreen == 2 and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            resetGame()
            currentScreen = 1
        elif currentScreen == 3 and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            resetGame()
            currentScreen = 1

    if currentScreen == 0:
        screen.fill((255, 255, 255))
        GAME_FONT.render_to(screen, (50, 50), "Welcome to Snake, to start press enter", (0, 0, 0))
        pygame.display.flip()
    elif currentScreen == 1:
        if pygame.time.get_ticks() - currentTicks > frameDuration - (speedMod * numEaten):
            currentTicks = pygame.time.get_ticks()
            screen.fill((255, 255, 255))
            moveSnake()
            drawSnake()
            turning = False
            pygame.display.flip()
    elif currentScreen == 2:
        screen.fill((255, 255, 255))
        GAME_FONT.render_to(screen, (50, 50), "You have lost, enter to play again", (0, 0, 0))
        pygame.display.flip()
    elif currentScreen == 3:
        screen.fill((255, 255, 255))
        GAME_FONT.render_to(screen, (50, 50), "You have won, enter to play again", (0, 0, 0))
        pygame.display.flip()

pygame.quit()
