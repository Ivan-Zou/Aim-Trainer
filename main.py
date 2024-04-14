import math, random, time # interal libraries
import pygame # external libraries

# python files
import constants
from target import Target

pygame.init()
pygame.display.set_caption("Aim Trainer")

DIFFICULTY_WINDOW = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
GAME_WINDOW = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))


TARGET_EVENT = pygame.USEREVENT
TARGET_SIZE = 30

LABEL_FONT = pygame.font.SysFont("roboto", 50)

GAME_DURATION = 30

def draw(win, targets):
    win.fill(constants.BACKGROUND_COLOR)

    for target in targets:
        target.draw(win)


def format_time(secs):
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}"


def draw_info_bar(window, elapsed_time, targets_clicked, num_clicks):
    pygame.draw.rect(window, "dark blue", (0, 0, constants.WINDOW_WIDTH, constants.INFO_BAR_HEIGHT))
    
    percentage_hit = round(0.0 if num_clicks == 0 else (targets_clicked / num_clicks) * 100, 1)
    percentage_hit_label = LABEL_FONT.render(f"{percentage_hit}%", 1, "grey")

    time_label = LABEL_FONT.render(f"< {format_time(elapsed_time)} >", 1, "grey")

    hits_label = LABEL_FONT.render(f"Hits: {targets_clicked}", 1, "grey")

    window.blit(hits_label, (20, 5))
    window.blit(time_label, (get_middle(time_label), 5))
    window.blit(percentage_hit_label, (constants.WINDOW_WIDTH - 125, 5))

def end_screen(window, elapsed_time, targets_clicked, num_clicks):
    window.fill(constants.BACKGROUND_COLOR)
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "white")

    speed = round(targets_clicked / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} targets/sec", 1, "white")

    hits_label = LABEL_FONT.render(f"Hits: {targets_clicked}", 1, "white")

    accuracy = round((targets_clicked / num_clicks) * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    window.blit(time_label, (get_middle(time_label), 100))
    window.blit(speed_label, (get_middle(speed_label), 200))
    window.blit(hits_label, (get_middle(hits_label), 300))
    window.blit(accuracy_label, (get_middle(accuracy_label), 400))

    pygame.display.update()

    end_screen_running = True
    while end_screen_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

def get_middle(surface):
    return constants.WINDOW_WIDTH / 2 - surface.get_width() / 2


def main():
    clock = pygame.time.Clock()

    targets_clicked = 0
    num_clicks = 0
    start_time = time.time()
    targets = []

    pygame.time.set_timer(TARGET_EVENT, 1)
    game_running = True
    while game_running:
        clock.tick(60)
        clicked = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                break

            if event.type == TARGET_EVENT and len(targets) < constants.NUM_TARGETS:
                x = random.randint(constants.TARGET_PADDING, constants.WINDOW_WIDTH - constants.TARGET_PADDING)
                y = random.randint(constants.TARGET_PADDING + constants.INFO_BAR_HEIGHT, constants.WINDOW_HEIGHT - constants.TARGET_PADDING)
                target = Target(x, y, TARGET_SIZE)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                num_clicks += 1

        for target in targets:
            if clicked and target.hit(*mouse_pos):
                targets.remove(target)
                targets_clicked += 1

        if elapsed_time > GAME_DURATION:
            end_screen(GAME_WINDOW, elapsed_time, targets_clicked, num_clicks)

        draw(GAME_WINDOW, targets)
        draw_info_bar(GAME_WINDOW, GAME_DURATION - elapsed_time, targets_clicked, num_clicks)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()