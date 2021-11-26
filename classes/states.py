from enum import Enum


class GameState(Enum):
    MAIN_MENU = 0
    GAME_FRESH = 1
    GAME_PLAYING = 2
    GAME_PAUSED = 3
    GAME_ENDING = 4

class PlayerDirection(Enum):
    DOWN = 0
    UP = 1
    RIGHT = 2
    LEFT = 3
    STAY = 4