from pygame.surface import Surface
from pygame.rect import Rect
from classes.dialogueline import DialogueLine
from classes.dialoguecharacter import DialogueCharacter
from classes.enums import GameState
import configs
import pygame
from utils import draw_text


class Dialogue:
    def __init__(self) -> None:
        self.__characters: dict[str, DialogueCharacter] = {}
        self.__lines: list[DialogueLine] = []
        self.__current_line_index: int = -1
        self.__completed: bool = False

        # Dialogue UI
        self.__ui_surface = Surface((configs.SCREEN_W, configs.CHARACTER_SIZE[1]/3), pygame.SRCALPHA)
        self.__ui_surface.fill((0, 0, 0, 210))
        self.__ui_position = (0, configs.SCREEN_H - self.__ui_surface.get_height())

        self.__text_rect = Rect((40, 80), (configs.SCREEN_W - 80, self.__ui_surface.get_height() - 80))

        self.__font_name = pygame.font.Font("assets/fonts/CarterOne-Regular.ttf", 42)
        self.__font_text = pygame.font.Font("assets/fonts/Roboto-Medium.ttf", 38)

        self.__next_input = pygame.image.load("assets/images/nextdialogue.png").convert_alpha()
        self.__next_input = pygame.transform.scale(self.__next_input,
                                                  (self.__next_input.get_width() * 2, self.__next_input.get_height() * 2))

        # Narrator
        self.add_character("", DialogueCharacter("", ""))

    def add_character(self, character_id: str, character: DialogueCharacter) -> None:
        self.__characters[character_id] = character

    def add_line(self, line: DialogueLine) -> None:
        self.__lines.append(line)

        if len(self.__lines) == 1:
            self.goto_next_line()

    def get_current_line(self) -> DialogueLine:
        return self.__lines[self.__current_line_index]

    def get_current_character_id(self) -> str:
        return self.get_current_line().get_character_id()

    def get_current_character(self) -> DialogueCharacter:
        return self.__characters[self.get_current_character_id()]

    def goto_next_line(self) -> None:
        if self.__current_line_index + 1 < len(self.__lines):
            self.__current_line_index += 1

            for id, character in self.__characters.items():
                if self.get_current_character_id() == id:
                    character.set_active(self.get_current_line().get_emotion())
                else:
                    character.set_inactive()
        else:
            self.__completed = True

    def reset(self) -> None:
        self.__current_line_index = -1
        self.__completed = False

        self.goto_next_line()

    def update(self) -> GameState:
        if self.__completed or len(self.__lines) == 0:
            return GameState.GAME_LEVEL_END
        else:
            return GameState.GAME_OK

    def draw(self, screen: Surface) -> None:
        for id, character in self.__characters.items():
            if id == "":
                continue

            screen.blit(character.get_image(), character.get_position())

        # UI
        ui_surface = self.__ui_surface.copy()

        # Name
        ui_surface.blit(self.__font_name.render(
            self.get_current_character().get_name(),
            True,
            self.get_current_character().get_colour()),
            (40, 10))

        # Text
        draw_text(ui_surface,self.get_current_line().get_line(), "white", self.__text_rect, self.__font_text)

        # Input hint
        ui_surface.blit(self.__next_input, (ui_surface.get_width() - self.__next_input.get_width() - 4,
                                             ui_surface.get_height() - self.__next_input.get_height() - 2))

        # Draw UI
        screen.blit(ui_surface, self.__ui_position)
