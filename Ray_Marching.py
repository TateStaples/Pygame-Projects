from resources import *
from random import *
pygame.init()

windowWidth = 800
windowHeight = 800
window = pygame.display.set_mode((windowWidth, windowHeight))


class GameObject:
    height = 10
    all_objects = []

    def __init__(self):
        self.all_objects.append(self)

    def get_dis(self, pos):
        pass

    @staticmethod
    def generate_random():
        all_types = [Circle, Square]
        colors = [GREEN, BLUE, PINK, ORANGE, RED, YELLOW]
        thing = choice(all_types)
        thing(randint(0, windowWidth), randint(0, windowWidth), randint(5, 50), choice(colors))


class Circle(GameObject):
    def __init__(self, x, y, r, c):
        self.x, self.y, self.radius, self.color = x, y, r, c
        super(Circle, self).__init__()

    def draw(self):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)

    def get_dis(self, pos):
        from_center = distance(pos, (self.x, self.y))
        return from_center - self.radius


class Rectangle(GameObject):
    def __init__(self, x, y, w, l, c):
        self.x = x
        self.y = y
        self.width = w
        self.length = l
        self.color = c
        super(Rectangle, self).__init__()

    def draw(self):
        rect = [self.x, self.y, self.width, self.length]
        pygame.draw.rect(window, self.color, rect)
        return [self.x, self.y, self.width, self.length]

    def get_dis(self, pos):
        x, y = pos
        if x < self.x:
            my_x = self.x
        elif x > self.x + self.width:
            my_x = self.x + self.width
        else:
            my_x = x
        if y < self.y:
            my_y = self.y
        elif y > self.y + self.length:
            my_y = self.y + self.length
        else:
            my_y = y
        return distance(pos, (my_x, my_y))


class Square(Rectangle):
    def __init__(self, x, y, s, c):
        super(Square, self).__init__(x, y, s, s, c)


class Ray:
    all_objects = GameObject.all_objects

    def __init__(self, x, y):
        self.x, self.y = x, y

    def cast(self, direction, draw=True):
        dis = 1
        total_dis = 0
        while dis > 0:
            if draw:
                pygame.time.delay(10)
            dis = self.get_dis()
            if dis < 1:
                break
            total_dis += dis
            if draw:
                pygame.draw.circle(window, WHITE, (int(self.x), int(self.y)), int(dis), 1)
            dx, dy = get_components(direction, dis)
            self.x += dx
            self.y += dy
            if draw:
                pygame.draw.circle(window, RED, (int(self.x), int(self.y)), 4)
                pygame.display.update()
                check_events()
            if not 0 < self.x < windowWidth or not 0 < self.y < windowHeight:
                #print(self.x, self.y)
                return 1, None
        distances = [thing.get_dis((self.x, self.y)) for thing in self.all_objects]
        closest_obj = self.all_objects[distances.index(min(distances))]
        return total_dis, closest_obj

    def get_dis(self):
        distances = [thing.get_dis((self.x, self.y)) for thing in self.all_objects]
        low_dis = min(distances)
        return low_dis


def draw_all():
    for thing in GameObject.all_objects:
        thing.draw()


def get_stuff(start, end, amount):
    dif = end - start
    d = dif/amount
    return [start + i*d for i in range(amount)]


class Camera:
    hFov = 90
    vFov = 90

    def __init__(self, objs, bars=90):
        self.stuff = objs
        self.view_angle = 0
        self.upview = 10
        self.bars = bars
        self.start_cords = None
        self.player_x = self.player_y = None

    def main_view(self):
        self.top_view()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_cords = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONUP:
                    end_cords = pygame.mouse.get_pos()
                    window.fill(BLACK)
                    draw_all()
                    x, y = self.start_cords
                    the_ray = Ray(x, y)
                    the_ray.cast(towards(self.start_cords, end_cords))
                    window.fill(BLACK)
                    self.start_cords = None
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    self.player_view()
            window.fill(BLACK)
            self.top_view()
            pygame.display.update()

    def top_view(self):
        for thing in self.stuff:
            thing.draw()
        self.draw_camera()
        if self.start_cords is not None:
            pygame.draw.line(window, WHITE, self.start_cords, pygame.mouse.get_pos())

    def draw_flat(self, x, y):
        info = []
        for i in get_stuff(self.view_angle - self.hFov / 2, self.view_angle + self.hFov / 2, self.bars):
            angle = radians(i)
            ray = Ray(x, y)
            dis, obj = ray.cast(angle, draw=False)
            if obj is not None:
                info.append((obj.color, dis))
            else:
                info.append((BLACK, 10000))
        bar_width = windowWidth / self.bars
        percent = self.upview / self.vFov
        horizon = windowHeight / 2 + percent * windowHeight
        pygame.draw.rect(window, LIGHT_BROWN, (0, horizon, windowWidth, windowHeight-horizon))
        pygame.draw.rect(window, LIGHT_BLUE, (0, 0, windowWidth, horizon))
        for i in range(self.bars):
            color, dis = info[i]
            if dis <= 0: continue
            upward_angle = atan(10 / dis)
            percent_up = degrees(upward_angle) / self.vFov
            dz = windowHeight * percent_up
            bar_height = 2 * dz
            rect = (i * bar_width, horizon - dz, bar_width + 1, bar_height)
            pygame.draw.rect(window, color, rect)

    def player_view(self):
        if self.player_x is None:
            x, y = pygame.mouse.get_pos()
        else:
            x, y = self.player_x, self.player_y
        walk_speed = 15
        turn_speed = 10
        window.fill(BLACK)
        self.draw_flat(x, y)
        pygame.display.update()
        while True:
            check_events()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                # print(1)
                self.view_angle -= turn_speed
                window.fill(BLACK)
                self.draw_flat(x, y)
                pygame.display.update()
            elif keys[pygame.K_RIGHT]:
                # print(2)
                self.view_angle += turn_speed
                window.fill(BLACK)
                self.draw_flat(x, y)
                pygame.display.update()
            if keys[pygame.K_w]:
                self.upview += turn_speed
                window.fill(BLACK)
                self.draw_flat(x, y)
                pygame.display.update()
            elif keys[pygame.K_s]:
                self.upview -= turn_speed
                window.fill(BLACK)
                self.draw_flat(x, y)
                pygame.display.update()
            if keys[pygame.K_UP]:
                # print(3)
                dx, dy = get_components(radians(self.view_angle), walk_speed)
                angle = towards((0, 0), (dx, dy))
                dis, obj = Ray(x, y).cast(angle, False)
                if dis > walk_speed or obj is None:
                    x += dx
                    y += dy
                    window.fill(BLACK)
                    self.draw_flat(x, y)
                    pygame.display.update()
            elif keys[pygame.K_DOWN]:
                # print(4)
                dx, dy = get_components(radians(self.view_angle), walk_speed)
                angle = towards((dx, dy), (0, 0))
                dis, obj = Ray(x, y).cast(angle, False)
                if dis > walk_speed or obj is None:
                    x -= dx
                    y -= dy
                    window.fill(BLACK)
                    self.draw_flat(x, y)
                    pygame.display.update()
            elif keys[pygame.K_RETURN]:
                self.player_x, self.player_y = x, y
                return

    def draw_camera(self):
        if self.player_x is not None:
            x, y = self.player_x, self.player_y
            w = 20
            h = 20
            rect = (x-w/2, y-h/2, w, h)
            triangle = [(x, y), (x+w, y+h/3), (x+w, y-h/3)]
            pygame.draw.polygon(window, LIGHT_GREY, triangle)
            pygame.draw.rect(window, GREY, rect)


if __name__ == '__main__':
    amount = 10
    for i in range(amount):
        GameObject.generate_random()
    test = Camera(GameObject.all_objects, windowWidth//1)
    test.main_view()