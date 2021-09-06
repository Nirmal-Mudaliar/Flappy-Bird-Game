import pygame, random
import sys


def draw_floor():
    display_surface.blit(floor_surface, (floor_x_pos, 420))
    display_surface.blit(floor_surface, (floor_x_pos + 288, 420))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    botttom_pipe = pipe_surface.get_rect(midtop=(350, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(350, random_pipe_pos - 150))
    return botttom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            display_surface.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            display_surface.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 512:
        death_sound.play()
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 5, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        display_surface.blit(score_surface, score_rect)

    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        display_surface.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(144, 400))
        display_surface.blit(high_score_surface, high_score_rect)


def update_score(score, highscore):
    if score > highscore:
        highscore = score

    return highscore


# pygame.mixer.pre_init(frequency=10410, size=16, channels=1, buffer=700)

# initialize pygame
pygame.init()

WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
game_font = pygame.font.Font("fonts/04B_19.TTF", 20)

# Game Variables
gravity = 0.2
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load("images/background-night.png").convert()

floor_surface = pygame.image.load("images/base.png").convert()
floor_x_pos = 0

bird_downflap = pygame.image.load("images/bluebird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("images/bluebird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("images/bluebird-upflap.png").convert_alpha()
bird_index = 0
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 50)

pipe_surface = pygame.image.load("images/pipe-green.png")
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 300, 360, 230, 390]

game_over_surface = pygame.image.load("images/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144, 245))

# Flap-sound
flap_sound = pygame.mixer.Sound("audio/wing.wav")
death_sound = pygame.mixer.Sound("audio/hit.wav")
score_sound = pygame.mixer.Sound("audio/point.wav")

score_sound_countdown = 0

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 190)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
        bird_surface, bird_rect = bird_animation()

    display_surface.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        display_surface.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        score += 0.01
        score_display("main_game")
        score_sound_countdown -= 0.1
        # if score_sound_countdown <= 0:
        #     score_sound.play()
        # else:
        #     score_sound_countdown = 100
    else:
        display_surface.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")
    # Floor
    floor_x_pos -= 0.4
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)
