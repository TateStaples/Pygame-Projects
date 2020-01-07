import pygame
from Pathfinding import pathfind
from Pathfinding import in_board
from random import *
from copy import deepcopy

# This is a first attempt at making a maze generator
# Created: very late december
__author__ = "Tate Staples"


windowWidth = 700
windowHeight = 700

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (135,206,235)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

window = pygame.display.set_mode((windowWidth, windowHeight))

windowColor = (0, 0, 0)
amount_of_rows = 100
amount_of_cols = 100
square_width = windowWidth // (amount_of_cols)
square_height = windowHeight // (amount_of_rows)
list_of_walls = []


def generate_framed_2d(l, w, frame_val=1, center_val=0, gaps=()):
    board = []
    for r in range(l):
        row = []
        for c in range(w):
            if (r == 0 or r == l - 1 or c == 0 or c == w - 1) and (c, r) not in gaps:
                list_of_walls.append((r, c))
                row.append(frame_val)
            else:
                row.append(center_val)
        board.append(row)
    return board


def draw(board, color_dict={1: RED, 0: WHITE}):
    global square_width, square_height
    for r in range(len(board)):
        for s in range(len(board[r])):
            val = board[r][s]
            color = color_dict[val]
            x, y = s * square_width, r * square_height
            pygame.draw.rect(window, color, [x, y, square_width-1, square_height-1])


def path(start, end):
    return pathfind(start, end, list_of_walls, (amount_of_rows, amount_of_cols), False)


def add_wall(board, r, c):
    board[r][c] = 1
    list_of_walls.append((r, c))
    return board


def surround_walls(center_r, center_c, override=False):
    global board
    for r, c in get_neighbors((center_r, center_c), corners=False):
        if board[r][c] == 0 or override:
            board = add_wall(board, r, c)


def get_neighbors(cords, corners=False):
    neighbors = []
    board_dimensions = amount_of_rows, amount_of_cols
    row, col = cords
    if corners:
        for i in range(-1, 2):
            for j in range(-1, 2):
                # dis = 1 if i == 0 or j == 0 else sqrt(2)
                new_row = row + i
                new_col = col + j
                if i == 0 and j == 0:  # if the center
                    pass
                elif not in_board((new_row, new_col), board_dimensions): pass
                else:
                    neighbors.append((new_row, new_col))
    else:
        if in_board((row, col + 1), board_dimensions):
            neighbors.append((row, col + 1))
        if in_board((row, col - 1), board_dimensions):
            neighbors.append((row, col - 1))
        if in_board((row + 1, col), board_dimensions):
            neighbors.append((row + 1, col))
        if in_board((row - 1, col), board_dimensions):
            neighbors.append((row - 1, col))
    return neighbors


class Space:
    empty_variable = 0

    @staticmethod
    def make_space():
        global board
        for r in range(len(board)):
            for c in range(len(board[r])):
                if board[r][c] == 0:
                    return Space(r, c)
        return None

    def __init__(self, r, c):
        self.all_coords = [(r, c)]
        self.walls = []
        self.spread(r, c)

    def spread(self, origin_r, origin_c):
        live_boxes = [(origin_r, origin_c)]
        while len(live_boxes) > 0:
            for origin_r, origin_c in reversed(live_boxes):
                live_boxes.remove((origin_r, origin_c))
                for r, c in get_neighbors((origin_r, origin_c)):
                    if board[r][c] == 0 and (r, c) not in self.all_coords:
                        # print("test")
                        self.all_coords.append((r, c))
                        live_boxes.append((r, c))
                    elif board[r][c] == 1 and 0 < r < amount_of_rows-1 and 0 < c < amount_of_cols-1 and (r, c) not in self.walls:
                        # print('test2')
                        self.walls.append((r, c))


def generate_correct_path(start, end):
    global board
    points = 5
    original = deepcopy(board)
    works = False
    while not works:
        works = True
        coords = [(randint(1, amount_of_rows-2), randint(1, amount_of_cols-2)) for i in range(points)]
        coords.append(end)
        point1 = start
        for point2 in coords:
            the_path = path(point1, point2)
            if the_path is None:
                works = False
                print("reset")
                board = deepcopy(original)
                break
            for r, c in the_path:
                board[r][c] = 2
            for r, c in the_path:
                if (r, c) != point2:
                    surround_walls(r, c)
            point1 = point2


def flood_solve_maze(start, end, path_val=2, wall_val=1):
    class Box:
        def __init__(self, pos, parent):
            self.pos = pos
            self.r, self.c = pos
            self.parent = parent
    start_box = Box(start, None)
    filled_spots = [start]
    live_boxes = [start_box]
    while len(live_boxes) > 0:
        for box in live_boxes:
            # print(1)
            live_boxes.remove(box)
            for neighbor in get_neighbors(box.pos):
                r, c = neighbor
                # print(neighbor)
                neighbor_box = Box(neighbor, box)
                if neighbor == end:
                    # print("solved!")
                    the_path = []
                    the_box = neighbor_box
                    while the_box.parent is not None:
                        the_path.append(the_box.pos)
                        the_box = the_box.parent
                    return the_path
                if neighbor not in filled_spots and board[r][c] != wall_val and board[r][c] == path_val:
                    # print("test")
                    live_boxes.append(neighbor_box)
                    filled_spots.append(neighbor)
    return []


if __name__ == '__main__':
    pygame.init()
    drawing = True
    board = generate_framed_2d(amount_of_rows, amount_of_cols, gaps=[(1, 0), (amount_of_cols-2, amount_of_rows-1)])
    color_dict = {0: BLUE, 1: BLACK, 2: WHITE, 3:RED, 4:ORANGE}

    '''
    the_path = path((0, 1), (amount_of_cols-1, amount_of_rows-2))
    for r, c in the_path:
        board[r][c] = 2
    for r, c in the_path:
        surround_walls(r, c)
    '''
    generate_correct_path((0, 1), (amount_of_cols-1, amount_of_rows-2))

    space = Space.make_space()
    while space is not None:
        # pygame.time.delay(1000)
        if drawing:
            draw(board, color_dict)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
        if len(space.all_coords) == 0 or len(space.all_coords) == 0:
            break
        start = choice(space.walls)
        end = choice(space.all_coords)
        r1, c1 = start
        list_of_walls.remove(start)
        board[r1][c1] = 0
        the_path = path(start, end)
        if the_path is None:
            break
        for r, c in the_path:
            board[r][c] = 2
        for r, c in the_path:
            surround_walls(r, c)
        space = Space.make_space()
    '''
    for r, c in flood_solve_maze((0, 1), (amount_of_cols-1, amount_of_rows-2)):
        if board[r][c] == 1:
            print("flood doesnt work")
        board[r][c] = 4
    '''
    print("over")
    draw(board, color_dict)
    pygame.display.update()
    while True:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
