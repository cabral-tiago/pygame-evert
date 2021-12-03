from classes.button import Button
from classes.level import Level
from classes.player import Player
from classes.scene import Scene
from pygame.surface import Surface
from classes.enums import GameState, LevelType, PlayerDirection
import pygame
import configs


class World(Scene):
    def __init__(self) -> None:
        super().__init__()

        self.__player: Player = Player()

        # Dialogue button
        dialogue_hud_size = (configs.SCREEN_W,configs.CHARACTER_SIZE[1]/3)
        dialogue_hud_position = (0, configs.SCREEN_H - dialogue_hud_size[1])
        button = Button("", dialogue_hud_size, dialogue_hud_position, GameState.GAME_NEXT_DIALOGUE, transparent = True)
        super().add_button(button)
        
        level_1: Level = Level("assets/levels/1")
        super().load_level(1, level_1)

        level_2: Level = Level("assets/levels/2")
        super().load_level(2, level_2)

    def update(self, dt: float) -> None:
        super().update(dt)

        match self.get_current_level().get_type():
            case LevelType.MAP:
                self.__update_map(dt)
            case LevelType.DIALOGUE:
                self.__update_dialogue(dt)

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

    def __update_dialogue(self, dt: float) -> None:
        pass

    def change_level(self, level_nr: int) -> None:
        super().change_level(level_nr)

        if self.get_current_level().get_type() == LevelType.MAP:
            self.__player.teleport(self.get_current_level().get_player_spawn())

    def draw(self, screen: Surface) -> None:
        self.get_current_level().draw(screen)
        if self.get_current_level().is_player_visible():
            screen.blit(self.__player.get_surface(), (configs.SCREEN_W//2, configs.SCREEN_H//2))
        
        if self.get_current_level().get_type() == LevelType.DIALOGUE:
            super().draw(screen)  # To draw the "button"
