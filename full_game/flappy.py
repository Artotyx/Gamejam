import pygame
from pygame.locals import *
import random

pygame.init()

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
bg = pygame.image.load('images\\799254_flappy_generator_plus_create_your_own_flappy_bird_game_9600x950.png')
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

button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

flappy_run = False
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
    pygame.draw.rect(screen,"red",(480,520,240,115))
    pygame.display.update()
while flappy_run:
    clock.tick(fps)

    screen.blit(bg, (0,0))

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

    draw_score(score)
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False
    if score_counter == 5:
        flappy_run = False
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
        if button.draw():
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flappy_run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    pygame.display.update()

pygame.quit()
