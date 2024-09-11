# Minesweeper Game

This is a Python implementation of the classic Minesweeper game, built using the Textual framework to create a dynamic and interactive terminal-based user interface. The game runs in the browser, leveraging Heroku for deployment and xterm.js for rendering the terminal environment. This project aims to bring the retro gaming experience into a modern web-based context while maintaining the simplicity and challenge of the original Minesweeper.


#### [Visit Minesweeper Game](https://minesweeper-game-4ed657dc9292.herokuapp.com/)

![monitor1](https://github.com/user-attachments/assets/482a16e7-8071-438c-a8d3-689bf7e68a9e)

## Table of Contents

-   [User Experience](#user-experience)
-   [Features](#features)
-   [Design](#design)
-   [Installation](#installation)
-   [Testing](#testing)
-   [Bugs](#bugs)
-   [Deployment](#deployment)
-   [Credits](#credits)


## User Experience

### Ideal User Demographic

**Minesweeper is ideal for:**

-   **New Users:**

    -   People who enjoy puzzle and logic games.
    -   Casual gamers looking for a quick and challenging experience.
    -   Those who appreciate terminal-based retro interfaces.
    -   Classic Minesweeper enthusiasts wanting a fresh web-based version.

-   **Current Users:**
    -   Returning players who enjoy Minesweeper and are familiar with the game's mechanics.
    -   Users seeking updates on new themes, features, or improved performance.
    -   Players who prefer customizing their game setup for a personalized experience.

### Goals for First-Time Visitors

As a first-time visitor to Minesweeper, I want to:

-   Quickly understand how to play the game.
-   Easily navigate through the interface using intuitive terminal commands.
-   Start a new game session with minimal setup.
-   Access information or help regarding gameplay and controls.

### Goals for Returning Visitors

As a returning visitor to Minesweeper, I want to:

-   Check for new features, such as additional difficulty modes or themes.
-   Quickly start a new game with my preferred settings.
-   Track my progress or scores from previous games.
-   Customize the game interface with available themes and settings.

## Features

### Main Screen

- **Player Name Input**

    The player name input field ensures that users enter a valid and personalized name for their game session. It includes validation rules to make the input experience intuitive and error-free.

    - **Input Validation:**

        - Minimum Length Requirement: The player name must be at least 3 characters long. If a shorter name is provided, the input field resets, and the user is prompted with a placeholder message: "Use at least 3 letters."

            ![3letter](https://github.com/user-attachments/assets/b49f6f79-0c60-4a76-bed6-c951440a75c0)

        - Character Restrictions: Only alphabetic characters, spaces, and hyphens are allowed. If the user enters invalid characters, such as numbers or symbols, the input resets, and a new placeholder message appears: "Only use letters, spaces, hyphens."

            ![special_chr](https://github.com/user-attachments/assets/df08a167-7139-4fbb-a1c5-4e64bdbc3be4)

    - **Interactive Feedback:**

        - The input field provides real-time feedback. If the input is invalid, the player is immediately notified, and the input field is cleared, allowing them to quickly correct their entry.

        - The placeholder text dynamically adjusts based on the error encountered, guiding users toward valid input without interrupting the flow.

    - **Automatic Capitalization:**

        - Once a valid player name is provided, it is automatically capitalized, ensuring consistency in name formatting.

    This feature enhances user experience by enforcing simple yet effective validation, while offering clear guidance for players entering their name.


- **Theme Selector:**

    - Provides options to choose between different visual themes (e.g., Dark Mode for a sleek, modern look).

    ![dark_light](https://github.com/user-attachments/assets/50fe66d7-af1f-4643-92c3-b09f92fa8a17)

    - Color Selector: Allows players to choose from 7 predefined color schemes, offering customization options to suit personal preferences and enhance the visual experience.

    ![7_colors](https://github.com/user-attachments/assets/d2bf2377-1603-44ae-8ace-10a05587bc6b)


- **Difficulty Levels:**

    Players can choose between three difficulty settings—Easy, Medium, and Hard—each offering a unique challenge based on the number of mines and the grid size.

    - **Easy:** 10 mines on an 11x8 grid, perfect for new or casual players.
    - **Medium:** 30 mines on a 19x14 grid, offering a balanced challenge for regular players.
    - **Hard:** 60 mines on a 25x16 grid, designed for experienced players seeking a more intense challenge.

- **Play Button:** 

    - Once settings are adjusted, the player can start the game by selecting "Play."


Navigation is intuitive, using familiar keys for interaction:

- **Up/Down Arrows** or **(w/s):** Navigate between options.
- **Left/Right Arrows** or **(a/d):** Adjust the selected option (e.g., changing theme or difficulty).
- **Enter:** Confirm settings and begin the game.


### Game Screen

The game screen provides a clean and minimal interface, focusing on the core gameplay. It features the following elements.

- **Mine Counter (Top Left):** Displays the number of mines remaining on the field. This helps players keep track of how many mines they still need to flag or avoid.

- **Player Information (Top Center):** The player's name is displayed prominently in the center, personalizing the session.

- **Timer (Top Right):** Tracks the time elapsed since the game started, adding an additional challenge for players aiming for speed.

- **Game Grid (Center):** This is where the game is played. The grid consists of squares, and players move through it using keyboard controls. Hidden mines are distributed across the grid based on the selected difficulty. The grid will update as players reveal safe spaces or mark potential mines with flags.

- **Controls (Bottom):**

    - **Movement:** Players use arrow keys or w, a, s, d to move the cursor across the grid.
    - **Hit (Reveal):** Press Enter to reveal the current cell. If it contains a mine, the game ends.
    - **Place Flag:** Press Space or f to mark a cell with a flag, indicating a suspected mine.
    - **Quit:** Press esc or q to exit the game.

![hard](https://github.com/user-attachments/assets/845e52f6-2180-47fb-a440-635fd9ca0a4e)


### Game Screen: Cell Uncovering

When a player presses Enter on a cell with no mine and no neighboring mines (a zero cell), the game automatically uncovers all adjacent empty cells along with the boundary of numbered cells around them. This mechanism helps the player reveal larger portions of the game board in one move, improving gameplay flow and minimizing manual uncovering.

- **Empty Cells:** Shown in a blank space (as in the top-left corner of the grid).
- **Numbered Cells:** Cells adjacent to mines display numbers, with each number indicating how many mines are present in the neighboring cells. The numbers are color-coded for better distinction (e.g., blue for 1, green for 2, and red for 3).
- **Frame of Numbers:** The boundary around the uncovered area consists of numbered cells, which help guide the player in identifying where mines could be located next.

This feature allows for strategic gameplay by revealing safe areas quickly, reducing the need for cautious cell-by-cell clearing in open spaces.

![uncover_zeros_with_border](https://github.com/user-attachments/assets/db73ff20-6872-4fc5-83fb-ada4d0acdedb)


### Game Over Screen

The Game Over Screen serves as the final feedback interface in the Minesweeper game, displaying results to the player based on their performance—whether they successfully uncovered all non-mine cells or hit a mine.

- **Dynamic Messaging**: The message shown is dependent on the game outcome.

    - **Victory:** If the player successfully uncovers all the mines, a congratulatory message will appear, including the player's name and the time it took to complete the game.
    - **Defeat:** If the player hits a mine, a message informs them that the game is over, with a prompt to try again.

- **Performance Summary:** The Game Over screen provides the following details.

    - The player's name.
    - Total time taken to complete the game (in case of victory).

- **Encouraging User Experience:** The victory message emphasizes the player's success, while the failure message offers a positive note encouraging the player to try again, fostering a fun and motivational environment.

![modal_completed](https://github.com/user-attachments/assets/62c3609c-c676-4235-86b7-a265e36c0f89)


## Design

### Imagery

The design of the Minesweeper game focuses on a clean, retro-inspired terminal interface, maintaining simplicity and ease of navigation. There are no elaborate graphics or background images, ensuring that the gameplay itself remains the central focus without distractions.


### Color Scheme

The game's color scheme provides both Light and Dark themes, along with seven predefined hue options: Orange, Yellow, Green, Blue, Purple, Pink, and Red. These hues are applied to enhance the visual contrast between different game elements, making the interface customizable while remaining user-friendly.

The themes are designed for clarity, ensuring visibility of important game elements like the minefield, flags, and numbers, making the gameplay intuitive and accessible.


### Color Palette

- **Light Mode:**

    - Primary Background: Saturation 50%, Lightness 95%
    - Secondary Background: Saturation 75%, Lightness 85%
    - Primary Accent: Saturation 100%, Lightness 45%
    - Secondary Accent: Saturation 100%, Lightness 25%
    - Font Color: Saturation 15%, Lightness 15%

- **Dark Mode:**

    - Primary Background: Saturation 16%, Lightness 16%
    - Secondary Background: Saturation 15%, Lightness 25%
    - Primary Accent: Saturation 90%, Lightness 60%
    - Secondary Accent: Saturation 100%, Lightness 80%
    - Font Color: Saturation 95%, Lightness 95%

- **Hue Values:**
    The hue values in the game are predefined and listed as follows:

    - Orange: 33°
    - Yellow: 50°
    - Green: 110°
    - Blue: 200°
    - Purple: 266°
    - Pink: 320°
    - Red: 360°

    These predefined hues are designed to suit a variety of personal preferences and maintain visual consistency across different light and dark modes.

- **Accessibility:**

    The color choices aim to maximize readability for users across different lighting conditions, ensuring a comfortable visual experience during gameplay. Additionally, the terminal-based interface ensures the game runs efficiently without unnecessary visual noise, further enhancing accessibility.











## Personal Contribution and Experience

This project was developed entirely by me, without using any external sources, tutorials, or walkthroughs. I didn’t research how to make a Minesweeper game; instead, I used my own logic to solve the problems. I enjoy figuring things out on my own because it keeps the project challenging and fun. All the design and code decisions reflect my own experience and skills, with no outside help.

