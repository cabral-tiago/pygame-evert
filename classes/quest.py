from classes.enums import QuestType
from classes.collectable import Collectable


class Quest:
    def __init__(self, type: QuestType, objective: str, collectables: list[Collectable]) -> None:
        self.__type: QuestType = type
        self.__objective: str = objective
        self.__collectables: list[Collectable] = collectables
        self.__completed = False

    def get_type(self) -> QuestType:
        return self.__type

    def get_objective(self) -> str:
        return self.__objective

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

    def reset(self) -> None:
        for collectable in self.__collectables:
            collectable.reset()
        
        self.__completed = False
