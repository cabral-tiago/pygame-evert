from enum import Enum


class GameState(Enum):
    NULL = -1
    MAIN_MENU = 0
    GAME_FRESH = 1
    GAME_PLAYING = 2
    GAME_PAUSED = 3
    GAME_ENDING = 4


class SceneID(Enum):
    MENU = 0
    WORLD = 1


class PlayerDirection(Enum):
    DOWN = 0
    UP = 1
    RIGHT = 2
    LEFT = 3
    STAY = 4