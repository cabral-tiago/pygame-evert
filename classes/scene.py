import pygame
from pygame.surface import Surface
from classes.button import Button
from classes.gameobject import GameObject
from classes.level import Level
from classes.states import GameState


class Scene:
    def __init__(self) -> None:
        self.objects: list[GameObject] = []
        self.__buttons: list[Button] = []
        
        self.__levels: dict[int, Level] = {}
        self.__levels[0] = Level("assets/levels/0")
        self.__current_level = 0

    def add_button(self, button: Button) -> None:
        self.__buttons.append(button)

    def load_level(self, level_nr: int, level: Level) -> None:
        self.__levels[level_nr] = level

    def change_level(self, level_nr: int) -> None:
        if level_nr in self.__levels.keys():
            self.__current_level = level_nr

    def get_current_level(self) -> Level:
        return self.__levels[self.__current_level]

    def handle_mouse_click(self) -> GameState:
        mouse_pos = pygame.mouse.get_pos()

        for button in self.__buttons:
            if button.get_rect().collidepoint(mouse_pos):
                return button.get_target_state()
        
        return GameState.NULL

    def handle_key_down(self, key: int) -> None:
        pass

    def handle_key_up(self, key: int) -> None:
        pass

    def update(self, dt: float) -> None:
        self.update_mouse()
    
    def update_mouse(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        flag_hovered = False

        for button in self.__buttons:
            if button.get_rect().collidepoint(mouse_pos):
                button.hover()
                flag_hovered = True
            else:
                button.normal()
        
        if flag_hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self, screen: Surface) -> None:
        for object in self.objects:
            screen.blit(object.get_surface(), object.get_position())
        for button in self.__buttons:
            screen.blit(button.get_surface(), button.get_position())
