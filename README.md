# Minesweeper Game

This is a Python implementation of the classic Minesweeper game, built using the Textual framework to create a dynamic and interactive terminal-based user interface. The game runs in the browser, leveraging Heroku for deployment and xterm.js for rendering the terminal environment. This project aims to bring the retro gaming experience into a modern web-based context while maintaining the simplicity and challenge of the original Minesweeper.


#### [Visit Minesweeper Game](https://minesweeper-game-4ed657dc9292.herokuapp.com/)

![monitor1](https://github.com/user-attachments/assets/482a16e7-8071-438c-a8d3-689bf7e68a9e)

## Table of Contents

- [User Experience](#user-experience)
- [Features](#features)
- [Design](#design)
- [Installation](#installation)
- [Testing](#testing)
- [Bugs](#bugs)
- [Deployment](#deployment)
- [Credits](#credits)
- [Personal Contribution and Experience](#personal-contribution-and-experience)
- [Acknowledgments](#acknowledgments)


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

    ![dark_color](https://github.com/user-attachments/assets/2f73c5a3-0464-4be3-b403-e3ebf6eda6e7)

    ![light_color](https://github.com/user-attachments/assets/be765ac8-78ab-438a-8c48-30ced1c68efa)


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

![completed](https://github.com/user-attachments/assets/e32ff3df-455a-42f3-8bc8-5822b73c5356)


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


## Installation

While this Minesweeper game is primarily deployed on the web via Heroku and does not require installation for online play, you can set up a local version on Linux and macOS for a better visual experience. Windows support is currently unverified.

### Linux and macOS

**Clone the Repository**
```Bash
git clone https://github.com/tibssy/minesweeper-game.git
cd minesweeper-game/
```

**Create and Activate a Virtual Environment**
```Bash
python3 -m venv venv
source venv/bin/activate
```

**Install Dependencies**
```Bash
pip install -r requirements.txt
```

**Run the Game**
```Bash
python run.py
```

### Creating a Standalone Executable

To create a standalone executable for Linux and macOS, you can use PyInstaller with the provided spec file.

**Install PyInstaller**
```Bash
pip install pyinstaller
```

**Use the Spec File**
```Bash
pyinstaller run.spec
```

**Deactivate the Virtual Environment**
```Bash
deactivate
```

**Locate the Bundled Binary and run**
```Bash
cd dist
chmod +x run
./run
```

If the executable is running successfully, you can rename it to whatever you prefer.

### Notes

- Dependencies: Ensure you have Python 3.7 or higher installed.
- Windows Users: Installation steps for Windows are not currently provided. You may need to adapt the Linux/macOS instructions for your environment or consider using Windows Subsystem for Linux (WSL) if you encounter issues.


## Testing

### PEP8 Code Validation

The PEP8 style guide was used to check the code for any formatting errors or issues. The code was tested using the [PEP8CI tool](https://pep8ci.herokuapp.com/#) tool to ensure it follows Python's best practices.

- **PEP8 Validation Result:**

    - **run.py:**

    ![run](https://github.com/user-attachments/assets/41e046db-774a-4aef-afcb-92918736dc6f)

    - **game_components.py:**

    ![game_components](https://github.com/user-attachments/assets/3f20edf4-00aa-44ed-9957-47c792ca410b)

    - **configurations.py:**

    ![configurations](https://github.com/user-attachments/assets/1ad23ab1-e579-4223-8c9c-17f210b76ea0)


- **PyLint Validation Result:**

    - **run.py:**

    ![run_pylint](https://github.com/user-attachments/assets/10cd5975-e828-458a-971c-71b14445f797)

    - **game_components.py:**

    ![game_components_pylint](https://github.com/user-attachments/assets/5181996b-af81-41c4-b810-c4ec39667e6b)

    - **configurations.py:**

    ![configurations_pylint](https://github.com/user-attachments/assets/60fba7ad-1c91-428d-959f-74edf4544f33)

### HTML Validation

The HTML code, including modifications made to the layout.html file, was tested using the [W3C Markup Validation Service](https://validator.w3.org/) to ensure it is error-free and follows best practices.

- **HTML Validation Result:**

    - **layout.html:**

    ![layout_html](https://github.com/user-attachments/assets/106a1b84-0c73-4f16-a2be-b929fa8d5bed)


### Functionality Test

| **ID** | **Test Area** | **Test Action** | **Expected Outcome** | **Test Outcome** |
| ------ | ------------- | --------------- | -------------------- | ---------------- |
| 01 | Main Screen | User presses up, down, "w", or "s" keys to navigate between options | The selection moves up or down between the available options (Player input, theme, color, difficulty, play) | PASS |
| 02 | Main Screen | User selects the Player input field, types special characters, and presses enter | Placeholder text changes to "only use letters, spaces, hyphens" | PASS |
| 03 | Main Screen | User types less than 3 letters in the Player input field and presses enter | Placeholder text changes to "use at least 3 letters" | PASS |
| 04 | Main Screen | User types between 3 and 10 characters (no special characters) in the Player input field and presses enter | Cursor jumps to the next option (theme selection) | PASS |
| 05 | Main Screen | User presses left, right, "a", or "d" keys while on the theme option | The theme switches between dark and light modes | PASS |
| 06 | Main Screen | User presses left, right, "a", or "d" keys while on the color option | Switches between 7 predefined color themes | PASS |
| 07 | Main Screen | User presses left, right, "a", or "d" keys while on the difficulty option | Switches between Easy, Medium, and Hard difficulty levels | PASS |
| 08 | Main Screen | User selects the Play button and presses enter | The game starts with the selected settings (theme, color, difficulty) if the player name presented | PASS |
| 09 | Game Screen | The player presses enter on the game board or places a flag | The timer does not start until the player reveals a tile on the game board | PASS |
| 10 | Game Screen | User presses the space bar or the "f" key on the game board | A flag is placed or removed from the selected cell, and the remaining flag counter at the top left corner is updated accordingly. The flag count remains within the range of the total number of mines (i.e., it cannot go below zero or above the number of mines) | PASS |
| 11 | Game Screen | User presses enter on a cell where a flag is already placed and there is no mine behind it | The flag is automatically removed, the remaining flag counter at the top left corner is increased, and the cell is uncovered | PASS |
| 12 | Game Screen | User presses enter on a cell with no mine and no neighboring mines (a zero cell) | The game automatically uncovers all adjacent empty cells and continues to uncover until it reaches cells with numbers or boundaries, including the cells around them | PASS |
| 13 | Game Screen | User presses enter on a cell with a number (indicating neighboring mines) | The cell with the number is uncovered, and the number of neighboring mines is displayed on the cell | PASS |
| 14 | Game Screen | User presses Enter on a cell containing a mine | All cells on the game board are uncovered, and the game over modal is displayed, indicating the end of the game | PASS |
| 15 | Game Screen | User places the last flag | The game automatically starts the validation process. If all flags are in the correct locations, the game over modal is triggered, and the entire game board is uncovered | PASS |
| 16 | Game Screen | User presses "esc" or "q" during gameplay | The game is reset, and the user is returned to the Main Screen | PASS |
| 17 | Game Over Screen (Modal) | Game ends with all mines correctly flagged | The modal displays a congratulatory message to the user, indicating that all mines were found successfully | PASS |
| 18 | Game Over Screen (Modal) | Game ends with a mine triggering | The modal displays an "0ops! You hit a mine and the game is over. Better luck next time!" message indicating that the player triggered a mine | PASS |
| 19 | Game Over Screen (Modal) | User navigates between "Exit" and "Show" buttons using left/right or "a"/"d" keys | The selection moves between the "Exit" and "Show" buttons, allowing the user to choose one | PASS |
| 20 | Game Over Screen (Modal) | User selects "Show" and presses enter or "Esc" | The game board is revealed with all numbers and mines uncovered | PASS |
| 21 | Game Over Screen (Modal) | User selects "Exit" and presses enter | The user is redirected to the main screen with the player name field pre-filled with the user's name, allowing them to start a new game without re-entering their name | PASS |


### Operating Systems, Browsers, and Terminals

The application was tested thoroughly on the following operating system, terminals, and browsers. No issues were found:

- **Operating Systems and Kernel**

    - **ArchLinux:** Tested on kernel version 6.10.9-zen1-2-zen

- **Terminals**

    - **gnome-console:** Version 46.0
    - **xfce4-terminal:** Version 1.1.3
    - **foot:** Version 1.18.1
    - **alacritty:** Version 0.13.2

- **Browsers**

    - **Firefox:** Version 130.0
    - **Brave:** Version 1:1.69.168-1


## Bugs

- **Issue:** Unable to update the color themes using Textual's built-in update method.
- **Solution:** To work around this issue, the dark mode was toggled twice using the following code:

    ```
    self.app.dark = not self.app.dark
    self.app.dark = not self.app.dark
    ```

    This approach successfully refreshed the color themes.


## Deployment

For deployment, this project leverages Heroku's platform, which makes it simple to host and run terminal-based Python applications in the cloud. Here’s a guide for manually deploying your project to Heroku using a GitHub repository:

### Deployment Steps:

- **1. Create a Heroku Account**
    - Visit [Heroku](https://dashboard.heroku.com/) and sign up for an account.

- **2. Create a New App**
    - Go to the Heroku dashboard and click **new**.
    - On the dropdown click **Create new app**.
    - Provide a unique app name and select your region then click **Create app**.

- **3. Add Buildpacks**
    - In the **Settings** tab, click **Add buildpack**.
    - Select **Python** and **Node.js** (if needed), ensuring that Python is listed first.

- **4. Connect to GitHub**
    - In the **Deploy** tab, choose **GitHub** as the deployment method.
    - Search for your repository and connect it to Heroku.

- **5. Manual or Automatic Deploy**
    - Enable **Automatic Deploys** for Heroku to update the app with every push to GitHub, or use the **Manual Deploy** option to deploy the main branch manually.

This deployment process ensures your application runs smoothly in a web-based environment hosted on Heroku.


## Credits

- **Image Generation**
    - [Playground AI](https://playground.com) Used for background image and favicon.
- **Image Editing and Conversion**
    - [GIMP - GNU Image Manipulation Program](https://www.gimp.org/) Open-source tool for editing images. used for readme images.
- **Version Control**
    - [GitHub](https://github.com) Used for version control and repository management.
- **Integrated Development Environment (IDE)**
    - Visual Studio Code on Gitpod: [Visual Studio Code](https://code.visualstudio.com/), [GitPod](https://www.gitpod.io/) Online IDE used for coding and development.
- **Textual**
    - [Textual](https://textual.textualize.io/) is a Python framework for creating terminal-based user interfaces with rich features.
- **NumPy**
    - [NumPy](https://numpy.org/) is a Python library for numerical computing, enabling fast operations on large arrays and matrices
- **SciPy**
    - [SciPy](https://scipy.org/) is a Python library that builds on NumPy, providing additional tools for scientific computing, including optimization, integration, interpolation, and linear algebra functions.


## Personal Contribution and Experience

This project was developed entirely by me, without relying on external sources, tutorials, or walkthroughs. I didn’t research how to make a Minesweeper game; instead, I used my own logic to solve the problems. I enjoy figuring things out on my own because it keeps the project challenging and fun. All the design and code decisions reflect my own experience and skills, with no outside help.

However, I utilized the documentation for Textual, NumPy, and SciPy to guide my implementation and understand their functionalities better. Additionally, I reviewed the source code of the Textual framework to address specific issues and gain deeper insights into its features. Despite these resources, the overall design and problem-solving approach were entirely my own.


## Acknowledgments

Thank you to my mentor, Brian Macharia, for his continuous support and valuable feedback. His tips and resources have been instrumental in enhancing my coding and testing skills.