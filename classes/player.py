from typing import Tuple
from pygame.rect import Rect
from pygame.surface import Surface
from classes.spritesheet import Spritesheet
from classes.states import PlayerDirection


class Player():
    ANIMATION_INTERVAL = 0.1
    SPEED = 150

    def __init__(self) -> None:
        spritesheet: Spritesheet = Spritesheet("assets/images/elf_spritesheet.png", (18, 18), 4)

        self.__sprite_directions = [PlayerDirection.DOWN,
                                    PlayerDirection.UP,
                                    PlayerDirection.RIGHT,
                                    PlayerDirection.LEFT]
        self.__sprites: dict[PlayerDirection, list[Surface]] = spritesheet.get_dictionary(self.__sprite_directions)

        # Movement
        self.__prev_direction = PlayerDirection.DOWN
        self.__direction = PlayerDirection.DOWN

        # Position
        self.__prev_position: Tuple[float, float] = (0, 0)
        self.__position: Tuple[float, float] = (0, 0)
        self.__colliding: bool = False

        # Animation
        self.__current_frame = 0
        self.__max_frames = len(self.__sprites[next(iter(self.__sprites))])
        self.__animation_timer: float = 0
    
    def move(self, dt: float, direction: PlayerDirection) -> None:
        if direction == PlayerDirection.STAY:
            if self.__direction != PlayerDirection.STAY:
                self.__prev_direction = self.__direction
            
            self.__direction = direction
        else:
            self.__prev_direction = self.__direction
            self.__direction = direction

            direction_x = 0
            direction_y = 0
            match direction:
                case PlayerDirection.RIGHT:
                    direction_x = 1
                case PlayerDirection.LEFT:
                    direction_x = -1
                case PlayerDirection.DOWN:
                    direction_y = 1
                case PlayerDirection.UP:
                    direction_y = -1
            
            new_x = self.__position[0] + (dt * direction_x * Player.SPEED)
            new_y = self.__position[1] + (dt * direction_y * Player.SPEED)
            
            self.__prev_position = self.__position
            self.__position = (new_x, new_y)
    
    def teleport(self, pos: Tuple[int, int]) -> None:
        self.__position = pos
        self.__prev_position = pos

    def set_collided(self) -> None:
        self.__colliding = True

    def update(self, dt: float) -> None:
        if self.__colliding:
            self.__colliding = False
            self.__position = self.__prev_position
        
        self.__update_animation(dt)

    def __update_animation(self, dt: float) -> None:
        self.__animation_timer += dt
        if self.__direction == PlayerDirection.STAY:
            self.__current_frame = 0
            self.__animation_timer = 0
        else:
            if self.__prev_direction == PlayerDirection.STAY:
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
        if direction == PlayerDirection.STAY:
            direction = self.__prev_direction
        return self.__sprites[direction][self.__current_frame]

    def get_rect(self):
        position = int(self.__position[0]), int(self.__position[1])
        return self.get_surface().get_rect(topleft=position)
