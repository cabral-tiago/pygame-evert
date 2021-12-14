from typing import Tuple
from pygame.rect import Rect
from classes.collectable import Collectable
from classes.enemy import Enemy
from classes.enemies.monster import Monster
from classes.enemies.boss import Boss
from classes.projectile import Projectile
from classes.quest import Quest
from classes.enums import EndCondition, GameState, QuestType
from pygame.surface import Surface
import pygame
import configs
import random


class QuestTracker:

    def __init__(self) -> None:
        # Quests
        self.__quests: list[Quest] = []

        # Map Surface
        self.__map_surface: Surface = Surface((100, 100), pygame.SRCALPHA)

        # Projectiles
        self.__projectiles: list[Projectile] = []

        # Objective UI
        self.__objective_surface: Surface = Surface((configs.SCREEN_W, configs.BAR_HEIGHT))
        self.__objective_surface.fill("black")

        objective_title_font = pygame.font.Font("assets/fonts/CarterOne-Regular.ttf", 24)
        self.__objective_title = objective_title_font.render("Objetivos atuais:", True, "white")
        self.__objective_surface.blit(self.__objective_title,
                                    (20, configs.BAR_HEIGHT // 2 - self.__objective_title.get_height() // 2))

        self.__objective_font = pygame.font.Font("assets/fonts/CarterOne-Regular.ttf", 20)

        # Level End Condition
        self.__end_condition: EndCondition = EndCondition.NULL
        self.__end_objective: str = ""
        self.__end_position: Rect = Rect(-1, -1, 0, 0)
        self.__player_at_end: bool = False
        self.__level_completed: bool = False

    def add_quest(self, quest_info: dict) -> None:
        match quest_info["type"]:
            case "collect":
                type = QuestType.COLLECT
            case "kill_boss":
                type = QuestType.KILL_BOSS
            case "kill_monsters":
                type = QuestType.KILL_MONSTERS
            case _:
                type = QuestType.NULL

        collectables: list[Collectable] = []
        if "collectables" in quest_info:
            for collectable in quest_info["collectables"]:
                image = pygame.image.load(collectable["image_path"]).convert_alpha()
                scale = collectable["image_scale"]
                if scale != 1:
                    size = image.get_width() * scale, image.get_height() * scale
                    image = pygame.transform.scale(image, size)
                position = collectable["position"]
                
                collectables.append(Collectable(image, position))
        
        monsters: list[Enemy] = []
        if "monsters" in quest_info:
            left, top, width, height = quest_info["monsters"]["spawn_area"]
            for _ in range(quest_info["monsters"]["amount"]):
                rects = [m.get_rect() for m in monsters]
                while True:
                    pos_x = random.randint(left, left+width)
                    pos_y = random.randint(top, top+height)
                    new_monster = Monster((pos_x, pos_y))

                    if new_monster.get_rect().collidelist(rects) == -1:
                        break
                monsters.append(new_monster)
        if type == QuestType.KILL_BOSS:
            monsters.append(Boss(quest_info["boss_position"]))

        self.__quests.append(Quest(type, quest_info["objective"], collectables, monsters))

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
    
    def get_active_enemies(self) -> list[Enemy]:
        return [e for q in self.__quests for e in q.get_active_enemies()]
    
    def get_active_projectiles(self) -> list[Projectile]:
        return self.__projectiles

    def get_end_condition(self) -> EndCondition:
        return self.__end_condition

    def get_current_objectives(self) -> list[str]:
        objectives = [q.get_objective() for q in self.__quests if not q.is_completed()]

        if len(objectives) == 0:
            objectives.append(self.__end_objective)

        return objectives

    def get_map_surface(self) -> Surface:
        surface = self.__map_surface.copy()
        for collectable in self.get_active_collectables():
            surface.blit(collectable.get_image(), collectable.get_rect())
        return surface
    
    def get_objective_surface(self) -> Surface:
        surface = self.__objective_surface.copy()

        start_x = self.__objective_title.get_width() + 40
        current_x = start_x
        for objective in self.get_current_objectives():
            text = self.__objective_font.render("• " + objective, True, "white")
            surface.blit(text, (current_x + 10, configs.BAR_HEIGHT // 2 - text.get_height() // 2))
            current_x += text.get_width() + 20
        
        return surface

    def reset(self) -> None:
        for quest in self.__quests:
            quest.reset()
        
        self.__level_completed = False
