# Implement various solving methods for Sodoku (buggy)
# Decemeber 22, 2019
__author__ = "Tate Staples"

import pygame as pg
import random
pg.init()

windowHeight = 630
windowWidth = 630
window = pg.display.set_mode((windowWidth, windowHeight))

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (135, 206, 235)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
window.fill(WHITE)


def create_board():
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append(Box((i, j)))
        board.append(row)
    return board

def create_locked(amount):
    for i in range(amount):
        is_valid = False
        box = None
        while not is_valid:
            r, c = random.randint(0, 8), random.randint(0, 8)
            print(r, c)
            box = board[r][c]
            is_valid = box.value == 0
        options = box.get_possiblities()
        box.value = random.choice(options)
        box.possiblities = [box.value]
        box.locked = True
        box.draw_val(BLUE)
        box.update()

def establish_possiblities():
    for row in board:
        for box in row:
            box.set_options()

def get_row(r):
    return board[r]

def get_col(c):
    return [row[c] for row in board]

def get_box(r, c):
    row = r // 3
    col = c // 3
    return [board[3*row + i][3*col + j] for i in range(3) for j in range(3)]

def filter(list1, list2):
    for item in list1[::-1]:
        if item in list2:
            list1.remove(item)
    return list1

def place_locked():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

        keys = pg.key.get_pressed()
        if keys[pg.K_1]:
            r, c = get_square(pg.mouse.get_pos())
            box = board[r][c]
            box.locked = True
            box.value = 1
            box.draw()
        if keys[pg.K_2]:
            r, c = get_square(pg.mouse.get_pos())
            box = board[r][c]
            box.locked = True
            box.value = 2
            box.draw()
        if keys[pg.K_3]:
            r, c = get_square(pg.mouse.get_pos())
            box = board[r][c]
            box.locked = True
            box.value = 3
            box.draw()
        if keys[pg.K_4]:
            r, c = get_square(pg.mouse.get_pos())
            box = board[r][c]
            box.locked = True
            box.value = 4
            box.draw()
        if keys[pg.K_5]:
            r, c = get_square(pg.mouse.get_pos())
            box = board[r][c]
            box.locked = True
            box.value = 5
            box.draw()
        if keys[pg.K_6]:
            r, c = get_square(pg.mouse.get_pos())
            box = board[r][c]
            box.locked = True
            box.value = 6
            box.draw()
        if keys[pg.K_7]:
            r, c = get_square(pg.mouse.get_pos())
            box = board[r][c]
            box.locked = True
            box.value = 7
            box.draw()
        if keys[pg.K_8]:
            r, c = get_square(pg.mouse.get_pos())
            box = board[r][c]
            box.locked = True
            box.value = 8
            box.draw()
        if keys[pg.K_9]:
            r, c = get_square(pg.mouse.get_pos())
            box = board[r][c]
            box.locked = True
            box.value = 9
            box.draw()

def get_square(cords):
    x, y = cords
    return x // Box.box_width, y // Box.box_height

def draw_boxes():
    for row in board:
        for box in row:
            box.draw()
    box_width = windowWidth // 3
    box_height = windowHeight // 3
    for row in range(3):
        for col in range(3):
            pg.draw.rect(window, BLACK, [col*box_width, row*box_height, box_width, box_height], 5)
    pg.display.update()

def over():
    draw_boxes()
    print("over")
    while True:
        pg.time.delay(100)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

def impossible():
    print("The board cannot be solved")
    over()
    quit()


class Box:
    box_width = windowWidth // 9
    box_height = windowHeight // 9

    def __init__(self, pos):
        self.value = 0
        self.position = pos
        self.possiblities = []
        self.tried = []
        self.locked = False
        self.parent = None
        self.children = []
        self.options = []

    def get_possiblities(self):
        options = [i for i in range(1, 10)]
        r, c = self.position
        for box in get_row(r):
            if box.value in options:
                options.remove(box.value)
        for box in get_col(c):
            if box.value in options:
                options.remove(box.value)
        for box in get_box(r, c):
            if box.value in options:
                options.remove(box.value)
        return options

    def is_vaild(self, val):
        return val in self.possiblities

    def __repr__(self):
        return f"Val: {self.value}, pos: {self.position}"

    def set_options(self):
        self.possiblities = self.get_possiblities()
        self.options = filter(self.possiblities, self.tried)
        return self.options

    def draw_box(self, color=WHITE, outline=BLACK):
        r, c = self.position
        x, y = c*self.box_width, r*self.box_height
        pg.draw.rect(window, color, [x+3, y+3, self.box_width-6, self.box_height-6])
        pg.draw.rect(window, outline, [x, y, self.box_width, self.box_height], 1)

    def draw_val(self, color=BLACK):
        if self.value == 0: return
        r, c = self.position
        x, y = c * self.box_width+3, r * self.box_height
        msg = str(self.value)
        text_font = 'Comic Sans MS'
        text_size = self.get_text_size(self.box_width, len(msg))
        font = pg.font.SysFont(text_font, text_size)
        score_surface = font.render(msg, False, color)
        window.blit(score_surface, (x, y))

    def update(self):
        r, c = self.position
        x, y = c * self.box_width, r * self.box_height
        pg.display.update([x, y, self.box_width, self.box_height])

    def draw(self, fill_color=WHITE):
        self.draw_box(fill_color)
        if self.locked:
            self.draw_val(BLUE)
        else:
            self.draw_val()
        self.update()

    # todo add guesses for top right

    @staticmethod
    def get_text_size(w, len):
        width_per_char = w / len
        return int(width_per_char * 72 / 48)


class Backtrace:

    def __init__(self, draw):
        self.index = (0, 0)
        establish_possiblities()
        while not self.filled():
            # pg.time.delay(100)
            if draw:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        quit()
            r, c = self.index
            box = board[r][c]
            options = filter(box.possiblities, box.tried)
            if not box.locked and len(options) > 0:
                val = random.choice(options)
                self.remove_tried()
                box.value = val
                box.tried.append(val)
                self.reestablish_options()
                if draw:
                    box.draw()

            if len(options) == 0 and not box.locked:
                box.value = 0
                self.reestablish_options()
                self.index = self.previous_index(self.index)
                if draw:
                    box.draw()
            elif box.locked:
                if self.should_advance(self.index):
                    self.index = self.next_index(self.index)
                else:
                    self.index = self.previous_index(self.index)
            else:
                self.index = self.next_index(self.index)

    def remove_tried(self):
        spot = self.index
        while spot != (8, 8):
            spot = self.next_index(spot)
            r, c = spot
            board[r][c].tried = []

    def should_advance(self, index):
        r, c = index
        box = board[r][c]
        if box.locked:
            return self.should_advance(self.next_index(index))
        options = filter(box.possiblities, box.tried)
        return len(options) > 0

    def reestablish_options(self):
        r, c = self.index
        for box in get_row(r):
            box.possiblities = box.get_possiblities()
        for box in get_col(c):
            box.possiblities = box.get_possiblities()
        for box in get_box(r, c):
            box.possiblities = box.get_possiblities()

    @staticmethod
    def previous_index(location):
        r, c = location
        return (r, c-1) if c > 0 else (r-1, len(board[r-1])-1) if r > 0 else over()

    @staticmethod
    def next_index(location):
        r, c = location
        return (r, c+1) if c < len(board[r])-1 else (r+1, 0) if r+1 < len(board) else over()

    @staticmethod
    def valid_index(location):
        r, c = location
        return 0 <= r < len(board) and 0 <= c < len(board[r])

    @staticmethod
    def filled():
        for row in board:
            for box in row:
                if box.value == 0:
                    return False
        return True


class SmartSolve:
    current_parent = None

    def __init__(self, draw):
        self.draw = draw
        establish_possiblities()
        while not self.filled():
            # pg.time.delay(100)
            box = self.get_next()
            if box is None:
                self.break_path(self.current_parent)
                self.current_parent.value = 0
                # self.make_guess(self.current_parent)
            else:
                box.parent = self.current_parent if self.current_parent != box else box.parent
                if self.current_parent is not None:
                    self.current_parent.children.append(box)
                self.make_guess(box)
                if self.draw:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            quit()


    @staticmethod
    def get_next():
        best_box = None
        for row in board:
            for box in row:
                if box.value == 0:
                    if len(box.options) <= 1:
                        return box
                    if best_box is None or len(box.options) < len(best_box.options):
                        best_box = box
        # print(len(best_box.options))
        return best_box

    def break_path(self, box):
        for child in box.children:
            if child == box: continue
            child.parent = None
            child.value = 0
            if self.draw:
                child.draw()
            child.tried = []
            self.break_path(child)
        self.reestablish_options(box)
        box.children = []

    def make_guess(self, box):
        if box is None:
            impossible()

        options = box.set_options()
        if len(options) == 0:
            # print(box)
            try:
                self.break_path(box.parent)
                box.parent.value = 0
            except AttributeError:
                impossible()
            # self.make_guess(box.parent)
        elif len(options) == 1:  # make a certain move
            val = options[0]
            box.value = val
            box.tried.append(val)
            self.reestablish_options(box)
            if self.draw:
                box.draw()
        else:  # if a guess is made
            self.current_parent = box
            val = random.choice(options)
            box.value = val
            box.tried.append(val)
            self.reestablish_options(box)
            if self.draw:
                box.draw()

    @staticmethod
    def reestablish_options(start_box):
        r, c = start_box.position
        for box in get_row(r):
            box.set_options()
        for box in get_col(c):
            box.set_options()
        for box in get_box(r, c):
            box.set_options()


    @staticmethod
    def filled():
        return Backtrace.filled()


if __name__ == '__main__':
    board = create_board()
    draw_boxes()
    create_locked(5)
    SmartSolve(True)
    over()
