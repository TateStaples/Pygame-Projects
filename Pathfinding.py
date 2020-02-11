# this is attempt to implement A* pathfinding
# Dec 4, 2019
__author__ = "Tate Staples"

import pygame
from math import sqrt
pygame.init()

windowWidth = 800
windowHeight = 800
window = pygame.display.set_mode((windowWidth, windowHeight))

size = 30
row_count = size
col_count = size

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

normal_color = LIGHT_BLUE
wall_color = BLACK
open_node_color = ORANGE
closed_node_color = BROWN
path_color = YELLOW
start_color = GREEN
end_color = RED
label_color = BLUE

list_of_walls = []  # this will be filled with all the spot that the user draws in
start_cords = (0, 0)
end_cords = (10, 10)

draw_process = True


def get_square(cords):
    global windowWidth, windowHeight, row_count, col_count
    x, y = cords
    row_height = windowHeight // row_count
    col_width = windowWidth // col_count
    row = y // row_height
    col = x // col_width
    return row, col


def bigger_square(cords, size=1):
    r, c = cords
    spots = []
    for x_change in range(-size+1, size):
        for y_change in range(-size+1, size):
            spots.append((r + y_change, c + x_change))
    return spots


def in_board(cords, board_dimensions):
    r, c = cords
    row_count, col_count = board_dimensions
    return 0 <= r < row_count and 0 <= c < col_count


def square_cords(r, c):
    global windowWidth, windowHeight, row_count, col_count
    row_height = windowHeight // row_count
    col_width = windowWidth // col_count
    x = c * col_width
    y = r * row_height
    return x, y, col_width-1, row_height-1


def get_text_size(w, len):
    width_per_char = w / len * 2
    return int(width_per_char * 72 / 48)


def write_on_square(r, c, msg):
    msg = str(msg)
    x, y, w, h = square_cords(r, c)
    text_font = 'Comic Sans MS'
    text_size = get_text_size(w, len(msg))
    font = pygame.font.SysFont(text_font, text_size)
    score_surface = font.render(msg, False, label_color)
    window.blit(score_surface, (x, y))


def draw_square(row, col, color):
    pygame.draw.rect(window, color, square_cords(row, col))


def pathfind(start_cords, end_cords, list_of_walls, board_dimensions, can_diagonal=True):
    # row_count, col_count = board_dimensions
    def get_neighbors(cords):
        neighbors = []
        row, col = cords
        if can_diagonal:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    dis = 1 if i == 0 or j == 0 else sqrt(2)
                    new_row = row + i
                    new_col = col + j
                    if i == 0 and j == 0:  # if the center
                        pass
                    elif not in_board((new_row, new_col), board_dimensions): pass
                    else:
                        neighbors.append(((new_row, new_col), dis))
        else:
            if in_board((row, col+1), board_dimensions):
                neighbors.append(((row, col+1), 1))
            if in_board((row, col-1), board_dimensions):
                neighbors.append(((row, col-1), 1))
            if in_board((row+1, col), board_dimensions):
                neighbors.append(((row+1, col), 1))
            if in_board((row-1, col), board_dimensions):
                neighbors.append(((row-1, col), 1))
        return neighbors

    def get_index(list, value):
        for count, node in enumerate(list):
            if node.value >= value:
                return count
        return len(list)

    class Node:
        # val = dis_to_start + dis_to_end
        def __init__(self, parent, cords, dis=1):
            self.dis = dis
            self.position = cords
            self.parent = parent
            self.dis_to_target = 0
            self.dis_to_start = 0
            self.value = 0
            self.children = []

        def set_value(self):
            self.value = self.dis_to_start + self.dis_to_target if self.dis_to_target != 0 else 0

        def set_dis_to_start(self, past_dis):
            self.dis_to_start = self.dis + past_dis

        def set_dis_to_target(self):
            x, y = end_cords
            dis = ((self.position[0] - x) ** 2) + (  # pythagoeran
                    (self.position[1] - y) ** 2)
            self.dis_to_target = sqrt(dis)

    # Returns a list of tuples as a path from the given start to the given end in the given maze

    # Create start and end node
    start_node = Node(None, start_cords)
    start_node.dis_to_start = start_node.dis_to_target = start_node.value = 0
    end_node = Node(None, end_cords)
    end_node.dis_to_start = end_node.dis_to_target = end_node.value = 0

    # Initialize both open and closed list
    open_list = []  # nodes to be checked
    closed_list = []  # nodes that have been checked

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        if draw_process:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

        # Get the current node - maybe sort it to make faster
        current_node = open_list[0]

        # Pop current off open list, add to closed list
        # open_list.remove(current_node)
        open_list.pop(0)
        closed_list.append(current_node)
        if draw_process:
            r, c = current_node.position
            if (r, c) != start_cords and (r, c) != end_cords:
                draw_square(r, c, closed_node_color)
                write_on_square(r, c, round(current_node.value, 1))


        # Found the goal
        if current_node.position == end_cords:
            print("got to the end")
            path = []
            current = current_node
            while current is not None:  # traces your path back to the start
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        for neighbor, dis in get_neighbors(current_node.position):
            if neighbor in list_of_walls: continue  # don't go into walls

            # Create new node
            new_node = Node(current_node, neighbor, dis)  # creates a new node
            current_node.children.append(new_node)

        # Loop through children
        for child in current_node.children:

            # Create the node values
            child.set_dis_to_start(current_node.dis_to_start)
            child.set_dis_to_target()
            child.set_value()

            # takes shortcuts
            is_new = True
            insert_index = get_index(open_list, child.value)
            for node in open_list[insert_index:]:
                if child.position == node.position:  # if they are the same
                    if node.dis_to_start > child.dis_to_start:  # if this one better
                        open_list.remove(node)
                        for kid in node.children:
                            kid.parent = child
                    else:
                        is_new = False
                    break

            # prevent repeats
            if is_new:
                for node in closed_list:
                    if node.position == child.position:
                        is_new = False
                        break

            # adds child to open list
            if is_new:
                open_list.insert(insert_index, child)
                if draw_process:
                    r, c = child.position
                    if (r, c) != start_cords and (r, c) != end_cords:
                        draw_square(r, c, open_node_color)
        if draw_process:
            pygame.display.update()


def main():
    global start_cords, end_cords
    # basic display
    for r in range(row_count+1):
        for c in range(col_count+1):
            if (r, c) == start_cords:
                draw_square(r, c, start_color)
            elif (r, c) == end_cords:
                draw_square(r, c, end_color)
            else:
                draw_square(r, c, normal_color)

    run = True
    is_editing = False
    edit_size = 1
    is_drawing = True
    pygame.display.update()

    # main loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print("main loop over")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                is_editing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                is_editing = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_s]:  # set start
            print(1)
            new = get_square(pygame.mouse.get_pos())
            r1, c1 = start_cords
            r2, c2 = new
            draw_square(r1, c1, normal_color)
            draw_square(r2, c2, start_color)
            start_cords = new
            pygame.display.update()
        if keys[pygame.K_e]:  # set end
            print(2)
            new = get_square(pygame.mouse.get_pos())
            r1, c1 = end_cords
            r2, c2 = new
            draw_square(r1, c1, normal_color)
            draw_square(r2, c2, end_color)
            end_cords = new
            pygame.display.update()

        if keys[pygame.K_SPACE]:  # used to switch between writing and erasing
            is_drawing = False if is_drawing else True
            pygame.time.delay(100)
        if keys[pygame.K_RETURN]:  # when you are done set up
            print("begun")
            for square in pathfind(start_cords, end_cords, list_of_walls, (row_count, col_count)):
                if square != start_cords and square != end_cords:
                    r, c = square
                    draw_square(r, c, path_color)
            pygame.display.update()
            run = False
            print("over")

        if keys[pygame.K_1]:
            edit_size = 1
        elif keys[pygame.K_2]:
            edit_size = 2
        elif keys[pygame.K_3]:
            edit_size = 3
        elif keys[pygame.K_4]:
            edit_size = 4
        elif keys[pygame.K_5]:
            edit_size = 5
        elif keys[pygame.K_6]:
            edit_size = 6
        elif keys[pygame.K_7]:
            edit_size = 7
        elif keys[pygame.K_8]:
            edit_size = 8
        elif keys[pygame.K_9]:
            edit_size = 9

        if is_editing:
            cords = pygame.mouse.get_pos()
            center = get_square(cords)
            for square in bigger_square(center, edit_size):
                row, col = square
                if square == start_cords or square == end_cords: continue
                if is_drawing and square not in list_of_walls: # if drawing a wall
                    list_of_walls.append(square)
                    draw_square(row, col, wall_color)
                    pygame.display.update()
                elif not is_drawing and square in list_of_walls:  # erasing
                    # print("erasing")
                    list_of_walls.remove(square)
                    draw_square(row, col, normal_color)
                    pygame.display.update()
    pygame.display.update()

    # end screen
    while True:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            main()
            break


if __name__ == '__main__':
    main()
