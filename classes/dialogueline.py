from classes.dialoguecharacter import DialogueCharacter


class DialogueLine:
    def __init__(self, character: DialogueCharacter, line: str) -> None:
        self.__character: DialogueCharacter = character
        self.__line: str = line

    def get_character(self) -> DialogueCharacter:
        return self.__character
    
    def get_line(self) -> str:
        return self.__line
