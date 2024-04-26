# Aim-Trainer

## Installation Instructions

1. Download code
2. pip install pygame
3. run main.py
4. enjoy the game
5. a computer mouse is recommended

## Code Structure

- 15.png - image of the 15 seconds button
- 30.png - image of the 30 seconds button
- 45.png - image of the 45 seconds button
- 60.png - image of the 60 seconds button
- button.py - contains the Button class
  - This class allow us to have functional buttons within the game, so the player can select different things, such as difficulty.
  - The key methods are is_clicked, which returns true if the button instance has been clicked and false otherwise, and draw, which draws the button given its xy-coordinate and image provided upon initialization
  - I decided to create this class because my game requires and utilizes multiple buttons
- constants.py - contains constants used in the game
  - This allows us to easily change constants used in the code, without actively searching through the code to change them
- easy.png - image of the easy difficult button
- hard.png - image of the hard difficult button
- main.py - contains the game logic and game executable
  - Here I created methods for code that I use multiple times like format_time and get_middle. This is to prevent repeated code.
  - I also created methods for thing I will draw to the window, such as the start screen, select duration screen, info bar, drawing targets, and the end screen. Though this code is only used once, I put them in a method so the main methods can be easier to read and focus on the game mechanics, such as generating random targets, detecting a target getting clicked, tracking stats, and such, rather than drawing objects to the screen.
- medium.png - image of the medium difficult button
- README.md
- target.py - contains the Target class
  - Thus class allow use to create functional targets in the game, which is the main focus of the game.
  - The key methods are clicked, which checks if the given xy-coordinate is within the area of the target instance, and draw, which draws the target instance onto the window
  - I decided to create this class because thee main focus of my game is to click target on the screen, so my game needs to be able to have multiple instances of a target on the screen at once
- test.py - contains test cases for this program
