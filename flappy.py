import random
import pygame
import pygame.freetype

pygame.init()
clock = pygame.time.Clock()

# Создаем экран размером 1000x600 пикселей
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('Flappy Bird')

# Загружаем изображение заднего фона и масштабируем его
background_image = pygame.image.load('images/background.jpg')
background_image = pygame.transform.scale(background_image, (1000, 600))

# Загружаем изображение "Game Over" с прозрачным фоном и масштабируем его
game_over_image = pygame.image.load('images/gameover.png').convert_alpha()
game_over_image = pygame.transform.scale(game_over_image, (400, 200))

# Загружаем изображение птицы и трубы, и масштабируем их
bird_image = pygame.image.load('images/pixil-frame-0 (3).png')
wall_image = pygame.image.load('images/pipe.png')
bird_image = pygame.transform.scale(bird_image, (80, 60))
wall_image = pygame.transform.scale(wall_image, (100, 500))

bird_rect = bird_image.get_rect()
bird_rect.center = (300, 300)

font = pygame.freetype.Font(None, 30)

bird_speed = 0
gravity = 0.15
jump = 2  # Уменьшенная сила прыжка

wall_group = pygame.sprite.Group()
spawn_wall_event = pygame.USEREVENT
pygame.time.set_timer(spawn_wall_event, 2000)

game_status = 'game'
score = 0
score_updated = False  # Флаг для отслеживания обновления счета

# Загрузка изображений цифр для отображения счета
score_images = [
    pygame.image.load('images/0.png'),
    pygame.image.load('images/1.png'),
    pygame.image.load('images/2.png'),
    pygame.image.load('images/3.png'),
    pygame.image.load('images/4.png'),
    pygame.image.load('images/5.png'),
    pygame.image.load('images/6.png'),
    pygame.image.load('images/7.png'),
    pygame.image.load('images/8.png'),
    pygame.image.load('images/9.png')
]

def display_score(score):
    # Отображаем текущий счет в верхнем левом углу экрана
    digits = [int(digit) for digit in str(score)]
    x = 10
    y = 10
    for digit in digits:
        screen.blit(score_images[digit], (x, y))
        x += score_images[digit].get_width() + 5

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.passed = False  # Флаг для отслеживания прохождения птицей
        self.score_counted = False  # Флаг для отслеживания засчитанного счета

    def update(self):
        global game_status, score, score_updated
        self.rect.x -= 3

        # Проверяем, прошла ли птица эту трубу
        if self.rect.right < bird_rect.left and not self.passed:
            self.passed = True  # Помечаем трубу как пройденную

        # Проверяем, произошло ли прохождение трубы, и увеличиваем счет
        if self.rect.right < bird_rect.left and not self.score_counted:
            score += 1
            self.score_counted = True  # Помечаем, что счет засчитан
            score_updated = True  # Помечаем, что счет обновлен

        # Если птица столкнулась с трубой, переходим в режим "меню"
        if self.rect.colliderect(bird_rect):
            game_status = 'menu'

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_wall_event:
            # Генерируем случайные высоты для верхней и нижней трубы
            upper_wall_y = random.randint(-150, -50)
            lower_wall_y = upper_wall_y + 700  # Расстояние между трубами

            # Создаем верхнюю трубу
            upper_wall = Wall((1050, upper_wall_y), wall_image)
            wall_group.add(upper_wall)

            # Создаем нижнюю трубу
            lower_wall = Wall((1050, lower_wall_y), pygame.transform.flip(wall_image, False, True))
            lower_wall.passed = False  # Сбрасываем флаг прохождения
            wall_group.add(lower_wall)

    if game_status == 'game':
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bird_speed -= jump
        bird_speed += gravity
        bird_speed = max(-8, min(8, bird_speed))

        bird_rect.centery += int(bird_speed)
        bird_rect.centery = max(0, min(600, bird_rect.centery))

        # Отрисовываем задний фон
        screen.blit(background_image, (0, 0))

        # Отрисовываем птицу и трубы
        screen.blit(bird_image, bird_rect)
        wall_group.update()
        wall_group.draw(screen)

        # Отображаем счет
        display_score(score)
    else:
        # Отрисовываем изображение "Game Over" по центру экрана
        screen.blit(game_over_image, (300, 300))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()