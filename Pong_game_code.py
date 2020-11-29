import pygame, sys, random


def ball_animation():  # Making things cleaner
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        player_score += 1

    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        opponent_score += 1

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= 1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= 1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= 1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= 1


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)
    if keys[pygame.K_SPACE]:
        if current_time - score_time < 700:
            number_three = game_font.render("3", False, light_grey)
            screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))
        if 700 < current_time - score_time < 1400:
            number_two = game_font.render("2", False, light_grey)
            screen.blit(number_two, (screen_width/2 - 10, screen_height/2 + 20))
        if 1400 < current_time - score_time < 2100:
            number_one = game_font.render("1", False, light_grey)
            screen.blit(number_one, (screen_width/2 - 10, screen_height/2 + 20))

        if current_time - score_time < 2100:
            ball_speed_x, ball_speed_y = 0, 0
        else:
            ball_speed_y = 7 * random.choice((1, -1))
            ball_speed_x = 7 * random.choice((1, -1))
            score_time = None


# General Setup


pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Colors
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)
ball_color = (150, 130, 18)
blue = (0, 0, 128)
red = (200, 0, 0)
purple = (0, 200, 0)

# Game Rectangles
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

# Game Variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# Score Variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

# Sound
pong_sound = pygame.mixer.Sound("pong.mp3")
score_sound = pygame.mixer.Sound("score.mp3")

# Score Timer
score_time = 1

while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    # Game Logic
    ball_animation()
    player_animation()
    opponent_ai()

    # Visuals
    screen.fill(blue)
    pygame.draw.rect(screen, purple, player)
    pygame.draw.rect(screen, purple, opponent)
    pygame.draw.ellipse(screen, red, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

    if score_time:
        ball_restart()

    player_text = game_font.render(f"{player_score}", False, light_grey)
    screen.blit(player_text, (660, 25))

    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text, (600, 25))

    # Updating the window
    pygame.display.flip()
    clock.tick(60)
