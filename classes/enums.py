from enum import Enum


class GameState(Enum):
    NULL = -1
    MAIN_MENU = 0
    GAME_FRESH = 1
    GAME_PLAYING = 2
    GAME_PAUSED = 3
    GAME_OK = 4
    GAME_END = 5


class SceneID(Enum):
    MENU = 0
    WORLD = 1


class LevelType(Enum):
    BLANK = 0
    DIALOGUE = 1
    MAP = 2


class PlayerDirection(Enum):
    DOWN = 0
    UP = 1
    RIGHT = 2
    LEFT = 3
    STAY = 4


class ScreenAlignment(Enum):
    NULL = -1
    LEFT = 0
    CENTER = 1
    RIGHT = 2
