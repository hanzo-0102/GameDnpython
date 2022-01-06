from settings import *
from map import world_map
from ray_casting import mapping
import math
import pygame
import random



def ray_casting_npc_player(npc_x, npc_y, blocked_doors, world_map, player_pos):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    cur_angle = math.atan2(delta_y, delta_x)
    cur_angle += math.pi

    sin_a = math.sin(cur_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = math.cos(cur_angle)
    cos_a = cos_a if cos_a else 0.000001

    # verticals
    x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)) // TILE):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in world_map or tile_v in blocked_doors:
            return False
        x += dx * TILE

    # horizontals
    y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // TILE):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in world_map or tile_h in blocked_doors:
            return False
        y += dy * TILE
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing
        self.pain_sound = pygame.mixer.Sound('sound/pain.mp3')

    def interaction_objects(self):
        if self.player.shot and self.drawing.shot_animation_trigger:
            for obj in sorted(self.sprites.list_of_objects, key=lambda obj: obj.distance_to_sprite):
                if obj.is_on_fire[1]:
                    if obj.is_dead != 'immortal' and not obj.is_dead:
                        if obj.is_on_fire[1] >= self.player.weapon().dist:
                            obj.health -= self.player.weapon().damage
                            if obj.health <= 0:
                                if ray_casting_npc_player(obj.x, obj.y,
                                                          [],
                                                          world_map, self.player.pos):
                                    if obj.flag == 'npc':
                                        self.pain_sound.play()
                                    obj.is_dead = True
                                    obj.blocked = None
                                    self.drawing.shot_animation_trigger = False

    def npc_action(self):
        for obj in self.sprites.list_of_objects:
            if obj.flag == 'npc' and not obj.is_dead:
                if ray_casting_npc_player(obj.x, obj.y,
                                          [],
                                          world_map, self.player.pos):
                    obj.npc_action_trigger = True
                    self.npc_move(obj)
                    obj.npc_shoot(self.sprites.list_of_objects, self.player)
                else:
                    obj.npc_action_trigger = False
            elif obj.flag == 'bullet':
                self.npc_move(obj)
            elif obj.flag == 'farmland' and obj.stage != 3:
                obj.time_to_grow -= 1
                if obj.time_to_grow == 0:
                    obj.stage += 1
                    obj.object = pygame.image.load(f'sprites/{obj.item}/base/{obj.stage - 1}.png').convert_alpha()
                    obj.time_to_grow = random.randint(1000, 10000)

    def npc_move(self, obj):
        if (abs(obj.distance_to_sprite) > TILE):
            dx = obj.x - self.player.pos[0]
            dy = obj.y - self.player.pos[1]
            obj.x = obj.x + obj.speed if dx < 0 else obj.x - obj.speed
            obj.y = obj.y + obj.speed if dy < 0 else obj.y - obj.speed
            if obj.x < 0 or obj.x > 24 or obj.y < 0 or obj.y > 15:
                del obj

    def clear_world(self):
        deleted_objects = self.sprites.list_of_objects[:]
        [self.sprites.list_of_objects.remove(obj) for obj in deleted_objects if obj.delete]

    def play_music(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('sound/theme.mp3')
        pygame.mixer.music.play(10)