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
        # TODO: Implement player_direction as a state in states.py
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
        
        player_position = self.__player.position
        movement_x = 0
        movement_y = 0
        match player_direction:
            case PlayerDirection.RIGHT:
                movement_x = 1
            case PlayerDirection.LEFT:
                movement_x = -1
            case PlayerDirection.DOWN:
                movement_y = 1
            case PlayerDirection.UP:
                movement_y = -1
        
        next_x = player_position[0] + (dt * movement_x * Player.SPEED)
        next_y = player_position[1] + (dt * movement_y * Player.SPEED)

        #TODO: Check collissions

        # Applying position
        self.__player.position = (next_x, next_y)

        self.__player.update_animation(dt, player_direction)

    def change_level(self, level_nr: int) -> None:
        super().change_level(level_nr)
        # TODO

    def draw(self, screen: Surface) -> None:
        self.get_current_level().draw(screen)
        screen.blit(self.__player.get_surface(), self.__player.position)
        super().draw(screen)
