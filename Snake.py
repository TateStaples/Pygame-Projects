import random
import pygame
from resources import freeze_display
pygame.init()

# created jan 2, 2020
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


class Snake:
    head_val = 2

    def __init__(self, board):
        r, c = index_2d(board, self.head_val)
        self.head = (r, c)
        self.body = []
        self.just_ate = False
        self.eat_apple()
        self.eat_apple()

    def move(self, action):
        for i, body_seg in enumerate(reversed(self.body), start=1):
            if i == 1 and self.just_ate:
                continue
            if i < len(self.body) - 1:
                self.body[-i] = self.body[-(i+1)]
            else:
                self.body[-i] = self.head
        r, c = self.head
        if action == "up":
            r -= 1
        elif action == "down":
            r += 1
        elif action == "right":
            c += 1
        elif action == "left":
            c -= 1
        self.head = (r, c)
        self.just_ate = False

    def eat_apple(self):
        self.just_ate = True
        if len(self.body) > 0:
            self.body.append(self.body[-1])
        else:
            self.body.append(self.head)


class SnakeGame:
    head_val = 2
    body_val = 1
    apple_val = 3
    draw_delay = 50

    def __init__(self, w=20, l=20):
        self.width = w
        self.length = l
        self.board = None
        self.snek = None
        self.create_board()

    def play_game(self, user=None):
        user = self.manual if user is None else user
        run = True
        while run:
            pygame.time.delay(self.draw_delay)
            if self.board is not None:
                self.draw_board()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
            if not run or self.board is None:
                break
            self.action = user()
            self.update_board()

    def make_apple(self):
        x, y = random.randint(0, self.width - 1), random.randint(0, self.length - 1)
        while self.board[x][y] != 0:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.length - 1)
        self.board[x][y] = self.apple_val

    def create_board(self):
        self.board = [[0 for i in range(self.width)] for j in range(self.length)]
        self.board[self.length // 2][self.width // 2] = self.head_val
        self.snek = Snake(self.board)
        self.make_apple()

    def update_board(self, b=None):
        action = self.action
        new_pos = self.get_next_pos(action)
        if new_pos is None:
            return None
        r, c = new_pos
        if self.board[r][c] == self.apple_val:  # if ate
            self.snek.eat_apple()
            self.make_apple()
        elif len(self.snek.body) > 0:
            r, c = self.snek.body[-1]  # get the back of the body
            self.board[r][c] = 0
        else:
            r, c = self.snek.head
            self.board[r][c] = 0
        if self.get_next_pos(action) is None:
            print("you lost")
            self.over()
        self.snek.move(action)
        if len(self.snek.body) > 0:
            r2, c2 = self.snek.body[0]
            self.board[r2][c2] = self.body_val
        r1, c1 = self.snek.head
        self.board[r1][c1] = self.head_val
        return self.board

    def manual(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            return "left"
        if keys[pygame.K_RIGHT]:
            return "right"
        if keys[pygame.K_UP]:
            return "up"
        if keys[pygame.K_DOWN]:
            return "down"
        try:
            return self.action
        except AttributeError:
            return "right"

    def get_next_pos(self, action):
        r, c = index_2d(self.board, self.head_val)
        try:
            if action == "up":
                r -= 1
            elif action == "down":
                r += 1
            elif action == "right":
                c += 1
            elif action == "left":
                c -= 1
            if r < 0 or c < 0:
                return None
            if self.board[r][c] == self.body_val:
                return None
        except IndexError:
            return None
        return r, c

    def __repr__(self):
        string = ""
        for row in self.board:
            string += row + "\n"
        return string

    def draw_board(self):
        box_width = window_width // self.width
        box_height = window_height // self.length
        window.fill(BLACK)
        for r, row in enumerate(self.board):
            for c, spot in enumerate(row):
                color = GREEN
                if spot == 0:
                    color = BLACK
                if spot == self.apple_val:
                    color = RED
                pygame.draw.rect(window, color, [c * box_width, r * box_height, box_width, box_height])

    def over(self):
        freeze_display(100)
        quit()


class SimulatedSnake(SnakeGame):
    apple_score = 1000
    survive_score = 5
    hit_wall = -1000
    hit_body = -1000

    def score_board(self, action):
        if self.board is None:
            return -10000
        r, c = index_2d(self, self.head_val)
        try:
            if action == "up":
                r -= 1
            elif action == "down":
                r += 1
            elif action == "right":
                c += 1
            elif action == "left":
                c -= 1
            if r < 0 or c < 0:
                return self.hit_wall
            if self.board[r][c] == self.body_val:
                return self.hit_body
        except IndexError:
            return self.hit_wall
        apple = index_2d(self.board, self.apple_val)
        if apple == (r, c):
            return self.apple_score
        return self.survive_score

    def simulate_game(self, get_action_function):
        self.create_board()
        played_situations = []
        run = True
        while run and self.board is not None:
            action = get_action_function(self.board)
            reward = self.score_board(action)
            if reward == self.apple_score:
                played_situations = []
            elif (self.snek.head, self.snek.body) in played_situations:
                # print("loop")
                break
            else:
                played_situations.append((self.snek.head, self.snek.body))
            self.update_board(action)


def index_2d(board, val):
    for r, row in enumerate(board):
        if val in row:
            return r, row.index(val)
    return None


if __name__ == '__main__':
    window_width = 500
    window_height = 500
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("snake game")
    ScreenColor = BLACK
    game = SnakeGame()
    game.play_game()


