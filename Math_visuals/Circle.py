from resources import *
pygame.init()

windowWidth = 500
windowHeight = 500
windowColor = WHITE
window = pygame.display.set_mode((windowWidth, windowHeight))


def draw_sin(pos, width, height, d=pi*2, color=BLUE):
    draw_function(sin, domain=(0, d), range=(-1, 1), width=width, height=height, origin=pos, window=window, color=color)


def draw_cos(pos, width, height, d=pi*2, color=RED):
    draw_function(cos, domain=(0, d), range=(-1, 1), width=width, height=height, origin=pos, window=window, color=color)


class Sim:
    radius = 200
    radius_color = GREEN
    circle_color = BLACK
    dx_color = RED
    dy_color = BLUE

    def __init__(self):
        self.t = 0
        self.speed = .1
        self.graphic_timer = None
        self.pos = (windowWidth // 2, windowHeight - self.radius)

    def tick(self):
        self.t += self.speed
        self.t %= 10*pi
        self.input()
        self.draw()

    def draw(self):
        window.fill(windowColor)
        if self.graphic_timer is None:
            self.draw_circle()
            self.draw_angle()
            self.draw_lines()
        else:
            self.draw_visual()
        self.draw_bars()
        self.labels()
        self.draw_graphes()
        pygame.display.update()
        check_events()

    def sin(self):
        return sin(self.t)

    def cos(self):
        return cos(self.t)

    def radians(self):
        return self.t % (2*pi)

    def degrees(self):
        return degrees(self.radians())

    def get_vector(self):
        pos = pygame.mouse.get_pos()
        if distance(self.pos, pos) < self.radius:
            toward = towards(self.pos, pos)
            dx, dy = get_components(toward, self.radius)
            self.t = tau - toward
            return dx, dy
        else:
            dx, dy = get_components(self.t, self.radius)
            return dx, dy*-1

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.speed += .01
        if keys[pygame.K_DOWN]:
            self.speed -= .01
        if keys[pygame.K_RETURN]:
            self.graphic_timer = 0

    def draw_circle(self):
        pygame.draw.circle(window, self.circle_color, self.pos, self.radius, 1)

    def draw_angle(self):
        x, y = self.pos
        angle_radius = 10
        rect = (x - angle_radius, y - angle_radius, 2*angle_radius, 2*angle_radius)
        pygame.draw.arc(window, self.circle_color, rect, 0, self.radians())

    def draw_lines(self):
        dx, dy = self.get_vector()
        x, y = self.pos
        final = (x+dx, y+dy)
        pygame.draw.line(window, self.radius_color, self.pos, final)
        pygame.draw.line(window, self.dx_color, self.pos, (x + dx, y))
        display(window, "y", (x+dx+5, y+dy/2))
        pygame.draw.line(window, self.dy_color, (x+dx, y), final)
        display(window, "x", (x + dx/2, y + 5))

    def labels(self):
        dx, dy = self.get_vector()
        display(window, f"t = {round(self.t/pi, 2)}pi", (0, 0))
        display(window, f"radians = {round(self.radians(), 2)}", (0, 30))
        display(window, f"degrees = {round(self.degrees())}º", (0, 60))

        display(window, f"cos = {round(dx/self.radius, 2)}", (200, 0))
        display(window, f"sin = {round(dy*-1/self.radius, 2)}", (200, 50))
        #display(window, f"radius = 1", (0, 90))

    def draw_graphes(self):
        periodic = True
        d = self.radians()
        max_width = 100
        graph_x = 340
        cos_mid = 25
        sin_mid = 75
        amplitude = 20
        cos_1 = (graph_x, cos_mid)
        sin_1 = (graph_x, sin_mid)
        cos_2 = (graph_x+max_width+10, cos_mid)
        sin_2 = (graph_x+max_width+10, sin_mid)
        # axises
        pygame.draw.line(window, BLACK, (graph_x, cos_mid), (graph_x+max_width, cos_mid))
        pygame.draw.line(window, BLACK, (graph_x, sin_mid), (graph_x + max_width, sin_mid))
        if periodic:
            period_cos = cos_1
            period_sin = sin_1
            p_width = max_width
            flow_cos = cos_2
            flow_sin = sin_2
            f_width = 50
        else:
            period_cos = cos_2
            period_sin = sin_2
            p_width = 50
            flow_cos = cos_1
            flow_sin = sin_1
            f_width = max_width

        # periodic
        draw_cos(period_cos, p_width*d/tau, 2*amplitude, d)
        draw_sin(period_sin, p_width*d/tau, 2*amplitude, d)

        # flowing
        draw_function(cos, domain=(d, d+tau), range=(-1, 1), width=f_width, height=2*amplitude, origin=flow_cos,
                      window=window, color=RED)
        draw_function(sin, domain=(d, d + tau), range=(-1, 1), width=f_width, height=2*amplitude, origin=flow_sin,
                      window=window, color=BLUE)

    def draw_bars(self):
        bar_x = 310
        cos_mid = 25
        sin_mid = 75
        amplitude = 20
        dx, dy = shorten_vector(self.get_vector(), amplitude)
        pygame.draw.rect(window, self.dx_color, (bar_x, cos_mid, 20, dx*-1))
        pygame.draw.rect(window, self.dy_color, (bar_x, sin_mid, 20, dy))

    def draw_visual(self):
        x = self.graphic_timer
        visual_start = 50
        circle_radius = 50
        visual_width = 400
        y_coord = 300
        periods = 4
        proportion = x / visual_width
        angle = periods * tau * proportion
        dx, dy = get_components(angle, circle_radius)
        circle_pos = round_tup((visual_start + x, y_coord))
        up_pos = round_tup((visual_start + x, y_coord - dy))
        edge = round_tup((visual_start + x + dx, y_coord - dy))
        draw_sin((visual_start, y_coord), x, circle_radius*2, angle)
        pygame.draw.circle(window, self.circle_color, circle_pos, circle_radius, 1)
        pygame.draw.line(window, self.dx_color, up_pos, edge)  # x
        pygame.draw.line(window, self.radius_color, circle_pos, edge)  # radius
        pygame.draw.line(window, self.dy_color, circle_pos, up_pos)  # y
        self.graphic_timer += self.speed * 10
        self.t = angle
        if self.graphic_timer > visual_width:
            self.graphic_timer = None


if __name__ == '__main__':
    thing = Sim()
    while True:
        thing.tick()
