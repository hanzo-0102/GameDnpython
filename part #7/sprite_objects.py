import random

import pygame
from settings import *
from collections import deque
from ray_casting import mapping
from inventory_test import Item



class Sprites:
    def __init__(self):
        self.sprite_parameters = {
            'sprite_vase': {
                'sprite': pygame.image.load('sprites/vase/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.6,
                'scale': (0.8, 0.8),
                'side': 30,
                'animation': deque(
                    [pygame.image.load(f'sprites/vase/anim/{i}.png').convert_alpha() for i in range(1)]),
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 2.6,
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'decor',
                'obj_action': [],
                'drop': {}
            },
            'sprite_flame': {
                'sprite': pygame.image.load('sprites/flame/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.7,
                'scale': (0.6, 0.6),
                'side': 30,
                'animation': deque(
                    [pygame.image.load(f'sprites/flame/anim/{i}.png').convert_alpha() for i in range(16)]),
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 1.8,
                'animation_dist': 1800,
                'animation_speed': 5,
                'blocked': None,
                'flag': 'decor',
                'obj_action': [],
                'drop': {}
            },
            'npc_orc': {
                'sprite': [pygame.image.load(f'sprites/orc/base/{i // 2}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 1,
                'scale': (0.8, 0.8),
                'side': 50,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/orc/death/{i}.png')
                                           .convert_alpha() for i in range(2)]),
                'is_dead': None,
                'dead_shift': 1,
                'animation_dist': None,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque(
                    [pygame.image.load(f'sprites/orc/anim/{i}.png').convert_alpha() for i in range(3)]),
                'drop': {}
            },
            'npc_skeleton': {
                'sprite': [pygame.image.load(f'sprites/skeleton/base/{i // 2}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.8,
                'scale': (0.8, 0.8),
                'side': 30,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/skeleton/death/{i}.png')
                                         .convert_alpha() for i in range(4)]),
                'is_dead': None,
                'dead_shift': 0.8,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pygame.image.load(f'sprites/skeleton/anim/{i}.png')
                                    .convert_alpha() for i in range(3)]),
                'drop': {80: 'bone', 40: 'woodensword'}
            },
            'npc_trader': {
                'sprite': pygame.image.load('sprites/trader/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.8,
                'scale': (0.8, 0.8),
                'side': 30,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'flag': 'trader',
                'obj_action': [],
                'drop': {}
            },
            'npc_bee': {
                'sprite': pygame.image.load('sprites/bee/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.8,
                'scale': (0.8, 0.8),
                'side': 30,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/bee/death/{i}.png')
                                         .convert_alpha() for i in range(6)]),
                'is_dead': None,
                'dead_shift': 0.8,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pygame.image.load(f'sprites/bee/anim/{i}.png')
                                    .convert_alpha() for i in range(3)]),
                'drop': {30:'healshroom', 20:'manashroom'}
            },
            'npc_chiken': {
                'sprite': pygame.image.load('sprites/chiken/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.8,
                'scale': (0.8, 0.8),
                'side': 30,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/chiken/death/{i}.png')
                                         .convert_alpha() for i in range(6)]),
                'is_dead': None,
                'dead_shift': 0.8,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pygame.image.load(f'sprites/chiken/anim/{i}.png')
                                    .convert_alpha() for i in range(3)]),
                'drop': {100: 'chiken'}
            },
            'npc_irongolem': {
                'sprite': pygame.image.load(f'sprites/irongolem/base/0.png').convert_alpha(),
                'viewing_angles': False,
                'shift': 0.4,
                'scale': (1.2, 1.2),
                'side': 30,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/irongolem/death/{i}.png')
                                         .convert_alpha() for i in range(9)]),
                'is_dead': None,
                'dead_shift': 0.8,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pygame.image.load(f'sprites/irongolem/anim/{i}.png')
                                    .convert_alpha() for i in range(3)]),
                'drop': {10: 'golemgun'}
            },
            'ogr_trader': {
                'sprite': pygame.image.load(f'sprites/ogr/base/0.png').convert_alpha(),
                'viewing_angles': False,
                'shift': 0.4,
                'scale': (1.2, 1.2),
                'side': 30,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0.8,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'flag': 'trader',
                'obj_action': deque([pygame.image.load(f'sprites/ogr/anim/{i}.png')
                                    .convert_alpha() for i in range(1)]),
                'drop': {}
            }
        }

        self.list_of_objects = [
            SpriteObject(self.sprite_parameters['sprite_vase'], (7.1, 2.1)),
            SpriteObject(self.sprite_parameters['sprite_vase'], (5.9, 2.1)),
            SpriteObject(self.sprite_parameters['npc_orc'], (7, 4), 0.01, 10, 1),
            SpriteObject(self.sprite_parameters['npc_skeleton'], (7.68, 1.47), 0.005, 2, 2),
            SpriteObject(self.sprite_parameters['npc_skeleton'], (8.75, 3.65), 0.005, 2, 2),
            SpriteObject(self.sprite_parameters['npc_skeleton'], (1.27, 11.5), 0.005, 2, 2),
            SpriteObject(self.sprite_parameters['npc_skeleton'], (1.26, 8.29), 0.005, 2, 2),
            SpriteObject(self.sprite_parameters['ogr_trader'], (20.27, 12.43), dialog_list=[
                'T Hello. My want bones. You - bones, Me - reward.',
                'Q Ok ?',
                'T Good luck !',
                'R--(10, bone)--(1, bow)--Take it pleas. Thanks for help !',
                'D'
            ])
        ]

    @property
    def sprite_shot(self):
        return min([obj.is_on_fire for obj in self.list_of_objects], default=(float('inf'), 0))


    def clearing(self, player, world_map, inventory):
        if len(self.list_of_objects) > 7:
            for i in self.list_of_objects:
                if i.flag == 'drop':
                    if i.distance_to_sprite <= 28:
                        inventory.additem(i.name)
                        del self.list_of_objects[self.list_of_objects.index(i)]
                if i.is_dead and i.is_dead != 'immortal' and i.time_dead >= 100:
                    for j in i.drop.keys():
                        x = random.randint(1, 100)
                        if x < j:
                            self.list_of_objects.append(
                                SpriteObject(Item(i.drop[j]).item, (i.x / TILE, i.y / TILE), name=i.drop[j])
                            )
                            self.list_of_objects[-1].object_locate(player)
                    del self.list_of_objects[self.list_of_objects.index(i)]
                    chance = random.randint(1, 100)
                    x, y = random.randint(1, 33), random.randint(1, 21)
                    while (x, y) in world_map.keys():
                        x, y = random.randint(1, 33), random.randint(1, 21)
                    if chance > 10:
                        a, b = x - 13, y - 12
                        if a >= 0 and b < 0:#forest
                            self.spawn('npc_bee', (x, y), 0.007, 4, 1)
                        elif a < 0 and b < 0:#mineshaft
                            self.spawn('npc_skeleton', (x, y), 0.005, 2, 2)
                        elif a < 0 and b >= 0:#dragon's dungenon
                            self.spawn('npc_skeleton', (x, y), 0.005, 2, 2)
                        elif a >= 0 and b >= 0:#city
                            self.spawn('npc_chiken', (x, y), 0, 3, -1)
                    else:
                        self.spawn('npc_irongolem', (x, y), 0.02, 60, 0.5, '', True)
                    self.list_of_objects[-1].object_locate(player)
                elif i.is_dead != 'immortal' and i.is_dead:
                    i.time_dead += 1

    def spawn(self, type, pos, dmg, health, speed, name='', shooting=False):
        self.list_of_objects.append(SpriteObject(self.sprite_parameters[type], pos, dmg, health, speed, name, shooting))




class SpriteObject:
    def __init__(self, parameters, pos, damag=0, health=0, speed=0, name='', shooting=False, distance=170, dialog_list=[]):
        self.shooting = shooting
        self.dialog_list = dialog_list
        self.name = name
        self.speed = speed
        self.damag = damag
        self.health = health
        self.object = parameters['sprite'].copy()
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        self.time_dead = 0
        self.distance = distance
        # ---------------------
        self.drop = parameters['drop'].copy()
        self.death_animation = parameters['death_animation'].copy()
        self.is_dead = parameters['is_dead']
        self.dead_shift = parameters['dead_shift']
        # ---------------------
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.flag = parameters['flag']
        self.obj_action = parameters['obj_action'].copy()
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.side = parameters['side']
        self.dead_animation_count = 0
        self.animation_count = 0
        self.npc_action_trigger = False
        self.door_open_trigger = False
        self.door_prev_pos = self.y if self.flag == 'door_h' else self.x
        self.delete = False
        self.reload = 0
        if self.viewing_angles:
            if len(self.object) == 8:
                self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                                     [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
            else:
                self.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def damag(self):
        return self.damag

    @property
    def is_on_fire(self):
        if CENTER_RAY - self.side // 2 < self.current_ray < CENTER_RAY + self.side // 2 and self.blocked:
            return self.distance_to_sprite, self.proj_height
        return float('inf'), None

    @property
    def pos(self):
        return self.x - self.side // 2, self.y - self.side // 2

    def object_locate(self, player):

        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI
        self.theta -= 1.4 * gamma

        delta_rays = int(gamma / DELTA_ANGLE)
        self.current_ray = CENTER_RAY + delta_rays
        if self.flag not in {'door_h', 'door_v'}:
            self.distance_to_sprite *= math.cos(HALF_FOV - self.current_ray * DELTA_ANGLE)

        fake_ray = self.current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and self.distance_to_sprite > 30:
            self.proj_height = min(int(PROJ_COEFF / self.distance_to_sprite),
                                   DOUBLE_HEIGHT if self.flag not in {'door_h', 'door_v'} else HEIGHT)
            sprite_width = int(self.proj_height * self.scale[0])
            sprite_height = int(self.proj_height * self.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift

            # logic for doors, npc, decor
            if self.is_dead and self.is_dead != 'immortal':
                sprite_object = self.dead_animation()
                shift = half_sprite_height * self.dead_shift
                sprite_height = int(sprite_height / 1.3)
            elif self.npc_action_trigger:
                sprite_object = self.npc_in_action()
            else:
                self.object = self.visible_sprite()
                sprite_object = self.sprite_animation()


            # sprite scale and pos
            sprite_pos = (self.current_ray * SCALE - half_sprite_width, HALF_HEIGHT - half_sprite_height + shift)
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))
            return (self.distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

    def sprite_animation(self):
        if self.animation and self.distance_to_sprite < self.animation_dist:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count += 1
            else:
                self.animation.rotate()
                self.animation_count = 0
            return sprite_object
        return self.object

    def visible_sprite(self):
        if self.viewing_angles:
            if self.theta < 0:
                self.theta += DOUBLE_PI
            self.theta = 360 - int(math.degrees(self.theta))

            for angles in self.sprite_angles:
                if self.theta in angles:
                    return self.sprite_positions[angles]
        return self.object

    def dead_animation(self):
        if len(self.death_animation):
            if self.dead_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.dead_animation_count += 1
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.dead_animation_count = 0
        return self.dead_sprite

    def is_dead(self):
        return self.is_dead()

    def npc_shoot(self, list_of_objects, player):
        self.reload -= 1
        if self.shooting and self.reload <= 0:
            list_of_objects.append(SpriteObject({
                'sprite': pygame.image.load(f'sprites/bulletmagic/base/0.png').convert_alpha(),
                'viewing_angles': False,
                'shift': 0.2,
                'scale': (0.4, 0.4),
                'side': 30,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0.8,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': False,
                'flag': 'bullet',
                'obj_action': deque([pygame.image.load(f'sprites/bulletmagic/anim/{i}.png')
                                    .convert_alpha() for i in range(5)]),
                'drop': {}
            }, (self.x / TILE, self.y / TILE), damag=0.1, speed=6, distance=230))
            list_of_objects[-1].object_locate(player)
            self.reload = 300

    def npc_in_action(self):
        sprite_object = self.obj_action[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.obj_action.rotate()
            self.animation_count = 0
        return sprite_object