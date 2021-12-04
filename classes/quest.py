from classes.enums import GameState, QuestType
from classes.object import Object


class Quest:
    def __init__(self, type: QuestType, title: str, desc: str, object = None) -> None:
        self.__type: QuestType = type
        self.__title: str = title
        self.__desc: str = desc
        
        self.__objects: list[Object] = []
        if type == QuestType.COLLECT:
            self.__objects.append(object)

        self.__completed = False

    def get_type(self) -> QuestType:
        return self.__type

    def get_title(self) -> str:
        return self.__title

    def get_description(self) -> str:
        return self.__desc

    def get_object(self) -> Object:
        return self.__objects[0]

    def update_quest(self) -> None:
        if self.__type == QuestType.COLLECT and self.__objects[0].is_collected():
            self.__completed = True

    def set_completed(self) -> None:
        self.__completed = True
    
    def is_completed(self) -> bool:
        return self.__completed
