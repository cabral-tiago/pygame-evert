from typing import Tuple
from pygame.rect import Rect
from pygame.surface import Surface
from classes.projectiles.bullet import Bullet
from classes.spritesheet import Spritesheet
from classes.enums import Direction
import pygame


class Player:
    MAX_HP = 420
    ANIMATION_INTERVAL = 0.1
    SPEED = 150
    SHOOTING_COOLDOWN = 1

    def __init__(self) -> None:
        spritesheet: Spritesheet = Spritesheet("assets/images/jesse_sprite.png", (15, 18), 4)

        self.__sprite_directions = [Direction.DOWN,
                                    Direction.UP,
                                    Direction.RIGHT,
                                    Direction.LEFT]
        self.__sprites: dict[Direction, list[Surface]] = spritesheet.get_dictionary(self.__sprite_directions)

        # Movement
        self.__prev_direction = Direction.DOWN
        self.__direction = Direction.DOWN

        # Position
        self.__prev_position: Tuple[float, float] = (0, 0)
        self.__position: Tuple[float, float] = (0, 0)
        self.__colliding: bool = False

        # Animation
        self.__current_frame = 0
        self.__max_frames = len(self.__sprites[next(iter(self.__sprites))])
        self.__animation_timer: float = 0

        # Shooting cooldown
        self.__shooting_cooldown = 0

        # HP
        self.__hp = Player.MAX_HP
        self.__hp_font = pygame.font.Font("assets/fonts/Roboto-Medium.ttf", 22)
        self.__hpbar_border = 4
        self.__hpbar_bg = Surface((Player.MAX_HP + self.__hpbar_border * 2, 46), pygame.SRCALPHA)
        pygame.draw.rect(self.__hpbar_bg, "gray10", Rect((0, 0), self.__hpbar_bg.get_size()), border_radius=4)
        pygame.draw.rect(self.__hpbar_bg, "red4", Rect((0, 0), self.__hpbar_bg.get_size()), self.__hpbar_border, 4)
    
    def move(self, dt: float, direction: Direction) -> None:
        if direction == Direction.STAY:
            if self.__direction != Direction.STAY:
                self.__prev_direction = self.__direction
            
            self.__direction = direction
        else:
            self.__prev_direction = self.__direction
            self.__direction = direction

            direction_x = 0
            direction_y = 0
            match direction:
                case Direction.RIGHT:
                    direction_x = 1
                case Direction.LEFT:
                    direction_x = -1
                case Direction.DOWN:
                    direction_y = 1
                case Direction.UP:
                    direction_y = -1
            
            new_x = self.__position[0] + (dt * direction_x * Player.SPEED)
            new_y = self.__position[1] + (dt * direction_y * Player.SPEED)
            
            self.__prev_position = self.__position
            self.__position = (new_x, new_y)

    def can_shoot(self) -> bool:
        if self.__shooting_cooldown <= 0:
            return True
        return False

    def shoot(self) -> Bullet:
        self.__shooting_cooldown = Player.SHOOTING_COOLDOWN

        if self.__direction == Direction.STAY:
            return Bullet(self.get_rect().center, self.__prev_direction)
        return Bullet(self.get_rect().center, self.__direction)
    
    def get_hp(self) -> int:
        return self.__hp

    def get_hpbar_surface(self) -> Surface:
        surface = self.__hpbar_bg.copy()
        bar_size = Rect(self.__hpbar_border,
                        self.__hpbar_border,
                        self.get_hp(),
                        self.__hpbar_bg.get_height() - self.__hpbar_border * 2)
        pygame.draw.rect(surface, "red", bar_size)
        hp_text = self.__hp_font.render(f"HP: {self.__hp}/{Player.MAX_HP}", True, "white")
        surface.blit(hp_text, (self.__hpbar_border * 2, surface.get_height()//2 - hp_text.get_height() // 2))
        return surface
    
    def teleport(self, pos: Tuple[int, int]) -> None:
        position = self.get_surface().get_rect(topleft=pos).center
        self.__position = position
        self.__prev_position = position

    def set_collided(self) -> None:
        self.__colliding = True

    def update(self, dt: float) -> None:
        self.__shooting_cooldown -= dt

        if self.__colliding:
            self.__colliding = False
            self.__position = self.__prev_position
        
        self.__update_animation(dt)

    def __update_animation(self, dt: float) -> None:
        self.__animation_timer += dt
        if self.__direction == Direction.STAY:
            self.__current_frame = 0
            self.__animation_timer = 0
        else:
            if self.__prev_direction == Direction.STAY:
                self.__current_frame = 1
                self.__animation_timer = 0

            if self.__direction != self.__prev_direction:
                self.__current_frame = 1
                self.__animation_timer = 0

            if self.__animation_timer > Player.ANIMATION_INTERVAL:
                self.__animation_timer -= Player.ANIMATION_INTERVAL
                self.__current_frame += 1
                if self.__current_frame > self.__max_frames - 1:
                    self.__current_frame = 0

    def get_surface(self) -> Surface:
        direction = self.__direction
        if direction == Direction.STAY:
            direction = self.__prev_direction
        return self.__sprites[direction][self.__current_frame]

    def get_rect(self):
        position = int(self.__position[0]), int(self.__position[1])
        return self.get_surface().get_rect(center=position)
    