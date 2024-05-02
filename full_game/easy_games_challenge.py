import copy
from board import boards
import pygame
import math
pygame.init()
import pygame
import random
import os
import pygame
from pygame.locals import *
import random
pygame.init()
run3 = False
run = True
end_game = False
clock = pygame.time.Clock()
fps = 60
score_counter = 0
screen_width = 1200
screen_height = 800
flappy_start = pygame.image.load('images\start_flappy.jpg')
flappy_win = pygame.image.load('images\\15.jpg')
flappy_start_cycle = True
flappy_surface = pygame.Surface((240, 115), pygame.SRCALPHA)  # Создаем поверхность с альфа-каналом
flappy_surface.fill((255, 0, 0, 128))  # Заполняем красным цветом с
flappy_to_pac_surface = pygame.Surface((100, 100), pygame.SRCALPHA)  # Создаем поверхность с альфа-каналом
flappy_to_pac_surface.fill((255, 0, 0, 128))  # Заполняем красным цветом с
font = pygame.font.Font(None, 36)

# Цвет текста
flappy_text_color = (255, 255, 255)

# Создание текстовой поверхности
flappy_text_surface = font.render("10 points to pass", True, flappy_text_color)

# Получение прямоугольника, ограничивающего текст
flappy_text_rect = flappy_text_surface.get_rect()

# Положение текста
flappy_text_rect.center = (110, 20)       
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')
#define font
font = pygame.font.SysFont('Bauhaus 93', 60)

#define colours
white = (255, 255, 255)

#define game variables
ground_scroll = -1200
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 300
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False


#load images
flappy_bg = pygame.image.load('images\\799254_flappy_generator_plus_create_your_own_flappy_bird_game_9600x950.png')
ground_img = pygame.image.load('images\hz-removebg-preview.png')
button_img = pygame.image.load('images/restart.png')
numbers = [pygame.image.load('images\\0.png'), pygame.image.load('images\\1.png'),
           pygame.image.load('images\\2.png'), pygame.image.load('images\\3.png'),
           pygame.image.load('images\\4.png'), pygame.image.load('images\\5.png'),
           pygame.image.load('images\\6.png'), pygame.image.load('images\\7.png'),
           pygame.image.load('images\8.png'), pygame.image.load('images\9.png')]
# Dictionary to store numbers and their corresponding images
number_images = {0: numbers[0], 1: numbers[1], 2: numbers[2], 3: numbers[3],
                 4: numbers[4], 5: numbers[5], 6: numbers[6], 7: numbers[7],
                 8: numbers[8], 9: numbers[9]}
for i in range(10):
    if number_images[i] is None:
        print(f"Image {i} is not loaded.")
# Function to draw the score using number images
def draw_score(score):
    score_str = str(score)
    x = int(screen_width / 2) - 30 * len(score_str) / 2
    y = 20
    for digit in score_str:
        screen.blit(number_images[int(digit)], (x, y))
        x += 30  

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function for debug output
def debug_output():
    print("Debug output - score:", score)

def reset_game():
    global score
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score

class Bird(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        img = pygame.image.load(f"images/pixil-frame-0 (3).png")
        self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            flap_cooldown = 5
            self.counter += 1
            
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):

    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/pipe (1).png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

button_flappy = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

flappy_run = False
# Set up the window
WIDTH = 900
HEIGHT = 950
font = pygame.font.Font(None, 36)
menu = pygame.image.load('pacmanmenu.jpg')
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
timer = pygame.time.Clock()
space_surface = font.render("Press Space to Restart", True, "white")
space_rect = space_surface.get_rect(center=(625,500))
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(boards)
color = 'blue'
PI = math.pi
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))
blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (85, 85))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (85, 85))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (85, 85))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (85, 85))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (65, 65))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (85, 85))
button = pygame.image.load('images\IMG_6475-removebg-preview-removebg-preview.png')
victory_image = pygame.image.load('15.jpg').convert_alpha()
scaled_width = victory_image.get_width() // 4
scaled_height = victory_image.get_height() // 4
scaled_image = pygame.transform.scale(victory_image, (950, 600))
pac_surface = pygame.Surface((100, 100), pygame.SRCALPHA)  # Создаем поверхность с альфа-каналом
pac_surface.fill((255, 0, 0, 128))  # Заполняем красным цветом с       
center_x = (900 - scaled_width) // 2
center_y = (950 - scaled_height) // 2
        
screen.blit(scaled_image, (center_x, center_y))
player_x = 450
player_y = 663
direction = 0
blinky_x = 56
blinky_y = 58
blinky_direction = 0
inky_x = 440
inky_y = 388
inky_direction = 2
pinky_x = 440
pinky_y = 438
pinky_direction = 2
clyde_x = 440
clyde_y = 438
clyde_direction = 2
counter = 0
flicker = False
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False
blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False
moving = False
ghost_speeds = [2, 2, 2, 2]
startup_counter = 0
lives = 3
game_over = False
game_won = False
green_surface = pygame.Surface((240, 115), pygame.SRCALPHA)  # Создаем поверхность с альфа-каналом
green_surface.fill((0, 255, 0, 200))  # Заполняем красным цветом с
begin_surface = pygame.Surface((100, 100), pygame.SRCALPHA)  # Создаем поверхность с альфа-каналом
begin_surface.fill((0, 255, 0, 200))
start_surface = pygame.Surface((390, 145), pygame.SRCALPHA)  # Создаем поверхность с альфа-каналом
start_surface.fill((0, 255, 0, 200))# Заполняем красным цветом с
runer2 = False
runer3 = True
run3 = False
screen = pygame.display.set_mode((WIDTH, HEIGHT))
window = pygame.display.set_mode((1200, 800))
window_del = True
end_game = False
run_0 = True
start_agree = False
start_frame_counter = 0
start_frame = pygame.image.load('images\Arnur\'s Mission Glasses Recovery (2).jpg')
starting_frames = ['images\\2.jpg',
                   'images\\3.jpg',
                   'images\\4.jpg',
                   'images\\5.jpg',
                   'images\\6.jpg',
                   'images\\7.jpg',
                   'images\8.jpg',
                   'images\9.jpg',
                   'images\9.jpg'
                   ]
while run_0:
    #pygame.draw.rect(screen,"red",(500,300,200,100))
    if not start_agree:
        screen.blit(pygame.image.load('images\Arnur\'s Mission Glasses Recovery (2).jpg'),(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_0 = False
            runer2 =  False
            runer3 = False
            run3 = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if begin_surface.get_rect(topleft=(1000,600)).collidepoint(event.pos):
                    start_frame_counter +=1
                elif start_surface.get_rect(topleft=(405,390)).collidepoint(event.pos):
                    start_agree = True
    if start_frame_counter == 8:
        run_0 = False
        run = False
        flappy_start_cycle = True
    if start_agree:
        screen.blit(pygame.image.load(starting_frames[start_frame_counter]),(0,0))
        screen.blit(button,(1000,600))
    #pygame.draw.rect(screen,"red",(405,390,390,145))
    pygame.display.update()
class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_clyde(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_blinky(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_inky(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_pinky(self):

        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction


def draw_misc():
    global game_over, window_del, run3, run, end_game
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    
     
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
    
    if game_over:
        # Load game over PNG image
        game_over_image = pygame.image.load('14.jpg').convert_alpha()
        scaled_width = game_over_image.get_width() // 4
        scaled_height = game_over_image.get_height() // 4
        scaled_image = pygame.transform.scale(game_over_image, (950, 600))
        window_del = False
        # Calculate position to center the image on the screen
        center_x = (900 - scaled_width) // 2
        center_y = (950 - scaled_height) // 2
        screen.fill("white")
        screen.blit(scaled_image, (0, 150))  # Draw centered scaled image
        
        # Add Yes and No buttons
        button_yes = pygame.image.load('yes.png').convert_alpha()
        button_no = pygame.image.load('no.png').convert_alpha()
        
        # Calculate positions for buttons
        button_yes_x = 220
        button_no_x = 570
        button_y = 550
        
        screen.blit(button_yes, (button_yes_x, button_y))
        screen.blit(button_no, (button_no_x, button_y))
        
        pygame.display.update()

        # Event handling for game over screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Check if Yes button is clicked
                if button_yes_x <= mouse_x <= button_yes_x + button_yes.get_width() and \
                   button_y <= mouse_y <= button_y + button_yes.get_height():
                    # Restart the game
                    game_over = False
                    # Reset game state as needed
                    # restart_game()  # Implement your game restart logic
                    
                # Check if No button is clicked
                elif button_no_x <= mouse_x <= button_no_x + button_no.get_width() and \
                     button_y <= mouse_y <= button_y + button_no.get_height():
                    pygame.quit()
                    quit()  # Exit the game
    
    if game_won:
        run3 = True
        run = False
        end_game = True
        

def check_collisions(scor, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scor, power, power_count, eaten_ghosts


def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


def draw_player():
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(play_x, play_y):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y


def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]
runer2 = False
W, H = 1200, 800
FPS = 60
game_score = 0
paused = True
coun = 0
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
clock = pygame.time.Clock()
bg = (0, 0, 0)
left_a = 410
left_d = 540
barrier = False
# Load block images from directory
shields = []
block_images = []
block_directory = 'unbg'
shield = pygame.image.load('images\image (2).png')
shield_icon = pygame.image.load('images\icon_shield.png')
for filename in os.listdir(block_directory):
    if filename.endswith(".png"):
        image = pygame.image.load(os.path.join(block_directory, filename)).convert_alpha()  # Load with alpha channel
        block_images.append(image)
red_surface = pygame.Surface((100, 100), pygame.SRCALPHA)  # Создаем поверхность с альфа-каналом
red_surface.fill((255, 0, 0, 128))  # Заполняем красным цветом с
green_surface = pygame.Surface((200, 120), pygame.SRCALPHA)  # Создаем поверхность с альфа-каналом
green_surface.fill((0, 255, 0, 200))  # Заполняем красным цветом с
# Bonus coffee
bonus_coffee = pygame.image.load('images\cofe.png')
coffe_life = pygame.image.load('images\coffee.png')
red_balls = []
################################################################################################
bg_window = pygame.image.load('images\windows_xp_original-wallpaper-1280x800-transformed.jpeg')
first_frame = pygame.image.load('images\\10 (3).jpg')
second_frame = pygame.image.load('images\\11.jpg')
shield_picked_up = False
shield_pickup_time = None
# Function to create red balls
def create_shield(x, y):
    red_ball_rect = pygame.Rect(x, y, 100, 100)  # Size of the red ball
    if not any(shield1['rect'] == red_ball_rect for shield1 in shields):
        red_balls.append({'rect': red_ball_rect, 'speed': 2, 'radius': 5})

def create_red_ball(x, y):
    shield_ball_rect = pygame.Rect(x, y, 100, 100)  # Size of the red ball
    if not any(ball['rect'] == shield_ball_rect for ball in red_balls):
        shields.append({'rect': shield_ball_rect, 'speed': 2, 'radius': 5})

# Function to update red balls
def update_red_balls():
    global red_balls, H, sp,sp2,coffe_counter
    for ball in red_balls:
        ball['rect'].y += ball['speed']
        # Remove balls that go out of the screen
        if ball['rect'].top > H:
            red_balls.remove(ball)
        else:
            screen.blit(bonus_coffee, ball['rect'])
            # Check collision with paddle
            if paddle.colliderect(ball['rect']):
                sp += 1
                sp2 = sp2 + 1
                coffe_counter +=1
                red_balls.remove(ball)
                coin_colision_sound.play()
def update_shields():
    global shields, H, shield_picked_up, shield_pickup_time, barrier, coun
    for shield1 in shields:
        shield1['rect'].y += shield1['speed']
        # Remove shields that go out of the screen
        if shield1['rect'].top > H:
            shields.remove(shield1)
        else:
            screen.blit(shield_icon, shield1['rect'])
            # Check collision with paddle
            if paddle.colliderect(shield1['rect']):
                shields.remove(shield1)
                coin_colision_sound.play()
                barrier = True
sound_played = False
timer2 = False
frame2 = True
agree = True
timer = True
player = True
win_agree = True
coffe1  = False
coffe2 = False
coffe3 = False
unloose = True
second_chance = False
retry = True
new_game = False
timer2 = False
space_agree = False
passed_agree = True
frame3 = True
sp = 5
sp2 = 0
coffe_counter = 0
# Paddle settings
paddleW = 185
paddleH = 1
paddleSpeed = 20 + sp
paddle_surface = pygame.Surface((paddleW, paddleH), pygame.SRCALPHA)  # Create surface with alpha channel
paddle = paddle_surface.get_rect(center=(W // 2, H - paddleH - 50))  # Center paddle
pygame.draw.rect(paddle_surface, (255, 255, 255, 0), paddle)  # Draw transparent rectangle on surface
passed_after = False
# CD settings
cd_image_path = 'images\cd_ball.png'
glass_paddle = pygame.image.load('images\Remove-bg.ai_1713611941284.png')
wasted_sound = pygame.mixer.Sound('audio\gta-v-wasted-101soundboards (mp3cut.net) (1).mp3')
passed_sound = pygame.mixer.Sound('audio\gta-san-andreas-mission-passed-made-with-Voicemod.mp3')
button = pygame.image.load('images\IMG_6475-removebg-preview-removebg-preview.png')
cd = pygame.image.load(cd_image_path)
cd_radius = 50
cd_rect = cd.get_rect()
cd_ball = pygame.Rect(random.randrange(cd_rect.width, W - cd_rect.width), H // 2, cd_rect.width, cd_rect.height)
bonus_cd = pygame.Rect(random.randrange(cd_rect.width, W - cd_rect.width), H // 2, cd_rect.width, cd_rect.height)

ballSpeed = 6
dx, dy = 1, -1
frames = ['images\\10 (3).jpg','images\\11.jpg','images\\21.jpg']
frame_counter = 0
game_font = pygame.font.SysFont('comicsansms', 50, True)
settings_text = game_font.render('Settings', True, 'Black')

# Game score
game_score = 0
game_score_font = pygame.font.SysFont('comicsansms', 40)
game_score_text = game_score_font.render(f'Your game score is: {game_score}', True, ("black"))
game_score_rect = game_score_text.get_rect()
game_score_rect.center = (210, 20)

# Catching sound
collision_sound = pygame.mixer.Sound('audio\zvuk-podkljuchenija-usb-windows-10.mp3')
colision_sound2 = pygame.mixer.Sound('audio\zvuk-otkljuchenija-usb-windows-10.mp3')
coin_colision_sound = pygame.mixer.Sound('audio\Coin_Pick (mp3cut.net) (2).mp3')
cls1 = True
clss2 = False

def detect_collision(dx, dy, cd_ball, rect):
    if dx > 0:
        delta_x = cd_ball.right - rect.left
    else:
        delta_x = rect.right - cd_ball.left
    if dy > 0:
        delta_y = cd_ball.bottom - rect.top
    else:
        delta_y = rect.bottom - cd_ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    if delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy
frame = False
# Load block positions
block_list = [pygame.Rect(10 + 120 * i, 50 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
block_flags = [False] * len(block_list)
blocks = [(random.choice(block_images), block_pos) for block_pos in block_list]

# Game over Screen
lose_font = pygame.font.SysFont('comicsansms', 40)
lose_text = lose_font.render('Game Over', True, (255, 255, 255))
lose_text_rect = lose_text.get_rect()
lose_text_rect.center = (W // 2, H // 2)
wasted = pygame.image.load('images\mission_failed-removebg-preview.png')
passed = pygame.image.load('images\mission_passed-removebg-preview.png')

# Win Screen
win_font = pygame.font.SysFont('comicsansms', 40)
win_text = win_font.render('You win', True, (0, 0, 0))
win_text_rect = win_text.get_rect()
win_text_rect.center = (W // 2, H // 2)
counter = 0
done = True
flappy_pac = False
bottom_barrier_visible = False
bottom_barrier_time = 0
while flappy_start_cycle:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flappy_start_cycle = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if flappy_surface.get_rect(topleft=(480,520)).collidepoint(event.pos):
                    flappy_start_cycle = False
                    flappy_run = True
    screen.blit(flappy_start,(0,0))
    #pygame.draw.rect(screen,"red",(480,520,240,115))
    pygame.display.update()
while flappy_run:
    clock.tick(fps)

    screen.blit(flappy_bg,(0,0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()

    #screen.blit(ground_img, (400, 450))

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.right > pipe_group.sprites()[0].rect.right\
            and bird_group.sprites()[0].rect.left < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                score_counter +=1
                print("Score:", score)
                pass_pipe = False
    screen.blit(flappy_text_surface, flappy_text_rect)
    draw_score(score)
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False
    if score_counter == 10:
        flappy_run = False
        runer2 = True
    if flying == True and game_over == False:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
    
        pipe_group.update()

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
    if game_over == True:
        if button_flappy.draw():
            game_over = False
            score = reset_game()
            score_counter = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flappy_run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    pygame.display.update()
flappy_pac = True
while runer2:
    WIDTH = 1200
    HEIGHT = 800
    run = False
    flappy_to_pac_surface = pygame.Surface((100, 100), pygame.SRCALPHA)  # Создаем поверхность с альфа-каналом
    flappy_to_pac_surface.fill((255, 0, 0, 255))  # Заполняем красным цветом с 
    #screen2 = pygame.display.set_mode((1200, 800))
    if  flappy_pac:
        screen.blit(flappy_win,(0,0))
    if not flappy_pac:
        screen.blit(menu,(0,0))
    #pygame.draw.rect(screen,"red",(493,635,240,115))
    if flappy_pac:
        screen.blit(button,(1000,600))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runer2 = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if green_surface.get_rect(topleft=(493, 635)).collidepoint(event.pos):
                     runer2 = False
                     run = True
                     HEIGHT = 950
                     WIDTH = 900
                     screen = pygame.display.set_mode((WIDTH, HEIGHT))
                elif button.get_rect(topleft=(1000,600)).collidepoint(event.pos):
                    flappy_pac = False
                    
    #pygame.draw.rect(screen,"red",(1000,600,11))
    pygame.display.update()      
while run:
    clock.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black')
    draw_board()
    center_x = player_x + 23
    center_y = player_y + 24
    if powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    if eaten_ghost[0]:
        ghost_speeds[0] = 2
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2
    if blinky_dead:
        ghost_speeds[0] = 4
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)
    draw_player()
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead,
                   blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_img, inky_direction, inky_dead,
                 inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead,
                  pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_img, clyde_direction, clyde_dead,
                  clyde_box, 3)
    draw_misc()
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)

    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)
    if not powerup:
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                (player_circle.colliderect(inky.rect) and not inky.dead) or \
                (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                (player_circle.colliderect(clyde.rect) and not clyde.dead):
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    if powerup and player_circle.colliderect(blinky.rect) and eaten_ghost[0] and not blinky.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(inky.rect) and eaten_ghost[1] and not inky.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(pinky.rect) and eaten_ghost[2] and not pinky.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[3] and not clyde.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0]:
        blinky_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[1]:
        inky_dead = True
        eaten_ghost[1] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2]:
        pinky_dead = True
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3]:
        clyde_dead = True
        eaten_ghost[3] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                run3 = True
                run = False
                end_game = True
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_1:
                game_over = True
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                score = 0
                lives = 3
                level = copy.deepcopy(boards)
                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    if blinky.in_box and blinky_dead:
        blinky_dead = False
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False

    pygame.display.flip()       
    
if end_game:
    while run3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run3 = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pac_surface.get_rect(topleft=(740,640)).collidepoint(event.pos):
                        runer2 = True
                        run3 = False
            screen.fill("White")
            screen.blit(scaled_image,(0,150))
            screen.blit(button,(740,640))
            #pygame.draw.rect(screen,"red",(740,640,100,100))
        pygame.display.update()
if runer2:
    WIDTH = 1200
    HEIGHT = 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    while runer2:
        done = True
        screen.blit(pygame.image.load('images\\arkanoid.jpg'),(0,0))
        #pygame.draw.rect(screen,"red",(470,610,250,120))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runer2 = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if green_surface.get_rect(topleft=(500, 600)).collidepoint(event.pos):
                        done = False
                        runer2 = False
        pygame.display.update()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if red_surface.get_rect(topleft=(1000,600)).collidepoint(event.pos):
                    frame_counter +=1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
                pygame.display.update()
            if space_agree:
                space_agree = False
                if event.key == pygame.K_SPACE:
                    retry = False
                    new_game = True
            if not paused:
                if event.key == pygame.K_1:
                    paddleW = 200
                    paddle_surface = pygame.Surface((paddleW, paddleH), pygame.SRCALPHA)
                    paddle = paddle_surface.get_rect(center=(W // 2, H - paddleH - 30))
                    pygame.draw.rect(paddle_surface, (255, 255, 255, 0), paddle)
                    cd_ball = pygame.Rect(random.randrange(cd_rect.width, W - cd_rect.width), H // 2, cd_rect.width, cd_rect.height)
                elif event.key == pygame.K_2:
                    paddleW = 300
                    paddle_surface = pygame.Surface((paddleW, paddleH), pygame.SRCALPHA)
                    paddle = paddle_surface.get_rect(center=(W // 2, H - paddleH - 30))
                    pygame.draw.rect(paddle_surface, (255, 255, 255, 0), paddle)
                    cd_ball = pygame.Rect(random.randrange(cd_rect.width, W - cd_rect.width), H // 2, cd_rect.width, cd_rect.height)
                elif event.key == pygame.K_3:
                    paddleW = 150
                    paddle_surface = pygame.Surface((paddleW, paddleH), pygame.SRCALPHA)
                    paddle = paddle_surface.get_rect(center=(W // 2, H - paddleH - 30))
                    pygame.draw.rect(paddle_surface, (255, 255, 255, 0), paddle)
                    cd_ball = pygame.Rect(random.randrange(cd_rect.width, W - cd_rect.width), H // 2, cd_rect.width, cd_rect.height)
                elif event.key == pygame.K_SPACE:
                    cd_radius += 10
                    cd_ball = pygame.Rect(random.randrange(cd_rect.width, W - cd_rect.width), H // 2, cd_rect.width, cd_rect.height)
                elif event.key == pygame.K_s:
                    paddleSpeed += 20
                elif event.key == pygame.K_r:
                    paused = True
    if new_game:
        game_score = 0
        coffe_counter = 0
        coffe1 = False
        coffe2 = False
        coffe3 = False
        block_list = [pygame.Rect(10 + 120 * i, 50 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
        block_flags = [False] * len(block_list)
        blocks = [(random.choice(block_images), block_pos) for block_pos in block_list]
        cd_ball = pygame.Rect(random.randrange(cd_rect.width, W - cd_rect.width), H // 2, cd_rect.width, cd_rect.height)
        new_game = False
        retry = True
    if coffe_counter == 1:
        coffe1 = True
    if coffe_counter == 2:
        coffe2 = True
    if coffe_counter == 3:
        coffe3 = True
        unloose = False
        second_chance = True
    if coffe_counter != 3:
        second_chance = False
        unloose = True
    if coffe_counter > 3:
        coffe_counter = 3
    screen.blit(bg_window, (0, 0))
    if paused:
        for block_image, block_pos in blocks:
            screen.blit(block_image, block_pos)
        screen.blit(paddle_surface, paddle)
        screen.blit(cd, cd_ball)
        if coffe1:
            screen.blit(coffe_life, (1050, 0))
        if coffe2:
            screen.blit(coffe_life, (1100, 0))
        if coffe3:
            screen.blit(coffe_life, (1150, 0))
    # Ball movement
    if paused:
        cd_ball.x += ballSpeed * dx
        cd_ball.y += ballSpeed * dy
    # Collision left
    if cd_ball.centerx < cd_radius or cd_ball.centerx > W - cd_radius:
        dx = -dx
    # Collision top
    if cd_ball.centery < cd_radius + 50:
        dy = -dy
    # Collision with paddle
    if cd_ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, cd_ball, paddle)
    # Collision blocks
    hit_index = cd_ball.collidelist(block_list)

    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, cd_ball, hit_rect)
        game_score += 1
        if win_agree:
            if cls1:
                collision_sound.play()
                cls1 = False
                cls2 = True
            elif cls2:
                colision_sound2.play()
                cls1 = True
                cls2 = False
        if random.random() < 0.1:  #10% chance
            create_red_ball(hit_rect.centerx, hit_rect.centery)
        block_flags[hit_index] = True
        del blocks[hit_index]
        if random.random() < 0.1:  #10% chance
            create_shield(hit_rect.centerx, hit_rect.centery)
        block_flags[hit_index] = True
    update_red_balls()
    update_shields()
    if paused:
        for red_ball in red_balls:
            screen.blit(bonus_coffee, red_ball['rect'])

    # Game score
    if paused:
        game_score_text = game_score_font.render(f'Your game score is: {game_score}', True, ("black"))
        screen.blit(game_score_text, game_score_rect)
        screen.blit(glass_paddle, (left_a, left_d))
    # Win/lose screens
    if cd_ball.bottom > 1000:
            barrier = False
            if second_chance:
                coffe_counter = 0
                cd_ball = pygame.Rect(random.randrange(cd_rect.width, W - cd_rect.width), H // 2, cd_rect.width, cd_rect.height)
                coffe1 = False
                coffe2 = False
                coffe3 = False
            if unloose:
                if win_agree:
                    if retry:
                        screen.fill("black")
                        if timer:
                            time = pygame.time.get_ticks()
                            timer = False
                        if pygame.time.get_ticks() - time > 2500:
                            space_agree = True
                            screen.blit(wasted, (375, 150))
                            screen.blit(space_surface, space_rect)
                        pygame.display.update()
                        if player:
                            wasted_sound.play()
                            player = False
    elif not len(block_list):
        screen.fill((0, 0, 0)) 
        screen.blit(passed,(350,150))
        if passed_agree:
            pygame.display.update()
        win_agree = False
        if timer:
            time = pygame.time.get_ticks()
            timer = False
        if pygame.time.get_ticks() - time > 5000:
            passed_after = True
            passed_agree = False
        if agree:
            passed_sound.play()
            agree = False
        
        #screen.blit(win_text, win_text_rect)
    # Paddle Control
    if paused:
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddleSpeed
        if key[pygame.K_RIGHT] and paddle.right < W:
            paddle.right += paddleSpeed
    if paused:
        if key[pygame.K_LEFT] and left_a > -75:
            left_a = left_a - 20 - sp + sp2
        if key[pygame.K_RIGHT] and left_a < 900:
            left_a = left_a + 20 + sp - sp2

    # Display shield if picked up
    # Display bottom barrier if visible
    if barrier:
        if win_agree:
            screen.blit(shield, (0, 768))
            pygame.draw.rect(screen, (0, 0, 0), (0, H - 1, W, 1))
    # Check collision of CD ball with the barrier
    if barrier:
      if cd_ball.colliderect(pygame.Rect(0, H - 1, W, 1)):
         dx, dy = detect_collision(dx, dy, cd_ball, pygame.Rect(0, H - 1, W, 1))
         barrier = False
    if passed_after:
        screen.blit(pygame.image.load(frames[frame_counter]), (0, 0))
        screen.blit(button,(1000,600))
        pygame.display.update()  
    if win_agree:
        pygame.display.flip()
    clock.tick(fps)