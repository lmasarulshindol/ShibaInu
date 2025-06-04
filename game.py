import pygame
import sys

# Screen dimensions
WIDTH, HEIGHT = 800, 600
FPS = 60

# Logo display settings
LOGO_DURATION = FPS * 2  # total frames for logo screen
LOGO_FADE_STEP = 255 / (LOGO_DURATION / 2)

# States
LOGO = 'logo'
TITLE = 'title'
STAGE1_1 = 'stage1-1'
SETTINGS = 'settings'

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ShibaInu Game')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

state = LOGO
logo_timer = LOGO_DURATION
logo_alpha = 0


def draw_text(text, y, alpha=None):
    rendered = font.render(text, True, (255, 255, 255))
    if alpha is not None:
        rendered.set_alpha(int(alpha))
    rect = rendered.get_rect(center=(WIDTH // 2, y))
    screen.blit(rendered, rect)

def draw_logo(alpha):
    screen.fill((0, 0, 0))
    draw_text('ShibaInu', HEIGHT // 2, alpha)

def draw_title():
    screen.fill((0, 0, 128))
    draw_text('ShibaInu Game', HEIGHT // 2 - 50)
    draw_text('S: Start Game', HEIGHT // 2)
    draw_text('P: Settings', HEIGHT // 2 + 50)
    draw_text('Q: Quit', HEIGHT // 2 + 100)

GROUND_Y = HEIGHT - 100
PLAYER_SPEED = 5
JUMP_SPEED = -12
GRAVITY = 0.6

player_rect = pygame.Rect(50, GROUND_Y - 50, 50, 50)
player_vel_y = 0
on_ground = True
goal_rect = pygame.Rect(WIDTH - 100, GROUND_Y - 50, 50, 50)
stage_cleared = False


def init_stage():
    global player_rect, player_vel_y, on_ground, stage_cleared
    player_rect.x = 50
    player_rect.y = GROUND_Y - 50
    player_vel_y = 0
    on_ground = True
    stage_cleared = False


def update_stage(keys):
    global player_vel_y, on_ground, stage_cleared, state

    if keys[pygame.K_LEFT]:
        player_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_rect.x += PLAYER_SPEED

    if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and on_ground:
        player_vel_y = JUMP_SPEED
        on_ground = False

    player_vel_y += GRAVITY
    player_rect.y += player_vel_y

    if player_rect.bottom >= GROUND_Y:
        player_rect.bottom = GROUND_Y
        player_vel_y = 0
        on_ground = True

    player_rect.x = max(0, min(WIDTH - player_rect.width, player_rect.x))

    if player_rect.colliderect(goal_rect):
        stage_cleared = True


def draw_stage():
    screen.fill((0, 128, 0))
    pygame.draw.rect(screen, (100, 50, 0), (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
    pygame.draw.rect(screen, (0, 0, 255), player_rect)
    pygame.draw.rect(screen, (255, 215, 0), goal_rect)
    draw_text('Stage 1-1', 40)
    if stage_cleared:
        draw_text('Stage Clear! ESC: Title', 100)

def draw_settings():
    screen.fill((128, 0, 0))
    draw_text('Settings', HEIGHT // 2 - 50)
    draw_text('ESC: Back to Title', HEIGHT // 2)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if state == TITLE:
                if event.key == pygame.K_s:
                    init_stage()
                    state = STAGE1_1
                elif event.key == pygame.K_p:
                    state = SETTINGS
                elif event.key == pygame.K_q:
                    running = False
            elif state == STAGE1_1:
                if event.key == pygame.K_ESCAPE:
                    state = TITLE
            elif state == SETTINGS:
                if event.key == pygame.K_ESCAPE:
                    state = TITLE

    if state == LOGO:
        draw_logo(logo_alpha)
        if logo_timer > LOGO_DURATION / 2:
            logo_alpha = min(255, logo_alpha + LOGO_FADE_STEP)
        else:
            logo_alpha = max(0, logo_alpha - LOGO_FADE_STEP)
        logo_timer -= 1
        if logo_timer <= 0:
            state = TITLE
    elif state == TITLE:
        draw_title()
    elif state == STAGE1_1:
        keys = pygame.key.get_pressed()
        update_stage(keys)
        draw_stage()
    elif state == SETTINGS:
        draw_settings()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
