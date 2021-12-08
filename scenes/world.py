from classes.button import Button
from classes.buttongroup import ButtonGroup
from classes.level import Level
from classes.player import Player
from classes.scene import Scene
from pygame.surface import Surface
from classes.enums import EndCondition, GameState, LevelType, PlayerDirection
import pygame
import configs
import os


class World(Scene):
    def __init__(self) -> None:
        super().__init__()

        # Player
        self.__player: Player = Player()

        # Dialogue button
        dialogue_box_size = (configs.SCREEN_W,configs.CHARACTER_SIZE[1]/3)
        dialogue_box_position = (0, configs.SCREEN_H - dialogue_box_size[1])
        dialogue_button = Button("", dialogue_box_size, dialogue_box_position, GameState.GAME_NEXT_DIALOGUE, True)
        self.__dialogue_box: ButtonGroup = ButtonGroup()
        self.__dialogue_box.add_button(dialogue_button)
        super().add_button_group(self.__dialogue_box)

        # Loading all levels        
        levels_folder = "assets/levels/"
        levels = [f.name for f in os.scandir(levels_folder) if int(f.name) > 0]
        for level_nr in levels:
            level = Level("assets/levels/" + level_nr)
            super().load_level(int(level_nr), level)

    def update(self, dt: float) -> GameState:
        if self.get_current_level().get_type() == LevelType.MAP:
            self.__update_map(dt)
        
        return super().update(dt)

    def __update_map(self, dt: float) -> None:
        player_direction = PlayerDirection.STAY
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_direction = PlayerDirection.RIGHT
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_direction = PlayerDirection.LEFT
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player_direction = PlayerDirection.UP
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player_direction = PlayerDirection.DOWN
        
        self.__player.move(dt, player_direction)

        ### Player collisions
        # With obstacles
        for obstacle in self.get_current_level().get_obstacles():
            if obstacle.colliderect(self.__player.get_rect()):
                self.__player.set_collided()

        # With collectables
        for collectable in self.get_current_level().get_active_collectables():
            if collectable.get_rect().colliderect(self.__player.get_rect()):
                collectable.set_collected()
        
        # Check if player is at the end of the level
        if self.get_current_level().get_end_condition() == EndCondition.RETURN_WHEN_DONE and \
                self.get_current_level().get_end_position().colliderect(self.__player.get_rect()):
            self.get_current_level().set_player_at_end()

        # With the world edges
        if (self.__player.get_rect().x < 0
                or self.__player.get_rect().x > self.get_current_level().get_width() - self.__player.get_rect().width
                or self.__player.get_rect().y < 0
                or self.__player.get_rect().y > self.get_current_level().get_height() - self.__player.get_rect().height):
            self.__player.set_collided()

        # Updating player
        self.__player.update(dt)

        if self.get_current_level().is_player_visible():
            self.get_current_level().center_on_player(self.__player.get_rect())

    def change_level(self, level_nr: int) -> None:
        super().change_level(level_nr)

        if self.get_current_level().get_type() == LevelType.MAP:
            self.__player.teleport(self.get_current_level().get_player_spawn())
            self.__dialogue_box.hide()
        elif self.get_current_level().get_type() == LevelType.DIALOGUE:
            self.__dialogue_box.show()

    def draw(self, screen: Surface) -> None:
        self.get_current_level().draw(screen)
        if self.get_current_level().is_player_visible():
            screen.blit(self.__player.get_surface(), (configs.SCREEN_W//2, configs.SCREEN_H//2))
        
        super().draw(screen)
