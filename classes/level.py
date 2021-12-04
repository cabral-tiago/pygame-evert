import os
import json
from typing import Tuple
from pygame.rect import Rect
from pygame.surface import Surface
from classes.dialoguecharacter import DialogueCharacter
from classes.dialogueline import DialogueLine
from classes.object import Object
from classes.questtracker import QuestTracker
from classes.tileset import Tileset
from classes.levellayer import LevelLayer
from classes.enums import EndCondition, GameState, LevelType, QuestType
import configs
import pygame


class Level:
    def __init__(self, path) -> None:
        # Level
        self.__type: LevelType = LevelType.BLANK
        self.__background: Surface = Surface(configs.SCREEN_SIZE, pygame.SRCALPHA)
        
        ### Map
        self.__layers: list[LevelLayer] = []
        self.__obstacles: list[Rect] = []
        self.__quest_tracker: QuestTracker = QuestTracker()
        self.__level_complete = False
        
        # Player
        self.__player_appear: bool = False
        self.__player_spawn: Tuple[int, int] = (0, 0)
        
        # Camera
        self.__camera_offset: Tuple[int, int] = (0, 0)

        ### Dialogue
        self.__d_lines: list[DialogueLine] = []
        self.__d_characters: dict[str, DialogueCharacter] = {}
        self.__d_line_index: int = 0
        
        # Dialogue HUD
        self.__d_background = Surface((configs.SCREEN_W,configs.CHARACTER_SIZE[1]/3), pygame.SRCALPHA)
        self.__d_background.fill((0,0,0,210))
        self.__d_bg_position = (0, configs.SCREEN_H - self.__d_background.get_height())
        self.__d_text_font = pygame.font.Font("assets\\fonts\\Roboto-Medium.ttf", 38)
        self.__d_name_font = pygame.font.Font("assets\\fonts\\CarterOne-Regular.ttf", 42)


        with open(path+"/level_info.json", "r", encoding="utf-8") as file:
            level_info = json.load(file)

            self.__type = LevelType(level_info["type"])
            match self.__type:
                case LevelType.MAP:
                    self.__load_map(level_info, path)
                
                case LevelType.DIALOGUE:
                    self.__load_dialogue(level_info, path)
                    self.__d_line_index = -1
                    self.get_next_dialogue()
    
    def __load_map(self, level_info, path) -> None:
        self.__player_appear = level_info["player_appear"]
        spawn_x, spawn_y = level_info["player_spawn"]
        spawn_x *= level_info["tile_size"][0] * level_info["tile_scale"]
        spawn_y *= level_info["tile_size"][1] * level_info["tile_scale"]
        self.__player_spawn = (spawn_x, spawn_y)

        tileset = Tileset(level_info["tileset"], level_info["tile_size"], level_info["tile_scale"])

        layers_path = path + "/layers"
        layer_files = [f.name for f in os.scandir(layers_path) if f.name.endswith(".csv")]
        ordered_layers = sorted([(int(i[:-7]), i) for i in layer_files])

        for _, file in ordered_layers:
            layer_collide = True if file[:-4].split("_")[1] == "ob" else False
            layer = LevelLayer(layers_path + "/" + file, layer_collide, tileset)
            if layer_collide:
                self.__obstacles.extend(layer.get_obstacle_rects())
            self.__layers.append(layer)

        world_size_x = self.__layers[0].get_surface().get_width()
        world_size_y = self.__layers[0].get_surface().get_height()
        self.__quest_tracker.set_surface_size((world_size_x, world_size_y))
        
        for quest in level_info["quests"]:
            if quest["object"]:
                quest["world_scale"] = level_info["tile_scale"]
                quest["tile_size"] = level_info["tile_size"]
            self.__quest_tracker.add_quest(quest)

        end_condition = level_info["end_condition"]
        if end_condition["condition"] == "return_when_done":
            end_condition["home_position"] = level_info["player_spawn"]
            end_condition["world_scale"] = level_info["tile_scale"]
            end_condition["tile_size"] = level_info["tile_size"]
        self.__quest_tracker.set_level_completion(end_condition)

    def __load_dialogue(self, level_info, path) -> None:
        if level_info["bg_style"] == "colour":
            self.__background.fill(level_info["bg_colour"])
        elif level_info["bg_style"] == "image":
            image: Surface = pygame.image.load(level_info["bg_image"])
            if image.get_width() != configs.SCREEN_W:
                scale = configs.SCREEN_W / image.get_width()
                scaled_height = int(image.get_height() * scale)
                if level_info["bg_smooth_scale"]:
                    image = pygame.transform.smoothscale(image, (configs.SCREEN_W, scaled_height))
                else:
                    image = pygame.transform.scale(image, (configs.SCREEN_W, scaled_height))

            self.__background.blit(image,(0, 0))

        self.__d_characters[""] = DialogueCharacter("", "")  # Narrator
        with open(path+"/dialogue.json", "r", encoding="utf-8") as file:
            dialogue_data = json.load(file)

            for character in dialogue_data["characters"]:
                character_id = character[0]
                character_path = character[1]
                character_start_emotion = character[2]

                self.__d_characters[character_id] = DialogueCharacter(character_path, character_start_emotion)

            for line in dialogue_data["dialogue"]:
                if len(line) == 1:
                    self.__d_lines.append(DialogueLine("", line[0]))
                elif len(line) == 2:
                    self.__d_lines.append(DialogueLine(line[0], line[1]))
                elif len(line) == 3:
                    self.__d_lines.append(DialogueLine(line[0], line[1], line[2]))

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
    
    ### Map Level
    def get_obstacles(self) -> list[Rect]:
        return self.__obstacles

    def get_end_condition(self) -> EndCondition:
        return self.__quest_tracker.get_end_condition()

    def get_collectables(self) -> list[Object]:
        return self.__quest_tracker.get_active_objects()

    def set_player_position(self, position) -> None:
        self.__quest_tracker.set_player_position(position)

    def is_player_visible(self) -> bool:
        return self.__player_appear
    
    def get_player_spawn(self) -> Tuple[int, int]:
        return self.__player_spawn
    
    def center_on_player(self, player_rect: Rect) -> None:
        x, y = player_rect.x, player_rect.y
        self.__camera_offset = (configs.SCREEN_W//2 - x, configs.SCREEN_H//2 - y)

    def update(self) -> None:
        if self.__type == LevelType.MAP:
            self.__quest_tracker.update()
            if self.__quest_tracker.get_status() == GameState.GAME_LEVEL_END:
                self.__level_complete = True
    
    def is_level_complete(self) -> bool:
        return self.__level_complete

    ### Dialogue Level
    def __get_current_line(self) -> DialogueLine:
        return self.__d_lines[self.__d_line_index]
    
    def __get_active_character(self) -> DialogueCharacter:
        return self.__d_characters[self.__get_current_line().get_character_id()]
    
    def get_next_dialogue(self) -> GameState:
        if self.__d_line_index + 1 > len(self.__d_lines) - 1:
            return GameState.GAME_LEVEL_END
        else:
            self.__d_line_index += 1
            current_character = self.__get_current_line().get_character_id()
            for character_id in self.__d_characters:
                if current_character == character_id:
                    self.__d_characters[character_id].set_active()
                else:
                    self.__d_characters[character_id].set_inactive()

        return GameState.GAME_OK

    ### Drawing
    def draw(self, screen: Surface) -> None:
        screen.blit(self.__background, (0, 0))

        if self.__type == LevelType.MAP:
            for layer in self.__layers:
                screen.blit(layer.get_surface(), self.__camera_offset)
            screen.blit(self.__quest_tracker.get_surface(), self.__camera_offset)
        elif self.__type == LevelType.DIALOGUE:
            for character_id in self.__d_characters:
                if character_id == "":
                    continue
                character = self.__d_characters[character_id]
                if character_id == self.__get_current_line().get_character_id():
                    screen.blit(character.get_image(self.__get_current_line().get_emotion()), character.get_position())
                else:
                    screen.blit(character.get_image(), character.get_position())


            dialogue_surface = self.__d_background.copy()
            character_name = self.__get_active_character().get_name()
            character_colour = self.__get_active_character().get_colour()
            character_name_text = self.__d_name_font.render(character_name, True, character_colour)
            dialogue_surface.blit(character_name_text, (40, 10))
            text = self.__d_text_font.render(self.__get_current_line().get_line(), True, "white")
            dialogue_surface.blit(text, (40, 80))
            screen.blit(dialogue_surface, self.__d_bg_position)
        else:
            pass  # Blank level
