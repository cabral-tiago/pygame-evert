import pygame
from pygame.surface import Surface
from classes.button import Button
from classes.buttongroup import ButtonGroup
from classes.level import Level
from classes.enums import GameState, LevelType


class Scene:
    def __init__(self) -> None:
        self.__button_groups: list[ButtonGroup] = []
        
        self.__levels: dict[int, Level] = {}
        self.__levels[0] = Level("assets/levels/0")
        self.__current_level = 0

    def add_button_group(self, button_group: ButtonGroup) -> None:
        self.__button_groups.append(button_group)

    def load_level(self, level_nr: int, level: Level) -> None:
        self.__levels[level_nr] = level

    def change_level(self, level_nr: int) -> None:
        if level_nr in self.__levels.keys():
            self.__current_level = level_nr
    
    def get_next_dialogue(self) -> None:
        if self.get_current_level().get_type() == LevelType.DIALOGUE:
            self.get_current_level().goto_next_line()

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

        for button_group in self.__button_groups:
            if button_group.is_visible():
                result = button_group.click(mouse_pos)
                if result != GameState.NULL:
                    return result
        
        return GameState.NULL

    def handle_key_down(self, key: int) -> None:
        pass

    def handle_key_up(self, key: int) -> None:
        pass

    def reset(self) -> None:
        for level in self.__levels.values():
            level.reset()
        
        self.change_level(0)

    def update(self, dt: float) -> GameState:
        flag_hovering = False
        for button_group in self.__button_groups:
            if button_group.is_visible() and button_group.is_hovering():
                flag_hovering = True
                break
        
        if flag_hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        return self.get_current_level().update()

    def draw(self, screen: Surface) -> None:
        for button_group in self.__button_groups:
            if button_group.is_visible():
                screen.blit(button_group.get_surface(), (0, 0))
