from pygame.surface import Surface
from classes.dialogueline import DialogueLine
from classes.dialoguecharacter import DialogueCharacter
from classes.enums import GameState

class Dialogue:
    def __init__(self) -> None:
        self.__characters: dict[str, DialogueCharacter] = {}
        self.__lines: list[DialogueLine] = []
        self.__current_line_index: int = -1
        self.__completed: bool = False
    
    def add_character(self, character_id:str, character: DialogueCharacter) -> None:
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
                    character.set_active()
                else:
                    character.set_inactive()
        else:
            self.__completed = True

    def update(self) -> GameState:
        if self.__completed or len(self.__lines) == 0:
            return GameState.GAME_LEVEL_END
        else:
            return GameState.GAME_OK
    
    def draw(self, screen: Surface) -> None:
        for id, character in self.__characters.items():
            if id == "":
                continue

            if id == self.get_current_character_id():
                screen.blit(character.get_image(self.get_current_line().get_emotion()), character.get_position())
            else:
                screen.blit(character.get_image(), character.get_position())

