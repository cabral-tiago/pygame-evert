from enum import Enum
from classes.scene import Scene
from scenes.menu import Menu


class GameState(Enum):
    MAIN_MENU = 0
    GAME_FRESH = 1
    GAME_PLAYING = 2
    GAME_PAUSED = 3
    GAME_ENDING = 4


class Game:
    def __init__(self) -> None:
        self.__status = GameState.MAIN_MENU

        self.__scenes: list[Scene] = []

        menu = Menu()
        menu.visible = True
        self.__scenes.append(menu)

    def draw(self, screen) -> None:
        for scene in self.__scenes:
            scene.draw(screen)
