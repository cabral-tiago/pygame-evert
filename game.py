from classes.states import GameState
from classes.scene import Scene
from scenes.menu import Menu


class Game:
    def __init__(self) -> None:
        self.__state = GameState.MAIN_MENU

        self.__scenes: list[Scene] = []

        menu = Menu()
        self.__scenes.append(menu)

    def draw(self, screen) -> None:
        for scene in self.__scenes:
            scene.draw(screen)
