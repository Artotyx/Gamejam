import pygame
import random
import os

pygame.init()

# Set up the window
W, H = 1200, 800
FPS = 60
game_score = 0
paused = True
coun = 0
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
clock = pygame.time.Clock()
done = False
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
runer2 = True
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
timer2 = True
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

bottom_barrier_visible = False
bottom_barrier_time = 0
while runer2:
    done = True
    screen.blit(pygame.image.load('images\\arkanoid.jpg'),(0,0))
    #pygame.draw.rect(screen,"red",(600,600,100,120))
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
        #dx, dy = detect_collision(dx, dy, cd_ball, hit_rect)
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
    clock.tick(FPS)