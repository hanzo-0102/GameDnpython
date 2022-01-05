import pygame
import copy
import os
import sys
from collections import deque


items_rare = {
    'bone':'common',
    'woodensword':'common',
    'magicwand':'common'
}


def load_image(name, colorkey=None):
    fullname = os.path.join('Icons', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Item:
    def __init__(self, name):
        self.item = {
                'sprite': pygame.image.load(f'sprites/items/{name}.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.8,
                'scale': (0.5, 0.5),
                'side': 30,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': False,
                'flag': 'drop',
                'obj_action': [],
                'drop': {}
            }


class Inventory:
    def __init__(self, width, height, top, left, cellsize, player, sprites):
        self.player = player
        self.sprites = sprites
        self.width = width
        self.height = height
        self.moving = False
        self.invent = [[False for i in range(width)] for j in range(height)]
        self.top = top
        self.left = left
        self.cellsize = cellsize
        self.melee = 'woodensword'
        self.range = 'magicwand'

    def additem(self, item):
        for x in range(self.width):
            for y in range(self.height):
                if not(self.invent[y][x]):
                    self.invent[y][x] = item
                    return 0
        if all([all(i) for i in self.invent]):
            self.dropitem(item, self.sprites, self.player)

    def dropitem(self, item):
        x = {'sprite': pygame.image.load(f'sprites/items/base/{item}.png').convert_alpha(),
                'viewing_angles': False,
                'shift': 0.8,
                'scale': (0.8, 0.8),
                'side': 30,
                'animation': [],
                'death_animation': deque([]),
                'is_dead': 'immortal',
                'dead_shift': 0.8,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'flag': 'decor',
                'obj_action': deque([])}
        self.sprites.list_of_objects.append(x, self.player.pos)


    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, mouse_pos)

    def get_cell(self, pos):
        cell = ((pos[0] - self.left) / self.cellsize, (pos[1] - self.top) / self.cellsize)
        if int(cell[0]) == 13 and int(cell[1]) in range(5, 7):
            return (int(cell[0]), int(cell[1]))
        elif cell[0] < 0 or cell[0] > self.width or cell[1] < 0 or cell[1] > self.height:
            return None
        else:
            return (int(cell[0]), int(cell[1]))

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                screen.blit(pygame.image.load("sprites/inventory/emptyslot.png"),
                            (self.left + (x * self.cellsize), self.top + (y * self.cellsize)))
                if self.invent[x][y]:
                    screen.blit(pygame.image.load(f"sprites/inventory/{self.invent[x][y]}icon.png"),
                                (self.left + 2 + (x * self.cellsize), self.top + 2 + (y * self.cellsize)))
        screen.blit(pygame.image.load("sprites/inventory/emptyslot.png"),
                    (self.left + ((self.width + 3) * self.cellsize), self.top + (self.height // 2 * self.cellsize)))
        screen.blit(pygame.image.load("sprites/inventory/emptyslot.png"),
                    (self.left + ((self.width + 3) * self.cellsize), self.top + ((self.height // 2 + 1) * self.cellsize)))
        screen.blit(pygame.image.load(f"sprites/inventory/{self.melee}icon.png"),
                    (self.left + 2 + ((self.width + 3) * self.cellsize), self.top + 2 + (self.height // 2 * self.cellsize)))
        screen.blit(pygame.image.load(f"sprites/inventory/{self.range}icon.png"),
                    (self.left + 2 + ((self.width + 3) * self.cellsize), self.top + 2 + ((self.height // 2 + 1) * self.cellsize)))


    def on_click(self, cell, pos):
        if self.moving == False:
            self.dx = cell[0] * self.cellsize + self.left - pos[0]
            self.dy = cell[1] * self.cellsize + self.top - pos[1]
            self.invent[cell[0]][cell[1]] = False
        else:
            x, y = self.get_cell(pos)
            if self.invent[x][y]:
                self.dropitem(self.moving)
            else:
                self.invent[x][y] = self.moving
            self.moving = False

    def draw(self, screen):
        if self.moving:
            x, y = pygame.mouse.get_pos()
            screen.blit(pygame.image.load(f"sprites/items/{self.moving}.png"), (x + self.dx, y + self.dy))