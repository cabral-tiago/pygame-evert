class DialogueLine:
    def __init__(self, character_id: str, line: str, emotion: str = "") -> None:
        self.__character_id: str = character_id
        self.__line: str = line
        self.__emotion: str = emotion

    def get_character_id(self) -> str:
        return self.__character_id

    def get_emotion(self) -> str:
        return self.__emotion
    
    def get_line(self) -> str:
        return self.__line
