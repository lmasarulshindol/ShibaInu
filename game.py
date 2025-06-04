import pygame
import sys

# Screen dimensions
WIDTH, HEIGHT = 800, 600
FPS = 60

# States
LOGO = 'logo'
TITLE = 'title'
STAGE1_1 = 'stage1-1'
SETTINGS = 'settings'

# Settings variables
volume = 5  # 0 to 10
difficulty_options = ['Easy', 'Normal', 'Hard']
difficulty_index = 1
settings_items = ['Volume', 'Difficulty', 'Back']
selected_setting = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ShibaInu Game')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

state = LOGO
logo_timer = 120  # frames to display the logo


def draw_text(text, y):
    rendered = font.render(text, True, (255, 255, 255))
    rect = rendered.get_rect(center=(WIDTH // 2, y))
    screen.blit(rendered, rect)

def draw_logo():
    screen.fill((0, 0, 0))
    draw_text('ShibaInu', HEIGHT // 2)

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
    draw_text('Settings', 120)
    options = [
        f'Volume: {volume}',
        f'Difficulty: {difficulty_options[difficulty_index]}',
        'Back'
    ]
    for i, text in enumerate(options):
        color = (255, 255, 0) if i == selected_setting else (255, 255, 255)
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(center=(WIDTH // 2, 250 + i * 60))
        screen.blit(rendered, rect)


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
            elif state == STAGE1_1:
                if event.key == pygame.K_ESCAPE:
                    state = TITLE
            elif state == SETTINGS:
                if event.key == pygame.K_ESCAPE:
                    state = TITLE
                elif event.key == pygame.K_UP:
                    selected_setting = (selected_setting - 1) % len(settings_items)
                elif event.key == pygame.K_DOWN:
                    selected_setting = (selected_setting + 1) % len(settings_items)
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    if selected_setting == 0:
                        if event.key == pygame.K_LEFT and volume > 0:
                            volume -= 1
                        elif event.key == pygame.K_RIGHT and volume < 10:
                            volume += 1
                    elif selected_setting == 1:
                        if event.key == pygame.K_LEFT:
                            difficulty_index = (difficulty_index - 1) % len(difficulty_options)
                        else:
                            difficulty_index = (difficulty_index + 1) % len(difficulty_options)
                elif event.key == pygame.K_RETURN:
                    if selected_setting == 2:
                        state = TITLE

    if state == LOGO:
        draw_logo()
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
