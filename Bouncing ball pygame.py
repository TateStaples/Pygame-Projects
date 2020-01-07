# october 2019

import random
import pygame
pygame.init()

window = pygame.display.set_mode((500,500))
pygame.display.set_caption ('bouncing ball')

x = 250
y = 250
radius = 10
xspeed = random.randint(3, 8)
yspeed = random.randint(3, 8)
circle_color = (0, 255, 0)

run = True
while run:
    pygame.time.delay(10)  # wait 100 milliseconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    if x <= abs(xspeed)+radius or 500 - x <= abs(xspeed)+radius:
        print ('xspeed change', xspeed, xspeed*-1)
        xspeed *= -1
    if y <= abs(yspeed) or 500 - y <= abs(yspeed) + radius:
        yspeed *= -1
        #print ('bounce')

    x += xspeed
    y += yspeed

    window.fill((255,255,255))
    pygame.draw.circle(window, circle_color, (x, y), radius)
    pygame.display.update()
