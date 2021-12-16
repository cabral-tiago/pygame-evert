from typing import Tuple, Any
from pygame.mixer import Sound
from pygame.surface import Surface
from pygame.rect import Rect
from classes.enums import Direction
import random
import pygame


class Enemy:
    SPEED = 80
    SHOOTS = False
    SHOOTING_FREQ = 2
    CHANGE_DIRECTION_FREQ = 3
    MAX_HP = 100

    def __init__(self, surface: Surface, position: Tuple[int, int], directions: list[Direction], hurt: Sound) -> None:
        self.__surface = surface
        self.__position: Tuple[float, float] = position
        self.__prev_position: Tuple[float, float] = position

        # Hurt SFX
        self.__hurt: Sound = hurt
        
        # Direction
        self.__posible_directions: list[Direction] = directions
        self.__direction: Direction = random.choice(self.__posible_directions)
        self.__changedir_timer = 0
        
        # HP
        self.__hp: int = self.MAX_HP

        # HP Bar
        self.__hpbar_max_width = round(surface.get_width(), -1)
        self.__hpbar_height = (self.__hpbar_max_width / 10) * 2
        
        full_width = max(self.__hpbar_max_width, surface.get_width())
        full_height = int(self.__hpbar_height * 1.5) + surface.get_height()
        
        self.__hpbar_offset = (full_width - self.__hpbar_max_width) // 2

        self.__scaled_surface: Surface = Surface((full_width, full_height), pygame.SRCALPHA)
        offset_x = (full_width - surface.get_width()) // 2
        if offset_x > 0:
            self.__scaled_surface.blit(surface, (offset_x, int(self.__hpbar_height * 1.5)))
        else:
            self.__scaled_surface.blit(surface, (0, int(self.__hpbar_height * 1.5)))

        # Shooting
        self.__shooting_timer = 0

    def update(self, dt: float) -> None:
        # Timers
        self.__changedir_timer += dt
        if self.__changedir_timer >= self.CHANGE_DIRECTION_FREQ:
            self.__change_direction()
        
        self.__shooting_timer += dt

        # Update position
        direction_x = 0
        direction_y = 0
        match self.__direction:
            case Direction.RIGHT:
                direction_x = 1
            case Direction.LEFT:
                direction_x = -1
            case Direction.DOWN:
                direction_y = 1
            case Direction.UP:
                direction_y = -1
        
        new_x = self.__position[0] + (dt * direction_x * self.SPEED)
        new_y = self.__position[1] + (dt * direction_y * self.SPEED)
        
        self.__prev_position = self.__position
        self.__position = (new_x, new_y)
    
    def __change_direction(self) -> None:
        self.__changedir_timer = 0

        direction = random.choice(self.__posible_directions)
        while self.__direction == direction:
            direction = random.choice(self.__posible_directions)
        
        self.__direction = direction
    
    def can_shoot(self) -> bool:
        return self.SHOOTS and self.__shooting_timer >= self.SHOOTING_FREQ

    def shoot(self) -> Any:
        '''
        Supposed to be overridden by the child class with its own projectile and logic. Should still call this through
        super().shoot() to update the timer. Can also be left without being overridden, in the case of a passive enemy
        that doesn't shoot (Enemy.SHOOTS == False).
        '''
        self.__shooting_timer = 0
    
    def set_world_collision(self) -> None:
        self.__position = self.__prev_position

        self.__change_direction()

    def is_alive(self) -> bool:
        return self.__hp > 0
    
    def take_damage(self, damage: int) -> None:
        self.__hp -= damage
        self.__hurt.play()
        if self.__hp <= 0:
            self.__hp = 0
    
    def reset(self) -> None:
        self.__hp = self.MAX_HP

    def get_surface(self) -> Surface:
        return self.__surface
    
    def get_surface_with_hp(self) -> Surface:
        surface = self.__scaled_surface.copy()
        width = int((self.__hp * self.__hpbar_max_width) / self.MAX_HP)
        pygame.draw.rect(surface, "red", Rect((self.__hpbar_offset, 0),(width, self.__hpbar_height)))
        return surface

    def get_rect(self) -> Rect:
        position = (int(self.__position[0]), int(self.__position[1]))
        return self.get_surface().get_rect(center=position)
