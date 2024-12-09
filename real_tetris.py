from os import path
import pygame
import random
from color_list import *
import sys
from shape_list import shape_dict

HEIGHT = 600
WIDTH = 400
FPS = 30
GRID_WIDTH, GRID_HEIGHT = 10, 24

running = True

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
#pygame.display.set_icon() for later

src_dir = path.join(path.dirname(__file__), 'src')
ui_radius_img = pygame.image.load(path.join(src_dir, 'ui_radius.png')).convert()

ui_group = pygame.sprite.Group()


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.hover_color if self.active else self.color, self.rect)
        font = pygame.font.SysFont("Arial", 24)
        text_surface = font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (
            self.rect.centerx - text_surface.get_width() // 2, self.rect.centery - text_surface.get_height() // 2))

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False


class Menu:
    def __init__(self):
        self.buttons = [
            Button(WIDTH / 2 - 100, 200, 200, 50, "Play", (0, 255, 0), (0, 200, 0)),
            Button(WIDTH / 2 - 100, 300, 200, 50, "Options", (0, 0, 255), (0, 0, 200)),
            Button(WIDTH / 2 - 100, 400, 200, 50, "Quit", (255, 0, 0), (150, 0, 0))
        ]
        self.state = "menu"

    def draw(self, screen):
        screen.fill(BLACK)
        for button in self.buttons:
            button.draw(screen)

        font = pygame.font.Font(None, 64)
        title = font.render("Jektris", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

    def handle_events(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.active = button.check_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.check_click(event.pos):
                    if button.text == "Play":
                        self.state = "game"
                        print("game selected")
                    elif button.text == "Options":
                        print("Options selected")
                    elif button.text == "Quit":
                        pygame.quit()
                        sys.exit()


class Jektris:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.cell_size = 25
        self.shape = self.get_shape()
        self.shape_x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.shape_y = 0
        self.running = True
        self.last_fall = pygame.time.get_ticks()
        self.fall_delay = 1000
        self.current_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.shape_x > 0:

                self.shape_x -= 1
            elif event.key == pygame.K_RIGHT and self.shape_x + len(self.shape[0]) < GRID_WIDTH:
                self.shape_x += 1
            elif event.key == pygame.K_DOWN:
                self.fall_delay = 200
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.fall_delay = 1000
        if event.type == pygame.QUIT:
            self.running = False
            menu.state = "menu"

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(screen, GRAY,
                                 pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                if self.grid[y][x] == 0:
                    pygame.draw.rect(screen, WHITE,
                                     pygame.Rect(x * self.cell_size + 2, y * self.cell_size + 2, self.cell_size - 2,
                                                 self.cell_size - 2))
                elif self.grid[y][x] == 1:
                    pygame.draw.rect(screen, RED,
                                     pygame.Rect(x * self.cell_size + 2, y * self.cell_size + 2, self.cell_size - 2,
                                                 self.cell_size - 2))
                elif self.grid[y][x] == 2:
                    pygame.draw.rect(screen, GREEN,
                                     pygame.Rect(x * self.cell_size + 2, y * self.cell_size + 2, self.cell_size - 2,
                                                 self.cell_size - 2))
                elif self.grid[y][x] == 3:
                    pygame.draw.rect(screen, BLUE,
                                     pygame.Rect(x * self.cell_size + 2, y * self.cell_size + 2, self.cell_size - 2,
                                                 self.cell_size - 2))
                elif self.grid[y][x] == 4:
                    pygame.draw.rect(screen, YELLOW,
                                     pygame.Rect(x * self.cell_size + 2, y * self.cell_size + 2, self.cell_size - 2,
                                                 self.cell_size - 2))
                elif self.grid[y][x] == 5:
                    pygame.draw.rect(screen, CYAN,
                                     pygame.Rect(x * self.cell_size + 2, y * self.cell_size + 2, self.cell_size - 2,
                                                 self.cell_size - 2))
                elif self.grid[y][x] == 6:
                    pygame.draw.rect(screen, ORANGE,
                                     pygame.Rect(x * self.cell_size + 2, y * self.cell_size + 2, self.cell_size - 2,
                                                 self.cell_size - 2))
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def get_shape(self):
        key_shape = ["I", "O", "J", "T", "S", "Z", "L"]
        key_color = [1, 2, 3, 4, 5, 6]
        shape = shape_dict[random.choice(key_shape)]
        color = random.choice(key_color)

        for y in range(len(shape)):
            for x in range(len(shape[y])):
                if shape[y][x] == 1:
                    shape[y][x] = color

        return shape

    def draw_shape(self, shape):
        for y in range(len(shape)):
            for x in range(len(shape[y])):
                self.grid[y + self.shape_y][x + self.shape_x] = shape[y][x]

    def draw(self):
        screen.fill(BLACK)
        self.draw_shape(self.shape)
        self.draw_grid()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            if pygame.time.get_ticks() - self.last_fall > self.fall_delay:
                self.last_fall = pygame.time.get_ticks()
                self.shape_y += 1
            self.draw()
            pygame.display.flip()


menu = Menu()
game = Jektris()
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        menu.handle_events(event)
    if menu.state == "menu":
        menu.draw(screen)
    elif menu.state == "game":
        game.run()
        game = Jektris()
    pygame.display.flip()
pygame.quit()