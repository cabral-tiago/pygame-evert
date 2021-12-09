from typing import Tuple
from pygame.rect import Rect
from classes.collectable import Collectable
from classes.quest import Quest
from classes.enums import EndCondition, GameState, QuestType
from pygame.surface import Surface
import pygame
import configs


class QuestTracker:
    def __init__(self) -> None:
        # Quests
        self.__quests: list[Quest] = []

        # Map Surface
        self.__map_surface: Surface = Surface((100, 100), pygame.SRCALPHA)

        # Objective UI
        self.__objective_surface: Surface = Surface(configs.SCREEN_SIZE, pygame.SRCALPHA)
        objetive_title_font = pygame.font.Font("assets/fonts/CarterOne-Regular.ttf", 28)
        objective_title = objetive_title_font.render("Objetivo atual", True, "white")
        self.__objective_font = pygame.font.Font("assets/fonts/Roboto-Medium.ttf", 22)
        self.__objective_surface.blit(objective_title, (20, 10))

        # Level End Condition
        self.__end_condition: EndCondition = EndCondition.NULL
        self.__end_objective: str = ""
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
        
        self.__quests.append(Quest(type, quest_info["objective"], collectables))

    def set_end_condition(self, condition: EndCondition, objective: str = "", position: Rect = Rect(-1, -1, 0, 0)):
        self.__end_condition = condition
        self.__end_objective = objective
        self.__end_position = position

    def set_surface_size(self, size: Tuple[int, int]) -> None:
        self.__map_surface = Surface(size, pygame.SRCALPHA)

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

    def get_current_objective(self) -> str:
        for quest in self.__quests:
            if not quest.is_completed():
                return quest.get_objective()

        return self.__end_objective

    def get_map_surface(self) -> Surface:
        surface = self.__map_surface.copy()
        for collectable in self.get_active_collectables():
            surface.blit(collectable.get_image(), collectable.get_rect())
        return surface
    
    def get_objective_surface(self) -> Surface:
        surface = self.__objective_surface.copy()

        objective_text = self.__objective_font.render(self.get_current_objective(), True, "white")
        surface.blit(objective_text, (20, 46))

        return surface

    def reset(self) -> None:
        for quest in self.__quests:
            quest.reset()
        
        self.__level_completed = False
