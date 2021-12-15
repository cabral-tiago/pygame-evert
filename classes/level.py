import os
import json
from typing import Tuple
from pygame.rect import Rect
from pygame.surface import Surface
from classes.dialogue import Dialogue
from classes.dialoguecharacter import DialogueCharacter
from classes.dialogueline import DialogueLine
from classes.collectable import Collectable
from classes.enemy import Enemy
from classes.enemies.monster import Monster
from classes.projectile import Projectile
from classes.questtracker import QuestTracker
from classes.tileset import Tileset
from classes.maplayer import MapLayer
from classes.enums import EndCondition, GameState, LevelType
import configs
import pygame


class Level:
    def __init__(self, path) -> None:
        # Level
        self.__type: LevelType = LevelType.BLANK
        self.__background: Surface = Surface(configs.SCREEN_SIZE, pygame.SRCALPHA)
        
        # Map
        self.__layers: list[MapLayer] = []
        self.__obstacles: list[Rect] = []
        self.__quest_tracker: QuestTracker = QuestTracker()
        
        # Player
        self.__player_appear: bool = False
        self.__player_spawn: Tuple[int, int] = (0, 0)

        # Projectiles
        self.__projectile_list: list[Projectile] = []
        
        # Camera
        self.__camera_offset: Tuple[int, int] = (0, 0)

        # Dialogue
        self.__dialogue = Dialogue()

        # Loading
        with open(path+"/level_info.json", "r", encoding="utf-8") as file:
            level_info = json.load(file)

            self.__type = LevelType(level_info["type"])
            match self.__type:
                case LevelType.MAP:
                    self.__load_map(level_info, path)
                
                case LevelType.DIALOGUE:
                    self.__load_dialogue(level_info, path)
    
    def __load_map(self, level_info, path) -> None:
        # Tileset
        tile_scale: int = level_info["tile_scale"]
        tile_size: Tuple[int, int] = level_info["tile_size"]
        world_scale: Tuple[int, int] = (tile_scale*tile_size[0], tile_scale*tile_size[1])
        tileset = Tileset(level_info["tileset"], tile_size, tile_scale)

        # Player visibility and spawn location
        self.__player_appear = level_info["player_appear"]
        spawn_x, spawn_y = level_info["player_spawn"]
        spawn_x *= tile_size[0] * tile_scale
        spawn_y *= tile_size[1] * tile_scale
        self.__player_spawn = (spawn_x, spawn_y)

        # Map Layers
        layers_path = path + "/layers"
        layer_files = [f.name for f in os.scandir(layers_path) if f.name.endswith(".csv")]
        ordered_layers = sorted([(int(i[:-7]), i) for i in layer_files])

        for n, file in ordered_layers:
            layer_collide = True if file[:-4].split("_")[1] == "ob" else False
            alpha = True
            if n == 0:
                alpha = False
            layer = MapLayer(layers_path + "/" + file, layer_collide, tileset, alpha)    
            self.__obstacles.extend(layer.get_obstacle_rects())
            self.__layers.append(layer)

        # Passing map size to Quest Tracker
        world_size_x = self.__layers[0].get_surface().get_width()
        world_size_y = self.__layers[0].get_surface().get_height()
        self.__quest_tracker.set_surface_size((world_size_x, world_size_y))

        # Quests
        for quest in level_info["quests"]:
            if "collectables" in quest:
                for collectable in quest["collectables"]:
                    position = collectable["position"]
                    position = (position[0] * world_scale[0], position[1] * world_scale[1])
                    collectable["position"] = position
            if "monsters" in quest:
                left, top, width, height = quest["monsters"]["spawn_area"]
                spawn_area = [left * world_scale[0], top * world_scale[1],
                              width * world_scale[0], height * world_scale[1]]
                quest["monsters"]["spawn_area"] = spawn_area
            if "boss_position" in quest:
                position = quest["boss_position"]
                position = (position[0] * world_scale[0], position[1] * world_scale[1])
                quest["boss_position"] = position
            self.__quest_tracker.add_quest(quest)

        # End Condition
        end_condition = level_info["end_condition"]
        if end_condition["condition"] == "immediate_end":
            self.__quest_tracker.set_end_condition(EndCondition.IMMEDIATE_END)
        elif end_condition["condition"] == "return_when_done":
            end_position: Tuple[int, int] = end_condition["position"]
            end_left = end_position[0] * tile_scale * tile_size[0]
            end_top = end_position[1] * tile_scale * tile_size[1]
            end_width = tile_size[0] * tile_scale
            end_height = tile_size[1] * tile_scale
            end_rect = Rect(end_left, end_top, end_width, end_height)
            self.__quest_tracker.set_end_condition(EndCondition.RETURN_WHEN_DONE, end_condition["objective"], end_rect)


    def __load_dialogue(self, level_info, path) -> None:
        if level_info["bg_style"] == "colour":
            self.__background.fill(level_info["bg_colour"])
        elif level_info["bg_style"] == "image":
            image: Surface = pygame.image.load(level_info["bg_image"]).convert()
            if image.get_width() != configs.SCREEN_W:
                scale = configs.SCREEN_W / image.get_width()
                scaled_height = int(image.get_height() * scale)
                if level_info["bg_smooth_scale"]:
                    image = pygame.transform.smoothscale(image, (configs.SCREEN_W, scaled_height))
                else:
                    image = pygame.transform.scale(image, (configs.SCREEN_W, scaled_height))

            self.__background.blit(image,(0, 0))

        with open(path+"/dialogue.json", "r", encoding="utf-8") as file:
            dialogue_data = json.load(file)

            for character in dialogue_data["characters"]:
                character_id = character[0]
                character_path = character[1]
                character_start_emotion = character[2]

                self.__dialogue.add_character(character_id, DialogueCharacter(character_path, character_start_emotion))

            for line in dialogue_data["dialogue"]:
                if len(line) == 1:
                    self.__dialogue.add_line(DialogueLine("", line[0]))
                elif len(line) == 2:
                    self.__dialogue.add_line(DialogueLine(line[0], line[1]))
                elif len(line) == 3:
                    self.__dialogue.add_line(DialogueLine(line[0], line[1], line[2]))

    ### Level
    def get_type(self) -> LevelType:
        return self.__type

    def get_width(self) -> int:
        if self.__type == LevelType.MAP:
            return self.__layers[0].get_surface().get_width()
        else:
            return self.__background.get_width()

    def get_height(self) -> int:
        if self.__type == LevelType.MAP:
            return self.__layers[0].get_surface().get_height()
        else:
            return self.__background.get_height()
    
    def reset(self) -> None:
        if self.__type == LevelType.MAP:
            self.__quest_tracker.reset()
        elif self.__type == LevelType.DIALOGUE:
            self.__dialogue.reset()

    def update(self) -> GameState:
        if self.__type == LevelType.MAP:
            return self.__quest_tracker.update()
        elif self.__type == LevelType.DIALOGUE:
            return self.__dialogue.update()
        else:
            return GameState.GAME_OK
    
    ### Map Level
    def get_obstacles(self) -> list[Rect]:
        return self.__obstacles

    def get_end_condition(self) -> EndCondition:
        return self.__quest_tracker.get_end_condition()

    def get_active_collectables(self) -> list[Collectable]:
        return self.__quest_tracker.get_active_collectables()

    def get_end_position(self) -> Rect:
        return self.__quest_tracker.get_end_position()

    def set_player_at_end(self) -> None:
        self.__quest_tracker.set_player_at_end()

    def is_player_visible(self) -> bool:
        return self.__player_appear
    
    def get_player_spawn(self) -> Tuple[int, int]:
        return self.__player_spawn
    
    def center_on_player(self, player_rect: Rect) -> None:
        self.__camera_offset = (configs.SCREEN_W // 2 - player_rect.x - player_rect.width // 2,
                                configs.SCREEN_H // 2 - player_rect.y - player_rect.height // 2)
    
    def set_projectiles(self, projectiles: list[Projectile]) -> None:
        self.__projectile_list = projectiles

    def get_enemies(self) -> list[Enemy]:
        return self.__quest_tracker.get_active_enemies()

    ### Dialogue
    def goto_next_line(self) -> None:
        self.__dialogue.goto_next_line()

    ### Drawing
    def draw(self, screen: Surface) -> None:
        screen.blit(self.__background, (0, 0))

        if self.__type == LevelType.MAP:
            for layer in self.__layers:
                screen.blit(layer.get_surface(), self.__camera_offset)

            # Draw collectibles
            screen.blit(self.__quest_tracker.get_map_surface(), self.__camera_offset)

            # Draw enemies
            enemy_surface = Surface((self.get_width(), self.get_height()), pygame.SRCALPHA)
            for enemy in self.get_enemies():
                enemy_surface.blit(enemy.get_surface_with_hp(), enemy.get_rect())
            screen.blit(enemy_surface, self.__camera_offset)

            # Draw projectiles
            projectile_surface = Surface((self.get_width(), self.get_height()), pygame.SRCALPHA)
            for projectile in self.__projectile_list:
                projectile_surface.blit(projectile.get_surface(), projectile.get_rect())
            screen.blit(projectile_surface, self.__camera_offset)

            # Draw objective UI
            screen.blit(self.__quest_tracker.get_objective_surface(), (0, 0))
        elif self.__type == LevelType.DIALOGUE:
            self.__dialogue.draw(screen)
        else:
            pass  # Blank level
