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

def draw_stage():
    screen.fill((0, 128, 0))
    draw_text('Stage 1-1', HEIGHT // 2 - 50)
    draw_text('ESC: Back to Title', HEIGHT // 2)

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
                    state = STAGE1_1
                elif event.key == pygame.K_p:
                    state = SETTINGS
                elif event.key == pygame.K_q:
                    running = False
            elif state in (STAGE1_1, SETTINGS):
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
        draw_stage()
    elif state == SETTINGS:
        draw_settings()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
