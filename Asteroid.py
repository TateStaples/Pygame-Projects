# this is my version of the classic Asteroids game
# sometime in October
__author__ = "Tate Staples"

import pygame as pg
import random
import math
pg.font.init()
pg.init()

windowHeight = 500
windowWidth = 500
window = pg.display.set_mode((windowWidth, windowHeight))
windowColor = (0, 0, 0)
pg.display.set_caption('Asteroids!')
delay = 10

Asteroid_Wait_counter = 200
asteroids = []

bullets = []
amount_of_bullets = 5

score = 0


def rotate_polygon(list_of_points, rotation, center_x, center_y):
    x_cordinates = []
    y_cordinates = []

    for x, y in list_of_points:
        x_cordinates.append(x-center_x)
        y_cordinates.append(y-center_y)
    point_matrix = []
    point_matrix.append(x_cordinates)
    point_matrix.append(y_cordinates)

    # centroid_matrix = [[], []]
    # # center_x = sum(x_cordinates)/len(x_cordinates)
    # # center_y = sum(y_cordinates)/len(y_cordinates)
    # for i in range(len(x_cordinates)):
    #     centroid_matrix[0].append(center_x)
    #     centroid_matrix[1].append(center_y)

    rotation = math.radians(rotation)
    rotation_matrix = [
        [math.cos(rotation), -math.sin(rotation)],
        [math.sin(rotation), math.cos(rotation)]
    ]
    #
    # list1 = []
    # list2 = []
    # for entry in range(len(x_cordinates)):  # thing1 = P-C
    #     list1.append(point_matrix[0][entry] - centroid_matrix[0][entry])
    #     list2.append(point_matrix[1][entry] - centroid_matrix[1][entry])
    # thing1 = []
    # thing1.append(list1)
    # thing1.append(list2)
    # # print('thing1', thing1)

    result = [[], []]
    for i in range(len(x_cordinates)):  # result = R * thing1
        result[0].append(0)
        result[1].append(0)
    for i in range(len(rotation_matrix)):
        # iterate through columns of Y
        for j in range(len(point_matrix[0])):
            # iterate through rows of Y
            for k in range(len(point_matrix)):
                result[i][j] += rotation_matrix[i][k] * point_matrix[k][j]
    # print('result', result)

    # list1 = []
    # list2 = []
    # for i in range(len(x_cordinates)):  # final = result + C
    #     list1.append(result[0][i] + centroid_matrix[0][i])
    #     list2.append(result[1][i] + centroid_matrix[1][i])

    # print ('lists', (list1,list2))
    polygon = []
    print(result)
    for x, y in zip(result[0], result[1]):
        polygon.append((x + center_x, y + center_y))

    # print('OG', list_of_points)
    # print('C', centroid_matrix)
    # print('R', rotation_matrix)
    # print('P', point_matrix)
    # print('poly', polygon)
    return polygon


def draw_display(lives, score):
    message = 'You have ' + str(lives) + ' lives left. \n Your score is ' + str(score)
    text_color = (255, 255, 255)
    text_font = 'Comic Sans MS'
    text_size = 25
    font = pg.font.SysFont(text_font, text_size)
    text_surface = font.render(message, False, text_color)

    window.blit(text_surface, (10, 10))


class Asteroid:
    Asteroid_Sizes = [50, 30, 10]
    Asteroid_Top_Speed = 1
    Split_angle = 45

    def __init__(self, original):
        if original:
            position = random.choice(
                [
                    (random.randint(0, windowWidth), 0),
                    (random.randint(0,windowWidth), windowHeight),

                    (0, random.randint(0, windowHeight)),
                    (windowWidth, random.randint(0, windowHeight))
                ])
            self.x, self.y = position
            self.size = random.choice(self.Asteroid_Sizes)
            self.speed = random.randint(1, self.Asteroid_Top_Speed)
            self.heading = random.randint(1,360)
            self.draw()

    def draw(self):  # circle
        pg.draw.circle(window, (255, 255, 255), (int(self.x//1), int(self.y//1)), self.size, 1)

    def asteroid_split(self):
        a = Asteroid(False)
        a.x = self.x
        a.y = self.y
        a.heading = self.heading + self.Split_angle
        a.speed = self.speed
        a.size = self.Asteroid_Sizes[self.Asteroid_Sizes.index(self.size) + 1]
        b = Asteroid(False)
        b.x = self.x
        b.y = self.y
        b.speed = self.speed
        b.heading = self.heading - self.Split_angle
        b.size = self.Asteroid_Sizes[self.Asteroid_Sizes.index(self.size) + 1]

        asteroids.append(a)
        asteroids.append(b)

        asteroids.pop(asteroids.index(self))
        del self

    def move(self):
        global score
        for count, bullet in enumerate(bullets):
            if math.sqrt((self.x - bullet.x)**2+(self.y - bullet.y)**2) <= self.size:
                if self.size != 10:
                    self.asteroid_split()
                else:
                    asteroids.pop(asteroids.index(self))
                    #del self
                bullets.pop(count)
                score += 1
                break
        self.x += math.sin(math.radians(self.heading)) * self.speed
        self.y += math.cos(math.radians(self.heading)) * self.speed

        if self.x < 0:
            self.x += windowWidth
        elif self.x > windowWidth:
            self.x -= windowWidth
        if self.y < 0:
            self.y += windowHeight
        elif self.y > windowHeight:
            self.y -= windowHeight


class Spaceship:
    color = (0, 255, 0)
    heading = 0
    turn_speed = 10
    speed = 0
    max_speed = 25
    boost_power = .5
    friction_rate = .99
    lives = 3
    x = windowWidth/2
    y = windowHeight/2
    x_speed = 0
    y_speed = 0

    def draw(self):
        ship_shape = [
            (self.x, self.y + 5),
            (self.x - 3, self.y - 5),
            (self.x, self.y),
            (self.x + 3, self.y - 5)
        ]
        print(self.heading)
        polygon = rotate_polygon(ship_shape, self.heading*-1, self.x, self.y)
        new_poly = []

        for x, y in polygon:
            #x = int((x+.5)//1)
            #y = int((y+.5)//1)
            new_poly.append((x,y))
        #print(new_poly)
        pg.draw.polygon(window, self.color, new_poly)

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

        self.x_speed *= self.friction_rate
        self.y_speed *= self.friction_rate

        for asteroid in asteroids:  # check for asteroid impact
            if math.sqrt((self.x - asteroid.x)**2 + (self.y - asteroid.y)**2) < asteroid.size:
                self.lives -= 1
                self.reset()
        if self.x < 0:
            self.x += windowWidth
        elif self.x > windowWidth:
            self.x -= windowWidth
        if self.y < 0:
            self.y += windowHeight
        elif self.y > windowHeight:
            self.y -= windowHeight

    def user_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.heading += self.turn_speed
            if self.heading > 360:
                self.heading -= 360
        elif keys[pg.K_RIGHT]:
            self.heading -= self.turn_speed
            if self.heading < 0:
                self.heading += 360
        if keys[pg.K_UP]:
            if self.x_speed**2 + self.y_speed**2 < self.max_speed:
                self.x_speed += math.sin(math.radians(self.heading)) * self.boost_power
                self.y_speed += math.cos(math.radians(self.heading)) * self.boost_power
        if keys[pg.K_SPACE]:
            # TODO: add a stall counter
            if len(bullets) < amount_of_bullets:
                bullets.append(Bullet())

    def reset(self):
        self.x = windowWidth/2
        self.y = windowHeight/2
        self.speed = 0


ship = Spaceship()


class Bullet:
    Bullet_size = 2
    Bullet_color = (255, 0, 0)
    Bullet_Speed = 8

    def __init__(self):
        self.x = ship.x
        self.y = ship.y
        self.heading = ship.heading

    def draw(self):
        pg.draw.circle(window, self.Bullet_color, (int(self.x//1), int(self.y//1)), self.Bullet_size)

    def move(self):
        self.x += math.sin(math.radians(self.heading)) * self.Bullet_Speed
        self.y += math.cos(math.radians(self.heading)) * self.Bullet_Speed

        if self.x < 0 or self.x > windowWidth:
            bullets.pop(bullets.index(self))
            del self
        elif self.y < 0 or self.y > windowHeight:
            bullets.pop(bullets.index(self))
            del self

def main():
    global Asteroid_Wait_counter
    run = True
    Asteroid_Stall_counter = 0
    while run:
        # TODO: add a display
        pg.time.delay(delay)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
        ship.user_input()

        Asteroid_Stall_counter += 1
        if Asteroid_Stall_counter >= Asteroid_Wait_counter:
            Asteroid_Stall_counter = 0
            rock = Asteroid(True)
            asteroids.append(rock)
            if Asteroid_Wait_counter > 5:
                Asteroid_Wait_counter -= 2

        for bullet in bullets:
            bullet.move()
        for asteroid in asteroids:
            asteroid.move()
        ship.move()
        if ship.lives < 0:
            print('you have no more lives')
            run = False
            break

        window.fill(windowColor)
        for asteroid in asteroids:
            asteroid.draw()
        for bullet in bullets:
            bullet.draw()
        ship.draw()
        draw_display(ship.lives, score)
        pg.display.update()


if __name__ == '__main__':
    main()

    # this is so the app doesn't quit when over
    pg.display.update()
    while True:
        pg.time.delay(1000)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()