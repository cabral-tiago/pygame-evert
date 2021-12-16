import pygame
from pygame.mixer import Sound
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

        self.__click: Sound = Sound("assets/sounds/effects/click.wav")

    def add_button(self, button) -> None:
        self.__buttons.append(button)

    def load_level(self, level_nr: int, level: Level) -> None:
        self.__levels[level_nr] = level

    def play_click(self) -> None:
        self.__click.play()

    def change_level(self, level_nr: int) -> None:
        if level_nr in self.__levels.keys():
            self.__current_level = level_nr
            if self.get_current_level().get_music() != "":
                pygame.mixer.music.unload()
                pygame.mixer.music.load(self.get_current_level().get_music())
                pygame.mixer.music.play(-1)
    
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

        for button in self.__buttons:
            if button.is_visible() and button.get_rect().collidepoint(mouse_pos):
                self.play_click()
                return button.get_target_state()

        return GameState.NULL

    def handle_key_down(self, key: int) -> GameState:
        return GameState.GAME_OK

    def handle_key_up(self, key: int) -> GameState:
        return GameState.GAME_OK

    def reset(self) -> None:
        for level in self.__levels.values():
            level.reset()
        
        self.change_level(0)
    
    def reset_level(self) -> None:
        self.get_current_level().reset()

    def update(self, dt: float) -> GameState:
        flag_hovering = False
        for button in self.__buttons:
            if button.is_visible() and button.is_hovering():
                flag_hovering = True
                break
        
        if flag_hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        return self.get_current_level().update()

    def draw(self, screen: Surface) -> None:
        for button in self.__buttons:
            if button.is_visible():
                screen.blit(button.get_surface(), button.get_rect())
