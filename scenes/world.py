from classes.level import Level
from classes.player import Player
from classes.scene import Scene
from pygame.surface import Surface
from classes.states import PlayerDirection
import pygame


class World(Scene):
    def __init__(self) -> None:
        super().__init__()

        self.__player: Player = Player()
        
        level_1: Level = Level("assets/levels/1")
        super().load_level(1, level_1)

    def update(self, dt: float) -> None:
        super().update(dt)

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

        # Checking collisions
        for obstacle in self.get_current_level().get_obstacles():
            if obstacle.colliderect(self.__player.get_rect()):
                self.__player.collide()

        # Updating player
        self.__player.update(dt)

    def change_level(self, level_nr: int) -> None:
        super().change_level(level_nr)
        self.__player.teleport(super().get_current_level().get_player_spawn())

    def draw(self, screen: Surface) -> None:
        self.get_current_level().draw(screen)
        screen.blit(self.__player.get_surface(), self.__player.get_rect())
        super().draw(screen)
