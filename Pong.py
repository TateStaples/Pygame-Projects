# october 2019

import pygame
import random

team1 = input('What is team one\'s name?   ')
team2 = input('What is team two\'s name?   ')

pygame.init()

windowWidth = 800
windowHeight = 500
window = pygame.display.set_mode((windowWidth, windowHeight))

winner = 'nobody'
ballwidth = 10
ballheight = 10
ball_x_speed = random.randint(9,15)
ball_y_speed = random.randint(-15, 15)
ball_accleration = 1.1

left_wall_x = 50
left_wall_y = 200
right_wall_x = windowWidth-50
right_wall_y = 200

wall_height = 100
wall_width = 10

wall_speed = 30

run = True
thing = True
right_score = 0
left_score = 0
while thing:
    run = True
    pygame.display.set_caption('Score: ' + team1 + ' = ' + str(left_score) + ', ' + team2 + ' = ' + str(right_score))
    ballx = 250
    bally = 150
    ball_x_speed = random.randint(9, 15)
    ball_y_speed = random.randint(-15, 15)
    while run:
        pygame.time.delay(10)  # wait 100 milliseconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                thing = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN] and windowHeight - right_wall_y >= wall_height + wall_speed:
            right_wall_y += wall_speed
        if keys[pygame.K_UP] and right_wall_y > 0:
            right_wall_y -= wall_speed
        if keys[pygame.K_w] and left_wall_y > 0:
            left_wall_y -= wall_speed
        if keys[pygame.K_s] and windowHeight - left_wall_y >= wall_height + wall_speed:
            left_wall_y += wall_speed

        if ballx + ball_x_speed <= left_wall_x + wall_width and bally + ball_y_speed >= left_wall_y and bally + ball_y_speed <= left_wall_y + wall_height:
            ball_x_speed *= -ball_accleration
            #print ('x reveresed 1')
        elif ballx + ball_x_speed + ballwidth >= right_wall_x and bally + ball_y_speed >= right_wall_y and bally + ball_y_speed <= right_wall_y + wall_height:
            ball_x_speed *= -ball_accleration
            #print('x reveresed 2', ballx)

        if bally + ball_y_speed <= 0:
            ball_y_speed *= -ball_accleration
            #print('y reveresed 1')
        elif bally + ballheight + ball_y_speed >= windowHeight:
            ball_y_speed *= -ball_accleration
            #print('y reveresed 2')

        ballx += ball_x_speed
        bally += ball_y_speed

        if ballx < left_wall_x:
            winner = 'right team'
            run = False
        elif ballx > right_wall_x:
            winner = 'left team'
            run = False

        window.fill((0,0,0))
        #draw ball
        pygame.draw.rect(window, (255,0,0), (ballx, bally, ballwidth, ballheight))
        #draw bouncers
        pygame.draw.rect(window, (255,255,255), (left_wall_x, left_wall_y, wall_width, wall_height))
        pygame.draw.rect(window, (255, 255, 255), (right_wall_x, right_wall_y, wall_width, wall_height))

        pygame.display.update()
    print ('The is winner is ' + winner)
    if winner == 'left team':
        left_score += 1
    elif winner == 'right team':
        right_score += 1
    pygame.time.delay((500))
pygame.quit()