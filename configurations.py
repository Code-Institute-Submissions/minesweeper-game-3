from enum import Enum


class Hue(Enum):
    """
    Enum representing various hues used in theming.

    Attributes:
        ORANGE (int): Hue value for the color orange.
        YELLOW (int): Hue value for the color yellow.
        GREEN (int): Hue value for the color green.
        BLUE (int): Hue value for the color blue.
        PURPLE (int): Hue value for the color purple.
        PINK (int): Hue value for the color pink.
        RED (int): Hue value for the color red.
    """

    ORANGE = 33
    YELLOW = 50
    GREEN = 110
    BLUE = 200
    PURPLE = 266
    PINK = 320
    RED = 360


class LightTheme(Enum):
    """
    Enum representing light theme color settings.

    Attributes:
        PRIMARY_BACKGROUND (tuple): Background color for primary areas.
        SECONDARY_BACKGROUND (tuple): Background color for secondary areas.
        PRIMARY_ACCENT (tuple): Accent color for primary elements.
        SECONDARY_ACCENT (tuple): Accent color for secondary elements.
        FONT_COLOR (tuple): Color for text.
    """

    PRIMARY_BACKGROUND = (0.5, 0.95)
    SECONDARY_BACKGROUND = (0.75, 0.85)
    PRIMARY_ACCENT = (1, 0.45)
    SECONDARY_ACCENT = (1, 0.25)
    FONT_COLOR = (0.15, 0.15)


class DarkTheme(Enum):
    """
    Enum representing dark theme color settings.

    Attributes:
        PRIMARY_BACKGROUND (tuple): Background color for primary areas.
        SECONDARY_BACKGROUND (tuple): Background color for secondary areas.
        PRIMARY_ACCENT (tuple): Accent color for primary elements.
        SECONDARY_ACCENT (tuple): Accent color for secondary elements.
        FONT_COLOR (tuple): Color for text.
    """

    PRIMARY_BACKGROUND = (0.16, 0.16)
    SECONDARY_BACKGROUND = (0.15, 0.25)
    PRIMARY_ACCENT = (0.9, 0.6)
    SECONDARY_ACCENT = (1, 0.8)
    FONT_COLOR = (0.95, 0.95)


class GameMode(Enum):
    """
    Enum representing different game modes and their settings.

    Attributes:
        EASY (dict): Settings for easy mode.
        MEDIUM (dict): Settings for medium mode.
        HARD (dict): Settings for hard mode.
    """

    EASY = {'mine': 10, 'grid_size': (11, 8)}
    MEDIUM = {'mine': 30, 'grid_size': (19, 14)}
    HARD = {'mine': 60, 'grid_size': (25, 16)}


class Icons(Enum):
    """
    Enum representing various icons used in the game.

    Attributes:
        MINE (str): Icon for a mine.
        BOMB (str): Icon for a bomb.
        SKULL (str): Icon for a skull.
        FLAG (str): Icon for a flag.
        LEFT (str): Icon for left arrow.
        RIGHT (str): Icon for right arrow.
        UP (str): Icon for up arrow.
        DOWN (str): Icon for down arrow.
    """

    MINE = '\u2747'
    BOMB = '\U0001F4A3'
    SKULL = '\u2620'
    FLAG = '\u2691'
    LEFT = '\u2B9C'
    RIGHT = '\u2B9E'
    UP = '\u2B9D'
    DOWN = '\u2B9F'
