from typing import Tuple
from classes.states import GameState
from classes.scene import Scene
from scenes.menu import Menu
from scenes.world import World


class Game:
    def __init__(self) -> None:
        self.__state = GameState.MAIN_MENU

        self.__scenes: dict[str, Scene] = {}
        
        self.__scenes["menu"] = Menu()
        self.__scenes["world"] = World()

        self.__current_scene = "menu"

    def draw(self, screen) -> None:
        self.__scenes[self.__current_scene].draw(screen)

    def change_state(self, new_state: GameState) -> None:
        self.__state = new_state

        match self.__state:
            case GameState.MAIN_MENU:
                self.__current_scene = "menu"
            case GameState.GAME_FRESH:
                self.__current_scene = "world"
            case GameState.GAME_PLAYING:
                self.__current_scene = "world"
    
    def handle_mouse_click(self, pos: Tuple[int, int]) -> None:
        match self.__state:
            case GameState.MAIN_MENU:
                for button in self.__scenes["menu"].buttons:
                    if button.get_rect().collidepoint(pos):
                        self.change_state(button.get_target_state())