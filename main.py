import random, time # interal libraries
import pygame # external libraries

# python files
import constants
from target import Target
from button import Button

pygame.init()
pygame.display.set_caption("Aim Trainer")

GAME_WINDOW = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
TARGET_EVENT = pygame.USEREVENT
LABEL_FONT = pygame.font.SysFont("roboto", 50)

GAME_DURATION = 30

def start_screen(window):
    window.fill(constants.BACKGROUND_COLOR)

    title_label = pygame.font.SysFont("roboto", 100).render("AIM TRAINER", 1, "orange")

    window.blit(title_label, (get_middle(title_label), 50))
    easy_img = pygame.image.load("easy.png").convert_alpha()
    medium_img = pygame.image.load("medium.png").convert_alpha()
    hard_img = pygame.image.load("hard.png").convert_alpha()

    easy_button = Button(constants.WINDOW_WIDTH // 2, 200, easy_img, 0.5)
    medium_button = Button(constants.WINDOW_WIDTH // 2, 300, medium_img, 0.5)
    hard_button = Button(constants.WINDOW_WIDTH // 2, 400, hard_img, 0.5)

    easy_button.draw(window)
    medium_button.draw(window)
    hard_button.draw(window)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.is_clicked():
                    return constants.EASY_TARGET_SIZE
                elif medium_button.is_clicked():
                    return constants.MEDIUM_TARGET_SIZE
                elif hard_button.is_clicked():
                    return constants.HARD_TARGET_SIZE
        
def format_time(secs):
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}"

def draw(window, targets):
    window.fill(constants.BACKGROUND_COLOR)
    for target in targets:
        target.draw(window)

def draw_info_bar(window, elapsed_time, targets_clicked, num_clicks):
    pygame.draw.rect(window, "black", (0, 0, constants.WINDOW_WIDTH, constants.INFO_BAR_HEIGHT))
    
    percentage_hit = round(0.0 if num_clicks == 0 else (targets_clicked / num_clicks) * 100, 1)
    percentage_hit_label = LABEL_FONT.render(f"{percentage_hit}%", 1, "grey")

    time_label = LABEL_FONT.render(f"< {format_time(elapsed_time)} >", 1, "grey")

    hits_label = LABEL_FONT.render(f"Hits: {targets_clicked}", 1, "grey")

    window.blit(hits_label, (20, 5))
    window.blit(time_label, (get_middle(time_label), 5))
    window.blit(percentage_hit_label, (constants.WINDOW_WIDTH - 125, 5))

def end_screen(window, elapsed_time, targets_clicked, num_clicks):
    window.fill(constants.BACKGROUND_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")

    hits_label = LABEL_FONT.render(f"Hits: {targets_clicked}", 1, "white")

    accuracy = round(0.0 if num_clicks == 0 else (targets_clicked / num_clicks) * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    speed = round(targets_clicked / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} targets/sec", 1, "white")

    play_again_img = pygame.image.load("play_again.png").convert_alpha()
    play_again_button = Button(constants.WINDOW_WIDTH // 2, 500, play_again_img, 0.75)
    play_again_button.draw(window)

    window.blit(time_label, (get_middle(time_label), 200))
    window.blit(hits_label, (get_middle(hits_label), 250))
    window.blit(accuracy_label, (get_middle(accuracy_label), 300))
    window.blit(speed_label, (get_middle(speed_label), 350))

    pygame.display.update()

    end_screen_running = True
    while end_screen_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.is_clicked():
                    main()

def get_middle(object):
    return constants.WINDOW_WIDTH / 2 - object.get_width() / 2

def main():
    clock = pygame.time.Clock()
    num_clicks = 0
    targets_clicked = 0
    target_size = -1
    targets = []

    pygame.time.set_timer(TARGET_EVENT, 1)
    game_running = True
    while game_running:
        if target_size == -1:
            target_size = start_screen(GAME_WINDOW)
            start_time = time.time()
        clock.tick(60)
        clicked = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                break
            
            # Generate a target when there are less than NUM_TARGET targets in the game window
            if event.type == TARGET_EVENT and len(targets) < constants.NUM_TARGETS:
                x = random.randint(constants.TARGET_PADDING, constants.WINDOW_WIDTH - constants.TARGET_PADDING)
                y = random.randint(constants.TARGET_PADDING + constants.INFO_BAR_HEIGHT, constants.WINDOW_HEIGHT - constants.TARGET_PADDING)
                target = Target(x, y, target_size)
                targets.append(target)

            # Track clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                num_clicks += 1

        # Remove targets when they are clicked
        for target in targets:
            if clicked and target.clicked(*mouse_pos):
                targets.remove(target)
                targets_clicked += 1

        # End the game when it exceeds the game duration
        if elapsed_time > GAME_DURATION:
            end_screen(GAME_WINDOW, elapsed_time, targets_clicked, num_clicks)

        # Draw and update targets and info bar
        draw(GAME_WINDOW, targets)
        draw_info_bar(GAME_WINDOW, GAME_DURATION - elapsed_time, targets_clicked, num_clicks)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()