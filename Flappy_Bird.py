import pygame
from random import *
pygame.init()

window_width = 500
window_height = 500
window = pygame.display.set_mode((window_width, window_height))

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (135,206,235)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)


def freeze():
    global game
    display("You lost", (50, 50), 100)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            # print(event, type(pygame.QUIT), pygame.KEYUP)
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYUP:
                print("i got here")
                del game
                game = FlappyBird()
                game.play_game()
       # print(1)


def display(msg, pos=(10, 10), font_size=20, color=BLACK):
    font = pygame.font.SysFont(pygame.font.get_default_font(), font_size)
    score_surface = font.render(msg, False, color)
    window.blit(score_surface, pos)


class Tube:
    tube_width = 60
    color = GREEN

    def __init__(self, x, gap):
        self.x = x
        self.height1 = randint(0, window_height-gap)
        self.height2 = window_height - self.height1 - gap
        self.gap = gap

    def tick(self, progression_speed):
        self.x -= progression_speed
        #print(self.x)

    def draw(self):
        tube1 = [self.x, 0, self.tube_width, self.height1]
        tube2 = [self.x, window_height - self.height2, self.tube_width, self.height2]
        pygame.draw.rect(window, self.color, tube1)
        pygame.draw.rect(window, self.color, tube2)
        return tube1, tube2

    def hit_tube(self, x, y):
        in_width = self.x <= x+Bird.radius and x-Bird.radius <= self.x + self.tube_width
        correct_y = y-Bird.radius < self.height1 or y+Bird.radius > window_height - self.height2
        return in_width and correct_y

    def is_off_screen(self):
        return self.x < -self.tube_width

    def __repr__(self):
        return f"Tube @ {self.x}: gap = {self.gap}"


class Bird:
    radius = 15
    flap_power = 20
    deceleration_rate = 3
    color = YELLOW

    def __init__(self):
        self.x = 50
        self.y = window_height//2
        self.y_vel = 0

    def flap(self):
        self.y_vel = self.flap_power

    def tick(self):
        self.y_vel -= self.deceleration_rate
        self.adjust_height()

    def adjust_height(self):
        self.y -= self.y_vel

    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)


class FlappyBird:
    space_between_tubes = 300

    def __init__(self):
        self.progression = 0
        self.progression_speed = 5
        self.tube_gap = 200
        self.score = 0
        self.bird = Bird()
        self.tubes = [Tube(-Tube.tube_width-1, 0)]
        self.generate_inital_tubes()
        self.game_running = True

    def play_game(self):
        while self.game_running:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    quit()
            self.tick()
            self.draw()

    def tick(self):
        for tube in reversed(self.tubes):
            tube.tick(self.progression_speed)
            if tube.hit_tube(self.bird.x, self.bird.y):
                print("You hit a tube")
                self.draw()
                freeze()
        self.manual_input()
        self.bird.tick()

        if self.bird.x > self.tubes[1].x:
            self.pass_through_tube()

        if self.bird.y > window_height - self.bird.radius:
            self.draw()
            print("You hit the ground")
            freeze()

    def pass_through_tube(self):
        self.tubes.pop(0)
        self.make_tube(self.tubes[-1].x + self.space_between_tubes)
        self.score += 1
        self.progression_speed += 1
        self.tube_gap -= 1

    def generate_inital_tubes(self):
        for i in range(2, 5):
            self.tubes.append(Tube(self.space_between_tubes*i, self.tube_gap))

    def make_tube(self, x):
        self.tubes.append(Tube(x, self.tube_gap))

    def manual_input(self):
        for event in pygame.event.get():
            if event == pygame.KEYDOWN:
                self.bird.flap()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.bird.flap()

    def draw_score(self):
        scr = f"Score: {self.score}"
        msg_color = RED
        font = pygame.font.SysFont(pygame.font.get_default_font(), 20)
        score_surface = font.render(scr, False, msg_color)
        window.blit(score_surface, (10, 10))


    def draw(self):
            window.fill(LIGHT_BLUE)
            for tube in self.tubes:
                tube.draw()
            self.bird.draw()
            self.draw_score()
            pygame.display.update()


if __name__ == '__main__':
    game = FlappyBird()
    game.play_game()