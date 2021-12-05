from typing import Tuple

from pygame.rect import Rect
from classes.collectable import Collectable
from classes.quest import Quest
from classes.enums import EndCondition, GameState, QuestType
from pygame.surface import Surface
import pygame


class QuestTracker:
    def __init__(self) -> None:
        self.__quests: list[Quest] = []
        self.__surface: Surface = Surface((100, 100), pygame.SRCALPHA)

        # Level End Condition
        self.__end_condition: EndCondition = EndCondition.NULL
        self.__end_quest_title: str = ""
        self.__end_quest_desc: str = ""
        self.__end_position: Rect = Rect(-1, -1, 0, 0)
        self.__player_at_end: bool = False
        self.__level_completed: bool = False

    def add_quest(self, quest_info: dict) -> None:
        type = QuestType.NULL
        if quest_info["type"] == "collect":
            type = QuestType.COLLECT
        elif quest_info["type"] == "kill_boss":
            type = QuestType.KILL_BOSS

        collectables: list[Collectable] = []
        for collectable in quest_info["collectables"]:
            image = pygame.image.load(collectable["image_path"])
            scale = collectable["image_scale"]
            if scale != 1:
                size = image.get_width() * scale, image.get_height() * scale
                image = pygame.transform.scale(image, size)
            position = collectable["position"]
            
            collectables.append(Collectable(image, position))
        
        self.__quests.append(Quest(type, quest_info["quest_title"], quest_info["quest_description"], collectables))

    def set_end_condition(self, condition: EndCondition,\
                          quest_title: str = "", quest_desc: str = "", position: Rect = Rect(-1, -1, 0, 0)):
        self.__end_condition = condition
        self.__end_quest_title = quest_title
        self.__end_quest_desc = quest_desc
        self.__end_position = position

    def set_surface_size(self, size: Tuple[int, int]) -> None:
        self.__surface = Surface(size, pygame.SRCALPHA)

    def update(self) -> GameState:
        quests_left = len(self.__quests)

        for quest in self.__quests:
            quest.update_quest()

            if quest.is_completed():
                quests_left -= 1
        
        if quests_left == 0:
            if self.__end_condition == EndCondition.IMMEDIATE_END or \
            (self.__end_condition == EndCondition.RETURN_WHEN_DONE and self.__player_at_end):
                self.__level_completed = True
        else:
            self.__player_at_end = False
        
        if self.__level_completed:
            return GameState.GAME_LEVEL_END
        else:
            return GameState.GAME_OK

    def get_end_position(self) -> Rect:
        return self.__end_position
    
    def set_player_at_end(self) -> None:
        self.__player_at_end = True

    def get_active_collectables(self) -> list[Collectable]:
        active_collectables = []
        for quest in self.__quests:
            if not quest.is_completed() and quest.get_type() == QuestType.COLLECT:
                active_collectables.extend(quest.get_active_collectables())
        return active_collectables

    def get_end_condition(self) -> EndCondition:
        return self.__end_condition

    def get_end_condition_title(self) -> str:
        return self.__end_quest_title

    def get_end_condition_description(self) -> str:
        return self.__end_quest_desc

    def get_surface(self) -> Surface:
        surface = self.__surface.copy()
        for collectable in self.get_active_collectables():
            surface.blit(collectable.get_image(), collectable.get_rect())
        return surface
