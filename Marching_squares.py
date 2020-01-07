# mid december 2019

import pygame
import noise
from random import choice
import time
import math

# hello tate let's see if this commits

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (135,206,235)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

windowWidth = 700
windowHeight = 700

window = pygame.display.set_mode((windowWidth, windowHeight))

windowColor = (0, 0, 0)
amount_of_rows = 50
amount_of_cols = 50
square_width = windowWidth // (amount_of_cols - 1)
square_height = windowHeight // (amount_of_rows - 1)


def main():
    nodes = create_nodes(amount_of_rows, amount_of_cols)
    #nodes = [[1, -1], [-1, 1]]
    draw_nodes(nodes)
    pygame.display.update()
    editting(nodes)


def weighted_average(val1, val2, weight1, weight2):
    total_weight = abs(weight1) + abs(weight2)
    proportion1 = 1/2 if total_weight == 0 else abs(weight2) / total_weight
    proportion2 = 1/2 if total_weight == 0 else abs(weight1) / total_weight
    return round(val1 * proportion1 + val2 * proportion2)


def create_nodes(r, c):
    nodes = []
    ''' this is random
    for i in range(r):
        row_of_nodes = []
        for j in range(c):
            row_of_nodes.append(choice([1, -1]))
        nodes.append(row_of_nodes)
    #print(nodes)
    '''
    # this implements perlin noise
    scale = 1#amount_of_cols / 10
    #print(scale)
    octaves = round(time.time() % 20) + 1
    persistence = time.time() % 1.5
    lacunarity = time.time() % 1.5

    for i in range(r):
        row_of_nodes = []
        for j in range(c):
            val = noise.pnoise2(i / scale, j / scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=c, repeaty=r, base=0)
            row_of_nodes.append(val)
        nodes.append(row_of_nodes)
    # '''
    return nodes


def draw_nodes(nodes):
    for r in range(len(nodes)-1):  # for each row except bottom
        for c in range(len(nodes[r])-1):  # for each col except far right
            draw_square((r, c), nodes)


def draw_square(cords, nodes):
    r, c = cords
    global windowWidth, windowHeight
    x1, y1 = square_width * c, square_height * r
    x_half, y_half = x1 + square_width//2, y1 + square_height//2
    x2, y2 = x1 + square_width, y1 + square_height
    top_left = x1, y1
    top_right = x2, y1
    bottom_left = x1, y2
    bottom_right = x2, y2
    tl = nodes[r][c] > 0
    tr = nodes[r][c + 1] > 0
    bl = nodes[r + 1][c] > 0
    br = nodes[r + 1][c + 1] > 0

    fancy = True
    top_mid_x = weighted_average(x1, x2, nodes[r][c], nodes[r][c+1]) if fancy else x_half
    bottom_mid_x = weighted_average(x1, x2, nodes[r+1][c], nodes[r+1][c+1]) if fancy else x_half
    left_mid_y = weighted_average(y1, y2, nodes[r][c], nodes[r+1][c]) if fancy else y_half
    right_mid_y = weighted_average(y1, y2, nodes[r][c+1], nodes[r+1][c+1]) if fancy else y_half

    pygame.draw.rect(window, BLACK, [x1, y1, square_width, square_height])
    # pygame.draw.rect(window, (255, 0, 0), [x1, y1, square_width, square_height], 1)  # outline

    if tl and tr and bl and br:  # full square
        pygame.draw.rect(window, GREEN, [x1, y1, square_width, square_height])

    elif tl and tr and bl:  # triangle w/o br
        pygame.draw.polygon(window, GREEN, [top_left, top_right, (x2, right_mid_y), (bottom_mid_x, y2), bottom_left])
    elif tl and tr and br:  # triangle w/o bl
        pygame.draw.polygon(window, GREEN, [top_left, top_right, bottom_right, (bottom_mid_x, y2), (x1, left_mid_y)])
    elif tl and br and bl:  # triangle w/o tr.
        pygame.draw.polygon(window, GREEN, [top_left, (top_mid_x, y1), (x2, right_mid_y), bottom_right, bottom_left])
    elif br and tr and bl:  # triangle w/o tl
        pygame.draw.polygon(window, GREEN, [bottom_right, top_right, (top_mid_x, y1), (x1, left_mid_y), bottom_left])

    elif tl and tr:  # rectangle on top
        pygame.draw.polygon(window, GREEN, [top_left, top_right, (x2, right_mid_y), (x1, left_mid_y)])
    elif bl and br:  # rectangle on bottom
        pygame.draw.polygon(window, GREEN, [bottom_left, bottom_right, (x2, right_mid_y), (x1, left_mid_y)])

    elif tl and bl:  # rectangle on left
        pygame.draw.polygon(window, GREEN, [top_left, bottom_left, (bottom_mid_x, y2), (top_mid_x, y1)])
    elif tr and br:  # rectangle on right
        pygame.draw.polygon(window, GREEN, [top_right, bottom_right, (bottom_mid_x, y2), (top_mid_x, y1)])

    elif bl and tr:  # positive diagonal
        pygame.draw.polygon(window, GREEN, [
            bottom_left,
            (bottom_mid_x, y2),
            (x2, right_mid_y),
            top_right,
            (top_mid_x, y1),
            (x1, left_mid_y)
        ])
    elif tl and br:  # negative diagonal
        pygame.draw.polygon(window, GREEN, [
            top_left,
            (top_mid_x, y1),
            (x2, right_mid_y),
            bottom_right,
            (bottom_mid_x, y2),
            (x1, left_mid_y)
        ])

    # the single triangles
    elif tl:
        pygame.draw.polygon(window, GREEN, [top_left, (x1, left_mid_y), (top_mid_x, y1)])
    elif tr:
        pygame.draw.polygon(window, GREEN, [top_right, (x2, right_mid_y), (top_mid_x, y1)])
    elif bl:
        pygame.draw.polygon(window, GREEN, [bottom_left, (x1, left_mid_y), (bottom_mid_x, y2)])
    elif br:
        pygame.draw.polygon(window, GREEN, [bottom_right, (x2, right_mid_y), (bottom_mid_x, y2)])

    # pygame.draw.rect(window, RED if tr else BLUE, [x1, y1, 0, 0])  # dot


def editting(nodes):
    running = True
    print("editting")
    rate_of_change = 0.05
    highest_val = .16
    edit_tickness = amount_of_cols // 30
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and False:
                if event.button == 4:
                    edit_tickness = edit_tickness + 1 if edit_tickness < amount_of_cols/2 else edit_tickness
                elif event.button == 5:
                    edit_tickness = edit_tickness - 1 if edit_tickness > 1 else 1

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            edit_tickness = edit_tickness + 1 if edit_tickness < amount_of_cols/4 else edit_tickness
            pygame.time.delay(100)
        elif keys[pygame.K_s]:
            edit_tickness = edit_tickness - 1 if edit_tickness > 1 else 1
            pygame.time.delay(100)

        if keys[pygame.K_a]:
            for r, c in get_nearest(pygame.mouse.get_pos(), edit_tickness):
                if 0 <= r < amount_of_rows and 0 <= c < amount_of_cols:
                    nodes[r][c] = nodes[r][c] - rate_of_change if nodes[r][c] <= highest_val else highest_val
                    update_point((r, c), nodes)
            pygame.display.update()
        elif keys[pygame.K_d]:
            for r, c in get_nearest(pygame.mouse.get_pos(), edit_tickness):
                if 0 <= r < amount_of_rows and 0 <= c < amount_of_cols:
                    nodes[r][c] = nodes[r][c] + rate_of_change if nodes[r][c] >= -highest_val else -highest_val
                    update_point((r, c), nodes)
            pygame.display.update()
        elif keys[pygame.K_RETURN]:
            running = False
            del nodes
            main()
            quit()


def get_nearest(cords, radius=1):
    x, y = cords
    c = int((x + square_width/2) // square_width)
    r = int((y + square_height/2) // square_height)
    list_of_nearest = [(r, c)]
    for y_dis in range(-radius, radius):
        #print("test")
        # x^2 + y^2 = r^2
        # x = sqrt(r^2 - y^2)
        width = int(math.sqrt(radius ** 2 - y_dis ** 2))
        for x_dis in range(-width + 1, width):
            list_of_nearest.append((r + y_dis, c + x_dis))
    return list_of_nearest


def update_point(cords, nodes):
    global amount_of_rows, amount_of_cols
    r, c = cords
    if r < amount_of_rows-1:  # bottom
        if c < amount_of_cols-2:  # right
            draw_square(cords, nodes)
        if c >= 0:  # left
            draw_square((r, c-1), nodes)
    if r >= 0:  # top
        if c < amount_of_cols-2:  # right
            draw_square((r-1, c), nodes)
        if c >= 0:  # left
            draw_square((r-1, c-1), nodes)


if __name__ == "__main__":
    main()
