from typing import Tuple
from classes.states import GameState
from classes.scene import Scene
from scenes.menu import Menu
from scenes.world import World
import pygame


class Game:
    def __init__(self) -> None:
        self.__state = GameState.MAIN_MENU

        self.__scenes: dict[str, Scene] = {}
        
        self.__scenes["menu"] = Menu()
        self.__scenes["world"] = World()

        self.__current_scene = "menu"

        self.__mouse_down_event = False

    def update(self, dt) -> None:
        self.__scenes[self.__current_scene].update(dt)
        self.update_mouse()

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
    
    def update_mouse(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        flag_hovered = False

        match self.__state:
            case GameState.MAIN_MENU:
                for button in self.__scenes["menu"].buttons:
                    if button.get_rect().collidepoint(mouse_pos):
                        button.hovered = True
                        flag_hovered = True
                        if self.__mouse_down_event:
                            self.change_state(button.get_target_state())
                    else:
                        button.hovered = False
        
        self.__mouse_down_event = False

        if flag_hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    
    def handle_mouse_click(self) -> None:
        self.__mouse_down_event = True