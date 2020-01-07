# october / november 2019

import pygame as pg
from random import choice

pg.init()

# TODO: modify game to accept modular teleports
# TODO: add power-ups
# TODO: stop centering (done-ish)
# TODO: check if Inky is reflecting correctly

# 19x20 - https://www.arcade-museum.com/game_detail.php?game_id=8782

level_2 = [
    #0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # row 0
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # row 1
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],  # row 2
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],  # row 0
    [1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, ],  # row 0
    [],  # row 0
    [],  # row 0
    [],  # row 0
    [],  # row 0
    [],  # row 0
    [],  # row 0
    [],  # row 0
    [],  # row 0
    [],  # row 0
    [],  # row 0
    [],  # row 0
    [],  # row 0
    [],  # row 0
    [],  # row 0
    []   # row 0
]

board = [
    #0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # row 0 (top)
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # row 1
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],  # row 2
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # row 3
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],  # row 4
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],  # row 5
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],  # row 6
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],  # row 7
    [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],  # row 8 (middle)
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],  # row 9
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],  # row 10
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # row 11
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],  # row 12
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],  # row 13
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],  # row 14
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],  # row 15
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],  # row 16
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # row 17
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]   # row 18 (bottom)
]
delay = 1

windowHeight = 700
windowWidth = 600
windowColor = (0, 0, 0)
window = pg.display.set_mode((windowWidth, windowHeight))
pg.display.set_caption("Pac-Man")

square_width = windowWidth/len(board[0])
square_height = windowHeight/len(board[0])
animation_timer = 0
animation_wait = 2
play_direction = 1

lives = 3
score = 0
level = 1

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (135,206,235)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

ghost_colors = [LIGHT_BLUE, PINK, ORANGE, RED]

tokens = []
for row_count, row in enumerate(board):
    for col_count, col in enumerate(row):
        if col == 0:
            tokens.append((col_count, row_count))

ghosts = []
Pinky_lead = 2
Inky_reflect_point = 1
Clyde_scare_dis = 4
chase = True


def display(lives, score, level):
    message = 'Score: ' + str(score) + '. You are on level ' + str(level) + '.'
    text_color = (255, 255, 255)
    text_font = 'Comic Sans MS'
    text_size = 25
    font = pg.font.SysFont(text_font, text_size)
    score_surface = font.render(message, False, text_color)

    window.blit(score_surface, (10, 10))

    x = 10 + square_width
    y = windowHeight - square_height/2
    for i in range(lives):
        pg.draw.circle(window, YELLOW, (int(x),int(y)), int(square_width/2))
        x += 10 + square_width


def pathfind(start_cordinates, target_coordinates):
    # TODO: allow parameters for start directions
    # TODO: update this for the smarter path-finding
    x = start_cordinates[0]
    y = start_cordinates[1]

    checked = [start_cordinates]

    right = False
    left = False
    up = False
    down = False

    right_branch = [(x + 1, y)]
    left_branch = [(x - 1, y)]
    up_branch = [(x, y-1)]
    down_branch = [(x, y+1)]


    if board[y][x + 1] == 0:
        right = True
        # print('right')
    if board[y][x - 1] == 0:
        left = True
        # print('left')
    if board[y - 1][x] == 0:
        up = True
        # print('up')
    if board[y + 1][x] == 0:
        down = True
        # print('down')

    def check(list):
        new_spots = []
        for col, row in list:
            # TODO: change this to be modular
            try:
                if row == 8 and col == 18:
                    new_spots.append((0, 8))
                elif board[row][col + 1] == 0:
                    new_spots.append((col+1, row))
            except:
                pass
            try:
                if row == 8 and col == 0:
                    new_spots.append((18, 8))
                elif board[row][col - 1] == 0:
                    new_spots.append((col-1, row))
            except:
                pass
            try:
                if board[row + 1][col] == 0:
                    new_spots.append((col, row+1))
            except:
                pass
            try:
                if board[row - 1][col] == 0:
                    new_spots.append((col, row-1))
            except:
                pass
        # print(new_spots)
        return new_spots

    intial = target_coordinates
    if target_coordinates[0] > len(board[0])-1:
        target_coordinates = (len(board[0])-1, target_coordinates[1])
    elif target_coordinates[0] < 0:
        target_coordinates = (0, target_coordinates[1])
    if target_coordinates[1] > len(board)-1:
        target_coordinates = (target_coordinates[0], len(board)-1)
    elif target_coordinates[1] < 0:
        target_coordinates = (target_coordinates[0], len(board) - 1)

    if board[target_coordinates[1]][target_coordinates[0]] != 0:
        blocked = True
        block_checked = [target_coordinates]
        block_list = [target_coordinates]
        block_count = 0
        while blocked:
            thing = []
            for point in block_list:
                x, y = point
                if (x+1, y) not in block_checked:
                    thing.append((x+1, y))

                if (x-1, y) not in block_checked:
                    thing.append((x-1, y))

                if (x, y+1) not in block_checked:
                    thing.append((x, y+1))
                    # print('append down')

                if (x, y-1) not in block_checked:
                    thing.append((x, y-1))

            block_list = []
            # print('thing', thing)
            for tup in thing:
                a, b = tup

                if a > len(board[0])-1 or a < 0 or b > len(board)-1 or b < 0:
                    pass
                elif board[b][a] == 0:
                    target_coordinates = tup
                    blocked = False
                    # print('i got here')
                    break
                else:
                    block_list.append(tup)
                block_checked.append(tup)
            block_count += 1

            if block_count > 100 or len(block_list) == 0:
                print('block list timed out')
                print(start_cordinates, target_coordinates)
                break

    count = 0
    checking = True
    while checking:
        if left:
            left_new = check(left_branch)
            left_branch = []
            for tup in left_new:
                if tup == target_coordinates:
                    return 'left'
                elif tup not in checked:
                    checked.append(tup)
                    left_branch.append(tup)
            if len(left_branch) == 0:
                left = False
        if right:
            right_new = check(right_branch)
            right_branch = []
            for tup in right_new:
                if tup == target_coordinates:
                    return 'right'
                elif tup not in checked:
                    checked.append(tup)
                    right_branch.append(tup)
            if len(right_branch) == 0:
                right = False
        if up:
            up_new = check(up_branch)
            up_branch = []
            for tup in up_new:
                if tup == target_coordinates:
                    return 'up'
                elif tup not in checked:
                    checked.append(tup)
                    up_branch.append(tup)
            if len(up_branch) == 0:
                up = False
            # print(up_branch)
        if down:
            down_new = check(down_branch)
            down_branch = []
            for tup in down_new:
                if tup == target_coordinates:
                    return 'down'
                elif tup not in checked:
                    checked.append(tup)
                    down_branch.append(tup)
            if len(down_branch) == 0:
                down = False
            # print(down_branch)
        count += 1
        if count == 100:
            print('the path-finding timed out')
            print(start_cordinates, target_coordinates)
            print ('left, right, up, down', left, right, up, down)
            break


class PacMan:
    speed = 7

    def __init__(self):
        self.direction = 'right'
        self.row = 13
        self.col = 9
        self.center()

    def user_input(self):
        keys = pg.key.get_pressed()
        current_direction = self.direction
        if keys[pg.K_LEFT]:
            self.direction = 'left'
        elif keys[pg.K_RIGHT]:
            self.direction = 'right'
        elif keys[pg.K_UP]:
            self.direction = 'up'
        elif keys[pg.K_DOWN]:
            self.direction = 'down'
        if self.collision_check():
            self.direction = current_direction

    def move(self):
        intial_direction = self.direction
        self.user_input()
        if intial_direction != self.direction:
            self.center()

        if not self.collision_check():
            if self.direction == 'left':
                self.x -= self.speed
            elif self.direction == 'right':
                self.x += self.speed
            elif self.direction == 'up':
                self.y -= self.speed
            else:
                self.y += self.speed
        else:
            self.center()
        self.row = int(self.y//square_height)
        self.col = int(self.x//square_width)
        self.check_tokens()
        if self.check_ghosts():
            self.death()

    def draw(self):
        # TODO: update this animation
        global animation_timer
        global animation_wait
        global play_direction
        pg.draw.circle(window, YELLOW, (int(self.x), int(self.y)), int(square_width/2))

        if animation_timer // animation_wait == 0:
            triangle_width = int(square_width / 2)
            animation_timer += play_direction
            if animation_timer <= 0:
                play_direction = 1
        elif animation_timer // animation_wait == 1:
            triangle_width = int(square_width / 3)
            animation_timer += play_direction
        elif animation_timer // animation_wait == 2:
            triangle_width = int(square_width / 4)
            animation_timer += play_direction
        else:
            triangle_width = 0
            animation_timer += play_direction
            if animation_timer % animation_wait >= animation_wait // 2:
                play_direction = -1

        if self.direction == 'right':
            pg.draw.polygon(window, BLACK, [
                (self.x, self.y),
                (self.x + int(square_width / 2), self.y + triangle_width),
                (self.x + int(square_width / 2), self.y - triangle_width)
            ])
        elif self.direction == 'left':
            pg.draw.polygon(window, BLACK, [
                (self.x, self.y),
                (self.x - int(square_width / 2), self.y + triangle_width),
                (self.x - int(square_width / 2), self.y - triangle_width)
            ])
        elif self.direction == 'up':
            pg.draw.polygon(window, BLACK, [
                (self.x, self.y),
                (self.x + triangle_width, self.y - int(square_width / 2)),
                (self.x - triangle_width, self.y - int(square_width / 2))
            ])
        else:
            pg.draw.polygon(window, BLACK, [
                (self.x, self.y),
                (self.x + triangle_width, self.y + int(square_width / 2)),
                (self.x - triangle_width, self.y + int(square_width / 2)),
            ])

    def warp(self):
        if self.col == 0:
            self.col = len(board[0]) - 1
        elif self.col == len(board[0]) - 1:
            self.col = 0
        else:
            print('you cant warp there!')
        self.center()

    def death(self):
        global lives
        global run
        if lives > 0:
            self.__init__()
            lives -= 1

            ghost_spawns = []

            for row_count, row in enumerate(board):
                for col_count, col in enumerate(row):
                    if col == 2:
                        ghost_spawns.append((col_count, row_count))

            for ghost in ghosts:
                ghost.col, ghost.row = choice(ghost_spawns)
                ghost.center()

        else:
            print('you have no more lives left! You are dead.')
            run = False

    def center(self):
        self.x = self.col * square_width + square_width / 2
        self.y = self.row * square_height + square_height / 2

    def collision_check(self):
        # TODO: prevent turning into a wall
        if self.direction == 'right':
            if self.col == len(board[0]) - 1:
                self.warp()
                return False
            elif board[self.row][self.col + 1] == 0:
                return False
            else:
                return True
        elif self.direction == 'left':
            if self.col == 0:
                self.warp()
                return False
            elif board[self.row][self.col - 1] == 0:
                return False
            else:
                return True
        elif self.direction == 'up':
            if board[self.row - 1][self.col] == 0:
                return False
            else:
                return True
        else:
            if board[self.row + 1][self.col] == 0:
                return False
            else:
                return True

    def check_tokens(self):
        global score
        global run
        global lives
        global level
        # print(self.col, self.row)

        if (self.col, self.row) in tokens:
            tokens.remove((self.col, self.row))
            score += 10

        if len(tokens) == 0:
            lives += 1
            level += 1
            for ghost in ghosts:
                ghost.speed += 1
            self.death()
            for row_count, row in enumerate(board):
                for col_count, col in enumerate(row):
                    if col == 0:
                        tokens.append((col_count, row_count))

    def check_ghosts(self):
        for ghost in ghosts:
            if ghost.row == self.row and ghost.col == self.col:
                return True
        return False


class Ghost:
    speed = 5
    # TODO: make the ghost movements less janky

    def __int__(self):
        print('i did done do dis')
        starting_area = []
        for row_count, row in enumerate(board):
            for col_count, col in enumerate(row):
                if col == 2:
                    starting_area.append((col_count, row_count))
        start = choice(starting_area)
        self.col, self.row = start
        self.x = self.col * square_width + square_width / 2
        self.y = self.row * square_height + square_height / 2
        self.direction = choice(['right', 'left', 'up', 'down'])
        self.width = int(square_width/2)
        self.height = int(square_height/2)

    def define(self):
        #print('i did done do dis')
        starting_area = []
        for row_count, row in enumerate(board):
            for col_count, col in enumerate(row):
                if col == 2:
                    starting_area.append((col_count, row_count))
        start = choice(starting_area)
        self.col, self.row = start
        self.center()
        self.direction = choice(['right', 'left', 'up', 'down'])
        self.width = int(square_width / 2)
        self.height = int(square_height / 2)
        self.turning = False
        self.previous_turn = 0

    def move(self):
        self.warp()
        self.set_direction()

        if self.x_center or self.y_center:
            self.center()
        else:
            if self.direction == 'right':
                self.x += self.speed
            elif self.direction == 'left':
                self.x -= self.speed
            elif self.direction == 'up':
                self.y -= self.speed
            else:
                self.y += self.speed

    def set_direction(self):
        self.x_center = False
        self.y_center = False
        possible_directions = []
        moved = False
        if self.row != int(self.y // square_height) or self.col != int(self.x // square_width):
            moved = True
            #print('move is true')
            self.row = int(self.y // square_height)
            self.col = int(self.x // square_width)

        if board[self.row][self.col + 1] == 0:
            possible_directions.append('right')
        if board[self.row][self.col - 1] == 0:
            possible_directions.append('left')
        if board[self.row - 1][self.col] == 0:
            possible_directions.append('up')
        if board[self.row + 1][self.col] == 0:
            possible_directions.append('down')

        if self.direction not in possible_directions and moved:
            self.new_direction = choice(possible_directions)
            self.turning = True
        elif len(possible_directions) > 2 and moved:
            self.new_direction = choice(possible_directions)
            self.turning = True

        if self.turning and (self.col, self.row) != self.previous_turn:
            if self.color == RED and False:
                print('\ndirection', self.direction)
                print('new', self.new_direction)
                print('possible', possible_directions)
                print('location', (self.col, self.row))

            if (self.x + self.speed) % square_width > square_width/2 and self.direction == 'right':  # if go right do you go past center of square
                self.x_center = True
            elif (self.x - self.speed) % square_width < square_width/2 and self.direction == 'left':  # if go left do you go past center of square
                self.x_center = True
            if (self.y - self.speed) % square_height > square_height/2 and self.direction == 'up':  # if go up do you go past center of square
                self.y_center = True
            elif (self.y + self.speed) % square_height < square_height/2 and self.direction == 'down':  # if go down do you go past center of square
                self.y_center = True

            if self.x_center or self.y_center:
                #print('turned')
                self.direction = self.new_direction
                self.turning = False
                self.previous_turn = (self.col, self.row)

                if chase:
                    if self.color == RED:  # Blinky
                        self.direction = pathfind((self.col, self.row), (player.col, player.row))
                    elif self.color == PINK:
                        if player.direction == 'left':
                            self.direction = pathfind((self.col, self.row), (player.col - Pinky_lead, player.row))
                        elif player.direction == 'right':
                            self.direction = pathfind((self.col, self.row), (player.col + Pinky_lead, player.row))
                        elif player.direction == 'up':
                            self.direction = pathfind((self.col, self.row), (player.col, player.row - Pinky_lead))
                        else:
                            self.direction = pathfind((self.col, self.row), (player.col, player.row + Pinky_lead))
                    elif self.color == LIGHT_BLUE:
                        if player.direction == 'left':
                            reflect = (player.col - Pinky_lead, player.row)
                        elif player.direction == 'right':
                            reflect = (player.col + Pinky_lead, player.row)
                        elif player.direction == 'up':
                            reflect = (player.col, player.row - Pinky_lead)
                        else:
                            reflect = (player.col, player.row + Pinky_lead)

                        x, y = reflect
                        for ghost in ghosts:
                            if ghost.color == RED:  # find Blinky
                                Blinky_x_dis = x - ghost.col
                                Blinky_y_dis = y - ghost.row
                                break
                        # print(x + Blinky_x_dis, y + Blinky_y_dis)

                        path = pathfind((self.col, self.row), (x + Blinky_x_dis, y + Blinky_y_dis))

                        if path != None or True:
                            self.direction = path
                    else:
                        if abs(self.row - player.row) + abs(self.col - player.col) < Clyde_scare_dis:
                            self.direction = pathfind((self.col, self.row), (1, len(board)-1))
                        else:
                            self.direction = pathfind((self.col, self.row), (player.col, player.row))


    def draw(self):
        # TODO: add eyes
        x = self.x
        y = self.y
        ghost_shape = [
            (x - square_width/3, y),
            (x - square_width/4, y - square_height/3),
            (x + square_width/4, y - square_height/3),
            (x + square_width / 3, y),
            (x + square_width / 3, y + square_height/3),
            (x + square_width / 6, y + square_height/4),
            (x, y + square_height / 3),
            (x - square_width / 6, y + square_height / 4),
            (x - square_width / 3, y + square_height / 3)
        ]

        pg.draw.polygon(window, self.color, ghost_shape)

    def warp(self):
        row = int(self.y // square_height)
        col = int(self.x // square_width)
        if col == 0 and self.direction == 'left':
            self.col = len(board[0]) - 2
            self.center()
        elif col == len(board[0]) - 1 and self.direction == 'right':
            self.col = 1
            self.center()

    def center(self):
        self.x = self.col * square_width + square_width / 2
        self.y = self.row * square_height + square_height / 2


class PowerUp:
    pass


player = PacMan()


for i in range(4):
    spooky = Ghost()
    spooky.define()
    spooky.color = ghost_colors[i]
    ghosts.append(spooky)


run = True
while run:
    pg.time.delay(delay)
    window.fill(windowColor)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break

    for row_count, row in enumerate(board):
        for col_count, square in enumerate(row):
            if square == 1:
                pg.draw.rect(window, BLUE, (col_count * square_width, row_count * square_height, square_width+1, square_height+1))
            elif square == 2:
                pg.draw.rect(window, GREEN, (col_count * square_width, row_count * square_height, square_width+1, square_height+1))

    for token in tokens:
        x, y = token
        pg.draw.circle(window, WHITE, (int(x * square_width + square_width / 2), int(y * square_height + square_height / 2)),int(square_width // 10))
    for ghost in ghosts:
        ghost.move()
        ghost.draw()
    display(lives, score, level)
    player.move()
    player.draw()
    pg.display.update()
