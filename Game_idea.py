import pygame
from math import *
pygame.init()

windowWidth = 800
windowHeight = 800
window = pygame.display.set_mode((windowWidth, windowHeight))

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (135, 206, 235)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


class Object:
    acceleration = 5
    radius = 10
    top_speed = 30

    def __init__(self):
        self.x = 100
        self.y = 100
        self.x_vel = 0
        self.y_vel = 0

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def draw(self):
        pygame.draw.circle(window, RED, (int(self.x), int(self.y)), self.radius)

    def update(self):
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_SPACE]:
            return
        x, y = pygame.mouse.get_pos()
        dx = x - self.x
        dy = y - self.y
        angle = atan(dy/dx)
        angle += pi if dx < 0 else 0
        self.x_vel += cos(angle) * self.acceleration
        self.y_vel += sin(angle) * self.acceleration

    def check_stuff(self):
        pass

    def tick(self):
        self.update()
        self.move()
        self.draw()



if __name__ == '__main__':
    thing = Object()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        window.fill(WHITE)
        thing.tick()
        pygame.display.update()