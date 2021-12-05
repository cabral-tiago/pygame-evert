from typing import Tuple
from classes.collectable import Collectable
from classes.quest import Quest
from classes.enums import EndCondition, GameState, QuestType
from pygame.surface import Surface
import pygame


class QuestTracker:
    def __init__(self) -> None:
        self.__quests: list[Quest] = []
        self.__surface: Surface = Surface((100, 100), pygame.SRCALPHA)

        self.__player_position: Tuple[int, int] = (0, 0)

        self.__end_condition: EndCondition = EndCondition.NULL
        self.__end_condition_quest_title: str = ""
        self.__end_condition_quest_desc: str = ""
        self.__end_condition_home: Tuple[int, int] = (0, 0)
        self.__is_level_completed: bool = False

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

    def set_level_completion(self, end_condition: dict) -> None:
        type = EndCondition.NULL
        if end_condition["condition"] == "return_when_done":
            type = EndCondition.RETURN_WHEN_DONE
        elif end_condition["condition"] == "immediate_end":
            type = EndCondition.IMMEDIATE_END

        self.__end_condition = type

        self.__end_condition_quest_title = end_condition["quest_title"]
        self.__end_condition_quest_desc = end_condition["quest_description"]

        if type == EndCondition.RETURN_WHEN_DONE:
            pos_x, pos_y = end_condition["home_position"]
            pos_x *= end_condition["tile_size"][0]
            pos_y *= end_condition["tile_size"][1]
            if end_condition["world_scale"] != 1:
                pos_x *= end_condition["world_scale"]
                pos_y *= end_condition["world_scale"]
            self.__end_condition_home = (pos_x, pos_y)

    def set_surface_size(self, size: Tuple[int, int]) -> None:
        self.__surface = Surface(size, pygame.SRCALPHA)

    def update(self) -> None:
        quests_left = len(self.__quests)

        for quest in self.__quests:
            quest.update_quest()

            if quest.is_completed():
                quests_left -= 1
        
        if quests_left == 0:
            if self.__end_condition == EndCondition.IMMEDIATE_END or \
                    (self.__end_condition == EndCondition.RETURN_WHEN_DONE and \
                    self.__player_position == self.__end_condition_home):
                self.__is_level_completed = True

    def set_player_position(self, position: Tuple[int, int]) -> None:
        self.__player_position = position

    def get_active_collectables(self) -> list[Collectable]:
        active_collectables = []
        for quest in self.__quests:
            if not quest.is_completed() and quest.get_type() == QuestType.COLLECT:
                active_collectables.extend(quest.get_active_collectables())
        return active_collectables

    def get_status(self) -> GameState:
        if self.__is_level_completed:
            return GameState.GAME_LEVEL_END
        else:
            return GameState.GAME_OK

    def get_end_condition(self) -> EndCondition:
        return self.__end_condition

    def get_end_condition_title(self) -> str:
        return self.__end_condition_quest_title

    def get_end_condition_description(self) -> str:
        return self.__end_condition_quest_desc

    def get_surface(self) -> Surface:
        surface = self.__surface.copy()
        for collectable in self.get_active_collectables():
            surface.blit(collectable.get_image(), collectable.get_rect())
        return surface
