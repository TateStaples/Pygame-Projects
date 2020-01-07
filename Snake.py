# october 5, 2019

# record = 151 (at delay of 30)
#TODO: add a pause and restart feature
import pygame
pygame.init()

import random

delay = 300

windowWidth = 500
windowHeight = 500

window = pygame.display.set_mode((windowWidth, windowHeight))
#pygame.display.set_caption("snake game")
ScreenColor = (0, 0, 0)

SnakeSpeed = 50
SnakeX = windowWidth//2
SnakeY = windowHeight//2
SnakeWidth = 49
SnakeHeight = 49
SnakeDirection = 'right'
SnakeColor = (0, 255, 0)

applewidth = 50
appleheight = 50
appleColor = (255,0,0)
appleX = random.randint(0, windowWidth - SnakeSpeed)//SnakeSpeed * SnakeSpeed
appleY = random.randint(0, windowHeight - SnakeSpeed)//SnakeSpeed * SnakeSpeed

things = [(SnakeX, SnakeY)]

window.fill(ScreenColor)
pygame.draw.rect(window, SnakeColor, (things[0][0], things[0][1], SnakeWidth, SnakeHeight))
pygame.draw.rect(window, appleColor, (appleX, appleY, applewidth, appleheight))
pygame.display.update()
pygame.time.delay(500)


def create_board():
    w, l = windowWidth//SnakeSpeed, windowHeight//SnakeSpeed
    board = [[0 for i in range(w)] for j in range(l)]
    #print(things)
    for x, y in things:
        r, c = x//SnakeSpeed, y//SnakeSpeed
        board[r][c] = 1
    apple_r, apple_c = appleX//SnakeSpeed, appleY//SnakeSpeed
    board[apple_r][apple_c] = 3
    head_r, head_c = SnakeX//SnakeSpeed, SnakeY//SnakeSpeed
    board[head_r][head_c] = 2
    return board


def write_board(file):
    board = create_board()
    for row in board:
        for spot in row:
            file.write(str(spot) + ",")
    direction_vals = {"left": 0, "up": 1, "right": 2, "down": 3}
    file.write(str(direction_vals[SnakeDirection]))
    file.write("\n")


def decrypt_file(file):
    solution_translator = {0: [1, 0, 0, 0], 1: [0, 1, 0, 0], 2: [0, 0, 1, 0], 3: [0, 0, 0, 1]}
    situations = []
    solutions = []
    for line in file:
        line = line.strip
        info = line.split(',')
        solution = solution_translator[int(info[-1])]
        situation = (int(i) for i in info[:-1])
        situations.append(solution)
        situations.append(situation)
    return situations, solutions

file = open("Files/snake_data", 'w')
run = True
while run:
    pygame.display.set_caption("snake game: length = " + str(len(things)))
    pygame.time.delay(delay)
    occupied = False
    TastyApple = False
    pygame.time.delay(10)  # wait 100 milliseconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        pygame.time.delay(200)
        while True:
            pygame.time.delay(100)
            if keys[pygame.K_SPACE]:
                break
    if keys[pygame.K_DOWN]:
        SnakeDirection = 'down'
    if keys[pygame.K_UP]:
        SnakeDirection = 'up'
    if keys[pygame.K_RIGHT]:
        SnakeDirection = 'right'
    if keys[pygame.K_LEFT]:
        SnakeDirection = 'left'

    if SnakeDirection == 'right':
        for object in things:
            if object[0] == SnakeX + SnakeSpeed and object[1] == SnakeY: #and SnakeX != object[0] and SnakeY != object[1]:
                occupied = True
            else:
                if SnakeX + SnakeSpeed == appleX and SnakeY == appleY:
                    TastyApple = True
        if SnakeX + SnakeSpeed >= windowWidth or SnakeX + SnakeSpeed < 0:
            occupied = True
    elif SnakeDirection == 'left':
        for object in things:
            if object[0] == SnakeX - SnakeSpeed and object[1] == SnakeY: #and SnakeX != object[0] and SnakeY != object[1]:
                occupied = True
            else:
                if SnakeX - SnakeSpeed == appleX and SnakeY == appleY:
                    TastyApple = True
        if SnakeX - SnakeSpeed > windowWidth or SnakeX - SnakeSpeed < 0:
            occupied = True
    elif SnakeDirection == 'up':
        for object in things:
            if object[0] == SnakeX and object[1] == SnakeY - SnakeSpeed: #and SnakeX != object[0] and SnakeY != object[1]:
                occupied = True
            else:
                if SnakeX == appleX and SnakeY - SnakeSpeed == appleY:
                    TastyApple = True
        if SnakeY - SnakeSpeed > windowHeight or SnakeY - SnakeSpeed < 0:
            occupied = True
    else:
        for object in things:
            if object[0] == SnakeX and object[1] == SnakeY + SnakeSpeed: #and SnakeX != object[0] and SnakeY != object[1]:
                occupied = True
            else:
                if SnakeX == appleX and SnakeY + SnakeSpeed == appleY:
                    TastyApple = True
        if SnakeY + SnakeSpeed >= windowHeight or SnakeY + SnakeSpeed < 0:
            occupied = True
    if not occupied:
        #print ('got here 1')
        if TastyApple:
            bonus = things[0::-1]
            #print('got here apple eaten')
        reverse = things[::-1]
        for count, seg in enumerate(reverse):
            if reverse[count] != things[0]:
                reverse[count] = reverse[count+1]
                #print('got here snake moved')
            else:
                #print(len(things))
                if SnakeDirection == 'right':
                    reverse[count] = (seg[0] + SnakeSpeed, seg[1])
                elif SnakeDirection == 'left':
                    reverse[count] = (seg[0] - SnakeSpeed, seg[1])
                elif SnakeDirection == 'up':
                    reverse[count] = (seg[0], seg[1] - SnakeSpeed)
                else:
                    reverse[count] = (seg[0], seg[1] + SnakeSpeed)
        things = reverse[::-1]
        if TastyApple:
            things.append(bonus[0])
            #print ('things', things, 'reverse', things[::-1])
            while (appleX, appleY) in things:
                appleX = random.randint(0, windowWidth - applewidth)//SnakeSpeed * SnakeSpeed
                appleY = random.randint(0, windowHeight - appleheight)//SnakeSpeed * SnakeSpeed
            #print (appleX,appleY)
        #print(things)
    else:
        print("Snake ran into something")
        break
    SnakeX = things[0][0]
    SnakeY = things[0][1]
    window.fill(ScreenColor)
    for seg in things:
        pygame.draw.rect(window, SnakeColor, (seg[0], seg[1], SnakeWidth, SnakeHeight))
    pygame.draw.rect(window, appleColor, (appleX, appleY, applewidth, appleheight))
    pygame.display.update()
    write_board(file)
pygame.time.delay(1000)
print('quitting')
print('Your Snake was', str(len(things)), 'long.')
pygame.quit()