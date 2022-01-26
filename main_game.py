import pygame
import random
import sys
import pathlib as pth


def get_player_name():
    file_curr = pth.Path("data.txt")
    if not file_curr.is_file():
        with open("data.txt", "w+") as file_out:
            file_out.write("DEFAULT_NAME")
        return "DEFAULT_NAME"
    else:
        with open("data.txt", "r") as file_out:
            return file_out.read().strip()




def show_score(game_state):
    if game_state == 1:
        score_surface = font.render(str(int(score)), True, WHITE_COLOR)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, 25))
        screen.blit(score_surface, score_rect)

    if game_state == 2:
        score_surface = font.render(f'Score: {int(score)}', True, WHITE_COLOR)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, 25))
        screen.blit(score_surface, score_rect)

        high_score_surface = font.render(f'High score: {int(highest_score)}', True, WHITE_COLOR)
        high_score_rect = high_score_surface.get_rect(center=(WIDTH // 2, 68))
        screen.blit(high_score_surface, high_score_rect)

        hi_surface = font.render(f'Hi, {get_player_name()}', True, WHITE_COLOR)
        hi_rect = hi_surface.get_rect(center=(WIDTH // 2, HEIGHT - 56))
        screen.blit(hi_surface, hi_rect)


def update_score(scr, high_score):
    return scr if scr > high_score else high_score


def show_floor():
    screen.blit(floor_surface, (floor_x_pos_curr, HEIGHT - 30))
    screen.blit(floor_surface, (floor_x_pos_curr + WIDTH, HEIGHT - 30))


def show_pipes():
    curr_pipe = random.choice([350, 400, 450, 500, 550, 600])

    return pipe_surface.get_rect(midtop=(400, curr_pipe)), pipe_surface.get_rect(midbottom=(400, curr_pipe - 300))


def move_pipes(pipes):
    for each in pipes:
        each.centerx -= 5
    visible_pipes = [el for el in pipes if el.right > -50]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def pipe_score_check():
    global score, can_score

    if pipes_list:
        for each in pipes_list:
            if 95 < each.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if each.centerx < 0:
                can_score = True


def check_collision(pipes):
    global can_score

    for each in pipes:
        if bird_rect.colliderect(each):
            hit_sound.play()
            can_score = True
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= HEIGHT + 100:
        can_score = True
        disappear_sound.play()
        return False

    return True


TITLE = 'Flappy Bird'
WIDTH = 400
HEIGHT = 708
WHITE_COLOR = (255, 255, 255)
BIRD_MOVE = pygame.USEREVENT + 0
CREATE_PIPE = pygame.USEREVENT + 1
SCORE_EVENT = pygame.USEREVENT + 2

pygame.display.set_caption(TITLE)
pygame.display.set_icon(pygame.image.load('assets/flappy_bird_icon.png'))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font('pixel_font.ttf', 40)

# Main and big values
gravity = 0.3
movement = 0
clock_time = 120
game_is_active, can_score = True, True
score, highest_score = 0, 0
pipes_list = []

bird_down = pygame.transform.scale2x(pygame.image.load('assets/red_down.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/red_mid.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/red_up.png').convert_alpha())
bg_surface = pygame.transform.scale2x(pygame.image.load('assets/bg.png').convert())
floor_surface = pygame.transform.scale2x(pygame.image.load('assets/floor.png').convert())
pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe.png'))

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/info.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

floor_x_pos_curr, bird_index_curr = 0, 0

bird_frames = [bird_down, bird_mid, bird_up]
bird_frame_right_now = bird_frames[bird_index_curr]

bird_surface = bird_frames[bird_index_curr]
bird_rect = bird_frame_right_now.get_rect(center=(100, 512))

pygame.time.set_timer(BIRD_MOVE, 200)
pygame.time.set_timer(CREATE_PIPE, 1000)
pygame.time.set_timer(SCORE_EVENT, 100)

hit_sound = pygame.mixer.Sound('sounds/hit_sound.wav')
hit_sound.set_volume(0.4)
move_sound = pygame.mixer.Sound('sounds/move_sound.wav')
move_sound.set_volume(0.6)
score_sound = pygame.mixer.Sound('sounds/score_up_sound.wav')
score_sound.set_volume(0.65)
disappear_sound = pygame.mixer.Sound('sounds/disappear_sound.wav')
disappear_sound.set_volume(0.6)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_is_active:
                movement = -10
                move_sound.play()
            if event.key == pygame.K_SPACE and game_is_active is False:
                game_is_active = True
                pipes_list = []
                bird_rect.center = (10, HEIGHT // 2)
                movement = 0
                score = 0

        if event.type == CREATE_PIPE:
            pipes_list.extend(show_pipes())

        if event.type == BIRD_MOVE:
            if bird_index_curr < 2:
                bird_index_curr += 1
            else:
                bird_index_curr = 0

            bird_surface = bird_frames[bird_index_curr]
            bird_rect = bird_frames[bird_index_curr].get_rect(center=(100, bird_rect.centery))

        if event.type == pygame.MOUSEWHEEL:
            gravity = 0.5
            clock_time = 100
            bird_down = pygame.transform.scale2x(
                pygame.image.load('assets/red_down.png').convert_alpha())
            bird_mid = pygame.transform.scale2x(
                pygame.image.load('assets/blue_mid.png').convert_alpha())
            bird_up = pygame.transform.scale2x(
                pygame.image.load('assets/yellow_up.png').convert_alpha())

            bird_frames = [bird_down, bird_mid, bird_up]

            bg_surface = pygame.transform.scale2x(pygame.image.load('assets/bg_2.png').convert())

        if event.type == pygame.MOUSEMOTION:
            gravity = 0.25
            clock_time = 120
            bird_down = pygame.transform.scale2x(
                pygame.image.load('assets/red_down.png').convert_alpha())
            bird_mid = pygame.transform.scale2x(
                pygame.image.load('assets/red_mid.png').convert_alpha())
            bird_up = pygame.transform.scale2x(
                pygame.image.load('assets/red_up.png').convert_alpha())

            bird_frames = [bird_down, bird_mid, bird_up]

            bg_surface = pygame.transform.scale2x(pygame.image.load('assets/bg.png').convert())

    screen.blit(bg_surface, (0, -100))

    if game_is_active:
        movement += gravity
        rotated_bird = pygame.transform.rotozoom(bird_surface, -movement * 2, 1)
        bird_rect.centery += movement
        screen.blit(rotated_bird, bird_rect)
        game_is_active = check_collision(pipes_list)

        pipes_list = move_pipes(pipes_list)
        draw_pipes(pipes_list)

        pipe_score_check()
        show_score(game_state=1)
    else:
        screen.blit(game_over_surface, game_over_rect)
        highest_score = update_score(score, highest_score)
        show_score(game_state=2)

    floor_x_pos_curr -= 1
    show_floor()
    if floor_x_pos_curr <= -WIDTH:
        floor_x_pos_curr = 0

    pygame.display.update()
    clock.tick(clock_time)
