import pygame
from pygame.surface import Surface
from classes.button import Button
from classes.level import Level
from classes.enums import GameState, LevelType


class Scene:
    def __init__(self) -> None:
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
    
    def get_next_dialogue(self) -> GameState:
        if self.get_current_level().get_type() == LevelType.DIALOGUE:
            return self.get_current_level().get_next_dialogue()
        else:
            return GameState.NULL

    def goto_next_level(self) -> GameState:
        if self.__current_level + 1 in self.__levels.keys():
            self.change_level(self.__current_level+1)
            return GameState.GAME_OK
        else:
            return GameState.GAME_END

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

    def update(self, dt: float) -> GameState:
        self.update_mouse()

        if self.get_current_level().is_level_complete():
            return GameState.GAME_LEVEL_END
        return GameState.GAME_OK
    
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
        for button in self.__buttons:
            screen.blit(button.get_surface(), button.get_position())
