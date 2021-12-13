from pygame.rect import Rect
from classes.button import Button
from classes.level import Level
from classes.enemies.monster import Monster
from classes.player import Player
from classes.projectiles.fireball import Fireball
from classes.scene import Scene
from pygame.surface import Surface
from classes.enums import EndCondition, GameState, LevelType, Direction
import pygame
import configs
import os


class World(Scene):
    def __init__(self) -> None:
        super().__init__()

        # Player
        self.__player: Player = Player()
        self.__player_fireballs: list[Fireball] = []

        # Bottom bar
        self.__black_bar = Surface((configs.SCREEN_W, configs.BAR_HEIGHT))
        self.__black_bar.fill("black")

        # Dialogue button
        dialogue_box_rect = Rect((0, configs.SCREEN_H - configs.CHARACTER_SIZE[1]/3),
                                 (configs.SCREEN_W, configs.CHARACTER_SIZE[1]/3))
        self.__dialogue_button = Button("", dialogue_box_rect, GameState.GAME_NEXT_DIALOGUE, True)
        super().add_button(self.__dialogue_button)

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
        ### Monsters
        for monster in self.get_current_level().get_monsters():
            monster.move(dt)
            
            # World collisions
            for obstacle in self.get_current_level().get_obstacles():
                if obstacle.colliderect(monster.get_rect()):
                    monster.set_world_collision()

            # World edges
            if (monster.get_rect().x < 0
                or monster.get_rect().x > self.get_current_level().get_width() - monster.get_rect().width
                or monster.get_rect().y < 0
                or monster.get_rect().y > self.get_current_level().get_height() - monster.get_rect().height):
                monster.set_world_collision()

        ### Player
        player_direction = Direction.STAY
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_direction = Direction.RIGHT
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_direction = Direction.LEFT
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player_direction = Direction.UP
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player_direction = Direction.DOWN
        
        self.__player.move(dt, player_direction)

        ### Player shooting
        if self.__player.can_shoot() and keys[pygame.K_SPACE]:
            self.__player_fireballs.append(self.__player.shoot())

        for fireball in self.__player_fireballs:
            fireball.update(dt)

        self.__player_fireballs[:] = [fireball for fireball in self.__player_fireballs if fireball.is_alive()]

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

        # Updating fireballs on Level
        self.get_current_level().set_projectiles(self.__player_fireballs)

        if self.get_current_level().is_player_visible():
            self.get_current_level().center_on_player(self.__player.get_rect())

    def change_level(self, level_nr: int) -> None:
        super().change_level(level_nr)

        if self.get_current_level().get_type() == LevelType.MAP:
            self.__player.teleport(self.get_current_level().get_player_spawn())
            self.__dialogue_button.hide()
        elif self.get_current_level().get_type() == LevelType.DIALOGUE:
            self.__dialogue_button.show()
    
    def reset(self) -> None:
        super().reset()
        self.change_level(1)

    def draw(self, screen: Surface) -> None:
        self.get_current_level().draw(screen)
        if self.get_current_level().is_player_visible():
            # Draw player
            screen.blit(self.__player.get_surface(),
                        (configs.SCREEN_W / 2 - self.__player.get_surface().get_width() / 2,
                         configs.SCREEN_H / 2 - self.__player.get_surface().get_height() / 2))

            # Draw bottom bar
            screen.blit(self.__black_bar, (0, configs.SCREEN_H - configs.BAR_HEIGHT))

            # Draw HP Bar
            screen.blit(self.__player.get_hpbar_surface(),
                        (configs.SCREEN_W//2 - self.__player.get_hpbar_surface().get_width()//2,
                         configs.SCREEN_H - self.__player.get_hpbar_surface().get_height() - 4))
        
        super().draw(screen)
