from settings import *
import pygame
import math
from map import collision_walls
from weapons import weapon_list

class Player:
    def __init__(self, sprites):
        self.curwep = 1
        self.x, self.y = player_pos
        self.sprites = sprites
        self.angle = player_angle
        self.sensitivity = 0.004
        self.skillpoints = 0
        self.speed = 1
        self.meleedmg = 1
        self.manacost = 1
        self.sheild = 1
        self.max_hp = 5
        self.hp = 5
        self.max_mana = 3
        self.managen = 0
        self.mana = 3
        self.xp = 0
        self.lvl = 1
        # collision parameters
        self.side = 50
        self.rect = pygame.Rect(*player_pos, self.side, self.side)
        # weapon
        self.shot = False
        self.weaponi = 'woodensword'

    def mana(self):
        return self.mana

    def max_mana(self):
        return self.max_mana

    def hp(self):
        return self.hp

    def max_hp(self):
        return self.max_hp

    def dmg(self, damage):
        self.hp -= damage

    def level_up(self):
        if self.xp >= self.lvl * 10:
            self.xp -= self.lvl * 10
            self.lvl += 1
            self.max_hp += 2
            self.max_mana += 1
            self.skillpoints += max(0, 3 - (self.lvl // 5))

    def xp(self):
        return self.xp

    def lvl(self):
        return self.lvl

    def heal(self, healing):
        self.hp += healing

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def collision_list(self):
        return collision_walls + [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  self.sprites.list_of_objects if obj.blocked]

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def weapon(self):
        return weapon_list[self.weaponi]

    def movement(self):
        self.keys_control()
        self.mouse_control()
        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_w]:
            dx = (player_speed * self.speed) * cos_a
            dy = (player_speed * self.speed) * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_s]:
            dx = -(player_speed * self.speed) * cos_a
            dy = -(player_speed * self.speed) * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = (player_speed * self.speed) * sin_a
            dy = -(player_speed * self.speed) * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -(player_speed * self.speed) * sin_a
            dy = (player_speed * self.speed) * cos_a
            self.detect_collision(dx, dy)

        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02


    def mouse_control(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * self.sensitivity

