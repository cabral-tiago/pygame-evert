from enum import Enum


class GameState(Enum):
    MAIN_MENU = 0
    GAME_FRESH = 1
    GAME_PLAYING = 2
    GAME_PAUSED = 3
    GAME_ENDING = 4


class Game:
    def __init__(self) -> None:
        self.__status = GameState.MAIN_MENU

    def draw(self, screen) -> None:
        pass
