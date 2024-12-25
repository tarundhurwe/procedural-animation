import pygame
import math
import random


class PygameInit:
    def __init__(self, distance=100, speed=10):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1500, 700
        self.FPS = 60
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.MAGENTA = (255, 0, 255)
        self.CYAN = (0, 255, 255)
        self.distance = distance
        self.speed = speed
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dragging = False
        self.velocity = 0.03
        self.dragged_index = -1
        pygame.display.set_caption("Procedural Animation")

    def pygame_instance(self):
        return pygame


class Animation:
    def __init__(self, num_dots, game, move=False):
        self.num_dots = num_dots
        self.dot_pos = []
        self.game = game
        self.pygame = self.game.pygame_instance()
        self.num = 0
        self.boundary = False
        self.even = True
        self.dots = []
        self.move = move

    def place_dots(self):
        for i in range(self.num_dots):
            if i == 0:
                x = self.game.WIDTH // 2 - 200
                y = self.game.HEIGHT // 2 - 200
                self.dot_pos.append([x, y])
            else:
                x, y = self.dot_pos[i - 1]
                self.dot_pos.append([x + self.game.distance, y + self.game.distance])

    def draw_dots(self):
        self.place_dots()
        while self.game.running:
            self.game.screen.fill(self.game.BLACK)
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.game.running = False

                elif event.type == self.pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    for i, (x, y) in enumerate(self.dot_pos):
                        if math.hypot(mouse_x - x, mouse_y - y) < 20:
                            self.game.dragging = True
                            self.game.dragged_index = i
                            break
                elif event.type == self.pygame.MOUSEBUTTONUP:
                    # Stop dragging
                    self.game.dragging = False
                    self.game.dragged_index = -1

            if self.game.dragging and self.game.dragged_index != -1:
                mouse_x, mouse_y = self.pygame.mouse.get_pos()
                self.dot_pos[self.game.dragged_index] = [mouse_x, mouse_y]

            keys = self.pygame.key.get_pressed()
            if keys[self.pygame.K_UP] or keys[self.pygame.K_w]:
                if self.dot_pos[0][1] > 20:
                    self.dot_pos[0][1] -= self.game.speed
            if keys[self.pygame.K_DOWN] or keys[self.pygame.K_s]:
                if self.dot_pos[0][1] < self.game.HEIGHT - 20:
                    self.dot_pos[0][1] += self.game.speed
            if keys[self.pygame.K_LEFT] or keys[self.pygame.K_a]:
                if self.dot_pos[0][0] > 20:
                    self.dot_pos[0][0] -= self.game.speed
            if keys[self.pygame.K_RIGHT] or keys[self.pygame.K_d]:
                if self.dot_pos[0][0] < self.game.WIDTH - 20:
                    self.dot_pos[0][0] += self.game.speed

            if self.move:
                self.auto_move()
            for i in range(1, len(self.dot_pos)):
                dx = self.dot_pos[i][0] - self.dot_pos[i - 1][0]
                dy = self.dot_pos[i][1] - self.dot_pos[i - 1][1]
                distance = math.sqrt(dx**2 + dy**2)

                # k = 10 if self.even else -10
                k = 0
                if distance != 0:
                    dx /= distance
                    dy /= distance
                    self.dot_pos[i][0] = (
                        self.dot_pos[i - 1][0] + dx * self.game.distance + k
                    )
                    self.dot_pos[i][1] = (
                        self.dot_pos[i - 1][1] + dy * self.game.distance + k
                    )
                # self.even = not self.even

            for i in range(len(self.dot_pos)):
                x, y = self.dot_pos[i]
                if i == 0:
                    self.pygame.draw.circle(
                        self.game.screen, self.game.WHITE, (int(x), int(y)), 20, 5
                    )
                else:
                    x_, y_ = self.dot_pos[i - 1]
                    self.pygame.draw.circle(
                        self.game.screen,
                        self.game.WHITE,
                        (int(x), int(y)),
                        20 // i + 5,
                        5,
                    )
            if self.dots and len(self.dots) > 1:
                for i in range(1, len(self.dots)):
                    x1, y1 = self.dots[i - 1]
                    x2, y2 = self.dots[i]
                    self.pygame.draw.line(
                        self.game.screen,
                        self.game.MAGENTA,
                        (int(x1), int(y1)),
                        (int(x2), int(y2)),
                        2,
                    )

            self.dots.append((int(self.dot_pos[-1][0]), int(self.dot_pos[-1][1])))
            self.pygame.display.update()
            self.game.clock.tick(self.game.FPS)

        self.pygame.quit()

    def auto_move(self):
        start_x = self.game.WIDTH // 2
        start_y = self.game.HEIGHT // 2

        if self.num > 300:
            self.boundary = True

        if self.boundary:
            self.num -= random.randint(1, 10)
            if self.num < 150:
                self.boundary = False
        else:
            self.num += random.randint(1, 10)
        self.dot_pos[0][0] = start_x + (450 + self.num) * math.cos(self.game.velocity)
        self.dot_pos[0][1] = start_y + (50 + self.num) * math.sin(self.game.velocity)

        self.game.velocity += 0.02


game = PygameInit(distance=20, speed=5)
num_dots = 20
animation = Animation(num_dots, game, move=True)
animation.draw_dots()
