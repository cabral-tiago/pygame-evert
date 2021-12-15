from typing import Tuple
from pygame.rect import Rect
from classes.button import Button
from classes.hitfx import HitFX
from classes.level import Level
from classes.enemy import Enemy
from classes.player import Player
from classes.projectile import Projectile
from classes.projectiles.fireball import Fireball
from classes.scene import Scene
from pygame.surface import Surface
from classes.enums import EndCondition, GameState, LevelType, Direction
import pygame
import configs
import os


class World(Scene):
    WASD_KEYS = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d,
                pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]

    def __init__(self) -> None:
        super().__init__()

        # Player
        self.__player: Player = Player()
        self.__player_fireballs: list[Projectile] = []
        self.__wasd_down: list[int] = []

        # Enemy
        self.__enemy_projectiles: list[Projectile] = []

        # HitFX
        self.__hitfx: list[HitFX] = []

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

            if not self.__player.is_alive():
                return GameState.GAME_DEAD

        return super().update(dt)

    def __update_map(self, dt: float) -> None:
        ### HitFX
        for hitfx in self.__hitfx:
            hitfx.update(dt)

        self.__hitfx[:] = [hitfx for hitfx in self.__hitfx if hitfx.is_alive()]

        self.get_current_level().set_hitfx(self.__hitfx)

        ### Enemies
        for enemy in self.get_current_level().get_enemies():
            enemy.update(dt)

            # Shooting
            if enemy.can_shoot():
                projectile = enemy.shoot()
                if projectile:
                    self.__enemy_projectiles.append(projectile)
            
            # World collisions
            if enemy.get_rect().collidelist(self.get_current_level().get_obstacles()) != -1:
                enemy.set_world_collision()
            
            # Other enemies collisions
            for other_enemy in self.get_current_level().get_enemies():
                if other_enemy is enemy:
                    continue
                if other_enemy.get_rect().colliderect(enemy.get_rect()):
                    enemy.set_world_collision()
            
            # Player collision
            if enemy.get_rect().colliderect(self.__player.get_rect()):
                enemy.set_world_collision()

        ### Player
        self.__player.move(dt, self.get_last_wasd())

        # Updating all projectiles
        for projectile in self.__enemy_projectiles:
            projectile.update(dt)

            # Kill projectile if it collides with obstacles in the World.
            if projectile.get_rect().collidelist(self.get_current_level().get_obstacles()) != -1:
                projectile.die()
            
            # Registering the hit on the player
            if projectile.get_rect().colliderect(self.__player.get_rect()):
                self.__player.take_damage(projectile.DAMAGE)
                self.__hitfx.append(HitFX(projectile.get_hitfx(), self.__player.get_rect().center))
                projectile.die()

        self.__enemy_projectiles[:] = [prj for prj in self.__enemy_projectiles if prj.is_alive()]

        for fireball in self.__player_fireballs:
            fireball.update(dt)

            # Kill projectile if it collides with obstacles in the World.
            if fireball.get_rect().collidelist(self.get_current_level().get_obstacles()) != -1:
                fireball.die()
            
            # Registering the hit on the enemy
            for enemy in self.get_current_level().get_enemies():
                if fireball.get_rect().colliderect(enemy.get_rect()):
                    enemy.take_damage(fireball.DAMAGE)
                    self.__hitfx.append(HitFX(fireball.get_hitfx(), enemy.get_rect().center))
                    fireball.die()
                    break

        self.__player_fireballs[:] = [fireball for fireball in self.__player_fireballs if fireball.is_alive()]

        # Sending projectiles to Level
        self.get_current_level().set_projectiles(self.__player_fireballs + self.__enemy_projectiles)

        ### Player collisions
        # With obstacles
        if self.__player.get_rect().collidelist(self.get_current_level().get_obstacles()) != -1:
            self.__player.set_collided()
        
        # With enemies
        for enemy in self.get_current_level().get_enemies():
            if self.__player.get_rect().colliderect(enemy.get_rect()):
                self.__player.set_collided()

        # With collectables
        for collectable in self.get_current_level().get_active_collectables():
            if collectable.get_rect().colliderect(self.__player.get_rect()):
                collectable.set_collected()
        
        # Check if player is at the end of the level
        if self.get_current_level().get_end_condition() == EndCondition.RETURN_WHEN_DONE and \
                self.get_current_level().get_end_position().colliderect(self.__player.get_rect()):
            self.get_current_level().set_player_at_end()

        # Updating player
        self.__player.update(dt)

        # Setting player surface on Level to be drawn at the right Z_Height

        if self.get_current_level().is_player_visible():
            self.get_current_level().center_on_player(self.__player.get_rect())
            self.get_current_level().set_player_surface(self.__player.get_surface())

    def change_level(self, level_nr: int) -> None:
        super().change_level(level_nr)

        if self.get_current_level().get_type() == LevelType.MAP:
            self.__player.teleport(self.get_current_level().get_player_spawn(),
                                   self.get_current_level().get_player_spawn_direction())
            self.__dialogue_button.hide()
        elif self.get_current_level().get_type() == LevelType.DIALOGUE:
            self.__dialogue_button.show()
    
    def reset(self) -> None:
        super().reset()
        self.__wasd_down = []
        self.__player_fireballs = []
        self.__enemy_projectiles = []
        self.__hitfx = []
        self.__player.reset()
        self.change_level(1)

    def reset_level(self) -> None:
        super().reset_level()
        self.__wasd_down = []
        self.__player_fireballs = []
        self.__enemy_projectiles = []
        self.__hitfx = []
        self.__player.reset()
        self.__player.teleport(self.get_current_level().get_player_spawn(),
                               self.get_current_level().get_player_spawn_direction())

    def handle_key_down(self, key: int) -> GameState:
        if key == pygame.K_SPACE:
            if self.get_current_level().get_type() == LevelType.DIALOGUE:
                return GameState.GAME_NEXT_DIALOGUE
            if self.get_current_level().get_type() == LevelType.MAP and self.__player.can_shoot():
                self.__player_fireballs.append(self.__player.shoot())
        if key in self.WASD_KEYS and key not in self.__wasd_down:
            self.__wasd_down.append(key)
        if key == pygame.K_ESCAPE:
            self.__wasd_down = []
            return GameState.GAME_PAUSE

        return super().handle_key_down(key)
    
    def handle_key_up(self, key: int) -> GameState:
        if key in self.WASD_KEYS:
            if key in self.__wasd_down:
                self.__wasd_down.remove(key)
    
        return super().handle_key_up(key)
    
    def get_last_wasd(self) -> int:
        if len(self.__wasd_down) > 0:
            return self.__wasd_down[-1]
        else:
            return -1

    def draw(self, screen: Surface) -> None:
        self.get_current_level().draw(screen)
        if self.get_current_level().is_player_visible():
            # Draw bottom bar
            screen.blit(self.__black_bar, (0, configs.SCREEN_H - configs.BAR_HEIGHT))

            # Draw HP Bar
            screen.blit(self.__player.get_hpbar_surface(),
                        (configs.SCREEN_W//2 - self.__player.get_hpbar_surface().get_width()//2,
                         configs.SCREEN_H - self.__player.get_hpbar_surface().get_height() - 4))
        
        super().draw(screen)
