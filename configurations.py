from enum import Enum


class Hue(Enum):
    ORANGE = 33
    YELLOW = 50
    GREEN = 100
    BLUE = 200
    PURPLE = 266
    PINK = 320
    RED = 360


class LightTheme(Enum):
    PRIMARY_BACKGROUND = (1, 0.95)
    SECONDARY_BACKGROUND = (0.75, 0.85)
    PRIMARY_ACCENT = (1, 0.5)
    SECONDARY_ACCENT = (1, 0.35)
    FONT_COLOR = (0.15, 0.15)


class DarkTheme(Enum):
    PRIMARY_BACKGROUND = (0.16, 0.16)
    SECONDARY_BACKGROUND = (0.15, 0.25)
    PRIMARY_ACCENT = (1, 0.6)
    SECONDARY_ACCENT = (1, 0.8)
    FONT_COLOR = (0.95, 0.95)


class GameMode(Enum):
    EASY = {'mine': 10, 'grid_size': (11, 8)}
    MEDIUM = {'mine': 30, 'grid_size': (19, 14)}
    HARD = {'mine': 60, 'grid_size': (25, 16)}


class Icons(Enum):
    MINE = '\u2747'
    STAR = '\u2738'
    SKULL = '\u2620'

