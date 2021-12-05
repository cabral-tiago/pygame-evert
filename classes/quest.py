from classes.enums import QuestType
from classes.collectable import Collectable


class Quest:
    def __init__(self, type: QuestType, title: str, desc: str, collectables: list[Collectable]) -> None:
        self.__type: QuestType = type
        self.__title: str = title
        self.__desc: str = desc
        self.__collectables: list[Collectable] = collectables
        self.__completed = False

    def get_type(self) -> QuestType:
        return self.__type

    def get_title(self) -> str:
        return self.__title

    def get_description(self) -> str:
        return self.__desc

    def get_active_collectables(self) -> list[Collectable]:
        active_collectables: list[Collectable] = []
        for collectable in self.__collectables:
            if not collectable.is_collected():
                active_collectables.append(collectable)
        return active_collectables

    def update_quest(self) -> None:
        if self.__type == QuestType.COLLECT and len(self.get_active_collectables()) == 0:
            self.__completed = True

    def set_completed(self) -> None:
        self.__completed = True
    
    def is_completed(self) -> bool:
        return self.__completed
