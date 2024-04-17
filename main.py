import random, time # interal libraries
import pygame # external libraries

# python files
import constants
from target import Target
from button import Button

# initialize pygame
pygame.init()
# set the program name
pygame.display.set_caption("Aim Trainer")

# create the game window
GAME_WINDOW = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
# create the user event
TARGET_EVENT = pygame.USEREVENT
# create a font to be used by labels
LABEL_FONT = pygame.font.SysFont("roboto", 50)

GAME_DURATION = 30

def start_screen(window: object):
    # set the background
    window.fill(constants.BACKGROUND_COLOR)

    # create and draw the title of this game, Aim Trainers
    title_label = pygame.font.SysFont("roboto", 100).render("AIM TRAINER", 1, "orange")
    window.blit(title_label, (get_middle(title_label), 50))

    # load the difficuly button images
    easy_img = pygame.image.load("easy.png").convert_alpha()
    medium_img = pygame.image.load("medium.png").convert_alpha()
    hard_img = pygame.image.load("hard.png").convert_alpha()

    # create the difficulty button objects
    easy_button = Button(constants.WINDOW_WIDTH // 2, 200, easy_img, 0.5)
    medium_button = Button(constants.WINDOW_WIDTH // 2, 300, medium_img, 0.5)
    hard_button = Button(constants.WINDOW_WIDTH // 2, 400, hard_img, 0.5)

    # draw the buttons onto the screen
    easy_button.draw(window)
    medium_button.draw(window)
    hard_button.draw(window)

    # update the screen
    pygame.display.update()

    # show the start screen until the player quits or have chosen a difficuly
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.is_clicked():
                    return constants.EASY_TARGET_SIZE, "Easy"
                elif medium_button.is_clicked():
                    return constants.MEDIUM_TARGET_SIZE, "Medium"
                elif hard_button.is_clicked():
                    return constants.HARD_TARGET_SIZE, "Hard"
        
def format_time(secs: float) -> str:
    # Format time in seconds into a presentable min:sec string
    if secs < 0:
        return 0
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}"

def draw(window: object, targets: list):
    # Draw the background and targets to the screen
    window.fill(constants.BACKGROUND_COLOR)
    for target in targets:
        target.draw(window)

def draw_info_bar(window: object, elapsed_time: float, targets_clicked: int, num_clicks: int):
    # create the bar
    pygame.draw.rect(window, "black", (0, 0, constants.WINDOW_WIDTH, constants.INFO_BAR_HEIGHT))
    
    # create labels to be displayed on the bar
    percentage_hit = round(0.0 if num_clicks == 0 else (targets_clicked / num_clicks) * 100, 1)
    percentage_hit_label = LABEL_FONT.render(f"{percentage_hit}%", 1, "grey")
    time_label = LABEL_FONT.render(f"< {format_time(elapsed_time)} >", 1, "grey")
    hits_label = LABEL_FONT.render(f"Hits: {targets_clicked}", 1, "grey")

    # draw the labels onto the bar
    window.blit(hits_label, (20, 5))
    window.blit(time_label, (get_middle(time_label), 5))
    window.blit(percentage_hit_label, (constants.WINDOW_WIDTH - 125, 5))

def end_screen(window: object, elapsed_time: float, targets_clicked: int, num_clicks: int, difficulty: str):
    # set the background
    window.fill(constants.BACKGROUND_COLOR)

    # create the statistic labels to be shown on the screen
    difficulty_label = LABEL_FONT.render(f"Difficulty: {difficulty}", 1, "white")
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits: {targets_clicked}", 1, "white")
    accuracy = round(0.0 if num_clicks == 0 else (targets_clicked / num_clicks) * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")
    speed = round(targets_clicked / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} targets/sec", 1, "white")

    # create and draw the play again button
    play_again_img = pygame.image.load("play_again.png").convert_alpha()
    play_again_button = Button(constants.WINDOW_WIDTH // 2, 500, play_again_img, 0.75)
    play_again_button.draw(window)

    # Draw the labels on to the screen 
    window.blit(difficulty_label, (get_middle(difficulty_label), 150))
    window.blit(time_label, (get_middle(time_label), 200))
    window.blit(hits_label, (get_middle(hits_label), 250))
    window.blit(accuracy_label, (get_middle(accuracy_label), 300))
    window.blit(speed_label, (get_middle(speed_label), 350))

    # update the screen
    pygame.display.update()

    # continue showing the end screen until the player either quits or choose to play again
    end_screen_running = True
    while end_screen_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.is_clicked():
                    main()

def get_middle(object: object) -> float:
    # get the middle of the window based on the object's width
    return constants.WINDOW_WIDTH / 2 - object.get_width() / 2

def main():
    # initialize values
    clock = pygame.time.Clock()
    num_clicks = 0
    targets_clicked = 0
    target_size = -1
    targets = []
    difficulty = None

    pygame.time.set_timer(TARGET_EVENT, 1)
    game_running = True
    while game_running:
        # show the start screen if the player hasn't chosen a difficulty to set the target set
        if target_size == -1:
            target_size, difficulty = start_screen(GAME_WINDOW)
            # start the start time when the player chose a difficulty
            start_time = time.time()
        clock.tick(60)
        clicked = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            # stop the game if the player quits
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
            # show the end screen
            end_screen(GAME_WINDOW, elapsed_time, targets_clicked, num_clicks, difficulty)

        # Draw and update targets and info bar
        draw(GAME_WINDOW, targets)
        draw_info_bar(GAME_WINDOW, GAME_DURATION - elapsed_time, targets_clicked, num_clicks)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()