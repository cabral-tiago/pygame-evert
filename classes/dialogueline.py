from classes.dialoguecharacter import DialogueCharacter
from pygame.surface import Surface


class DialogueLine:
    def __init__(self, character: DialogueCharacter, line: str, expression: str = "") -> None:
        self.__character: DialogueCharacter = character
        self.__line: str = line
        self.__expression: str = expression

    def get_character(self) -> DialogueCharacter:
        return self.__character

    def get_character_surface(self) -> Surface:
        return self.__character.get_image(self.__expression)
    
    def get_line(self) -> str:
        return self.__line
