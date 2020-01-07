# nov / december 2019
import pygame
import math
pygame.init()

windowWidth = 500
windowHeight = 500

window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("3d Graphics")

vFOV = 1.5  # vertical range of view (in radians)
hFOV = 1.5  # horizontal angle of view (in radians)

# use radians
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (135, 206, 235)
GREEN = (0, 255, 0)
BROWN = (165, 42, 42)
BLACK = (0, 0, 0)

ScreenColor = BLACK


def adjust_perspective(objective, player):  # I don't think that this works
    ob_x, ob_y = objective
    my_x, my_y = player
    return ob_x - my_x, ob_y - my_y


# converts from normal cords to screen cords
def convert_to_screen(cords):
    global windowWidth, windowHeight
    x, y = cords
    new_x = windowWidth/2 + x
    new_y = windowHeight/2 + y
    return new_x, new_y


# finds where on screen a point in 3d space would be displayed on 2d screen
def find_location(cord, player_info):
    global hFOV, vFOV, windowWidth, windowHeight
    perspective, player = player_info
    x1, y1, z1 = player
    x2, y2, z2 = cord
    x = x2 - x1
    y = y1 - y2
    z = z2 - z1 + 0.001  # todo prevent flipping
    z_width = math.tan(hFOV/2) * z * 2
    z_height = math.tan(vFOV/2) * z * 2
    x_angle = x/z_width * hFOV
    y_angle = y / z_height * vFOV
    if z < 0 and False:
        x_angle *= -1
        y_angle *= -1
    x_angle, y_angle = adjust_perspective((x_angle, y_angle), perspective)
    x_cord = x_angle/hFOV * windowWidth
    y_cord = y_angle/vFOV * windowHeight
    player_view = adjust_perspective((x_cord, y_cord), perspective)
    return convert_to_screen(player_view)


class Polygon:
    def __init__(self, list_of_points, color):
        self.points = list_of_points
        self.color = color

    def draw(self, player):
        coverted_list = []
        for point in self.points:
            coverted_list.append(find_location(point, player))
        pygame.draw.polygon(window, self.color, coverted_list)


class RectPrism:
    def __init__(self, cords, color):
        cord1, cord2, cord3 = cords
        x1, y1, z1 = cord1
        x2, y2, z2 = cord2
        x3, y3, z3 = cord3
        self.x_vals = {x1, x2, x3}
        self.y_vals = {y1, y2, y3}
        self.z_vals = {z1, z2, z3}
        self.color = color

    def draw(self, player):
        x1, x2 = tuple(self.x_vals)
        y1, y2 = tuple(self.y_vals)
        z1, z2 = tuple(self.z_vals)
        for x in self.x_vals:
            cords = []
            cords.append((x, y1, z1))
            cords.append((x, y1, z2))
            cords.append((x, y2, z2))
            cords.append((x, y2, z1))
            poly = Polygon(cords, self.color)
            poly.draw(player)
        for y in self.y_vals:
            cords = []
            cords.append((x1, y, z1))
            cords.append((x1, y, z2))
            cords.append((x2, y, z2))
            cords.append((x2, y, z1))
            poly = Polygon(cords, self.color)
            poly.draw(player)
        for z in self.z_vals:
            cords = []
            cords.append((x1, y1, z))
            cords.append((x2, y1, z))
            cords.append((x2, y2, z))
            cords.append((x1, y2, z))
            poly = Polygon(cords, self.color)
            poly.draw(player)


class Player:
    def __init__(self, start_cords):
        self.x, self.y, self.z = start_cords
        self.x_view = 0  # allows for looking around
        self.y_view = 0
        self.test = RectPrism(
            (
                (-5, 0, 10),
                (5, 10, 10),
                (5, 10, 20)  # todo figure out why the depth looks wrong
            ),
            GREEN
        )
        self.ground = Polygon(
            [
                (-1000, 1, -0),
                (-1000, 1, 100),
                (1000, 1, 100),
                (1000, 1, -0),
            ], BROWN
        )
        self.sky = Polygon(
            [
                (1000, 1000, 100),
                (1000, 0, 100),
                (-1000, 0, 100),
                (-1000, 1000, 100)
            ], LIGHT_BLUE
        )
        self.run_game()

    def run_game(self):
        run = True
        while run:
            pygame.time.delay(10)
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
                self.z -= 1
            if keys[pygame.K_UP]:
                self.z += 1
            if keys[pygame.K_RIGHT]:
                self.x += 5
            if keys[pygame.K_LEFT]:
                self.x -= 5
            if keys[pygame.K_SPACE]:
                self.y = 40
            if keys[pygame.K_w]:  # change this
                if self.y_view > -math.pi/2:
                    self.y_view -= .10
            if keys[pygame.K_s]:  # change this
                if self.y_view < math.pi / 2:
                    self.y_view += .10
            if keys[pygame.K_d]:  # change this (turning in a full circle does a weird)
                self.x_view += .10
            if keys[pygame.K_a]:  # change this
                self.x_view -= .10

            if self.y >= 20:
                self.y -= 1

            window.fill(ScreenColor)
            my_info = ((self.x_view, self.y_view), (self.x, self.y, self.z))
            self.sky.draw(my_info)
            self.ground.draw(my_info)
            self.test.draw(my_info)
            pygame.display.update()


main = Player((0, 20, 0))
