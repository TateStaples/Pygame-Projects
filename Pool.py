from resources import *
pygame.init()

windowWidth = 700
windowHeight = 700
window = pygame.display.set_mode((windowWidth, windowHeight))
bgColor = DARK_GREEN


class Ball:
    radius = 10
    slow_rate = .01
    balls = []

    def __init__(self, x=windowWidth//2, y=windowHeight//2, color=RED):
        self.x = x
        self.y = y
        self.color = color
        self.dx = 0
        self.dy = 0
        self.balls.append(self)
        self.moved = False

    def pos(self):
        return self.x, self.y

    def int_pos(self):
        pos = tuple([int(i) for i in self.pos()])
        return pos

    def move(self):
        self.x += self.dx
        self.y -= self.dy

    def tick(self):
        self.move()
        self.dx *= 1 - self.slow_rate
        self.dy *= 1 - self.slow_rate
        if not self.moved:
            self.reflect()
        return self.draw()

    def draw(self):
        pygame.draw.circle(window, self.color, self.int_pos(), self.radius)

    def reflect(self):
        if self.x < self.radius:
            self.dx *= -1
            self.x = self.radius
        elif self.x + self.radius > windowWidth:
            self.dx *= -1
            self.x = windowWidth - self.radius
        if self.y < self.radius:
            self.y = self.radius
            self.dy *= -1
        elif self.y + self.radius > windowHeight:
            self.y = windowHeight - self.radius
            self.dy *= -1
        for ball in self.balls:
            if ball != self and distance(self.pos(), ball.pos()) <= self.radius + ball.radius:
                self.ball_collsion(ball)

    def vector(self):
        return self.dx, self.dy

    def velocity(self):
        return vector_magnitude(self.vector())

    def set_motion(self, vector):
        self.dx, self.dy = vector
        #self.moved = True

    def ball_collsion(ball1, ball2):
        intial_vector = ball1.vector()
        mag = vector_magnitude(intial_vector)
        direction = towards(ball1.pos(), ball2.pos())
        offset = vector_angle(intial_vector) - direction
        a_angle = direction + 90 if offset > 90 else direction - 90
        print(ball1, ball2)
        output_a = get_components(radians(a_angle), mag*sin(radians(offset)))
        output_b = get_components(direction, mag*cos(radians(offset)))
        # print(get_unit_vector(output_a), get_unit_vector(output_b))
        ball2.move_to_border(ball1)
        ball1.set_motion(output_a)
        ball2.set_motion(output_b)

    def move_to_border(self, other):
        direction = towards(self.pos(), ball2.pos())
        dx_1, dy_1 = get_components(direction, self.radius)
        dx_2, dy_2 = get_components(direction, other.radius)
        other.x = self.x + dx_1 + dx_2
        other.y = self.y + dy_1 + dy_2
        #step_1 = self.x + dx_1, self.y + dy_1
        #pygame.draw.line(window, ORANGE, self.pos(), step_1)
        #pygame.draw.line(window, PINK, step_1, other.pos())

    def hitbox(self):
        return self.x - self.radius, self.y - self.radius, 2 * self.radius, 2*self.radius

    def __repr__(self):
        return f"Ball @ {(self.pos())}"


if __name__ == '__main__':
    ball = Ball()
    ball2 = Ball(100, 100, BLUE)
    while True:
        check_events()
        window.fill(bgColor)
        pygame.draw.line(window, WHITE, ball.pos(), pygame.mouse.get_pos())
        for b in Ball.balls:
            b.tick()
        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            x, y = pygame.mouse.get_pos()
            dx, dy = x - ball.x, ball.y - y
            vector = dx, dy
            vector = resize_vector(vector, vector_magnitude(vector)/10)
            vector = shorten_vector(vector, 50)
            ball.set_motion(vector)




