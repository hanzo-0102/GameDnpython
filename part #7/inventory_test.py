import pygame
import copy
import os
import sys
from collections import deque
from settings import *


items_rare = {
    'bone':'common',
    'woodensword':'common',
    'magicwand':'common',
    'golemgun':'legendary',
    'bow':'uncommon',
    'healshroom':'uncommon',
    'manashroom':'uncommon',
    'chiken':'uncommon',
    'carrot':'common',
    'cabage':'common',
    'crashedironsword':'uncommon',
    'ironsword':'epic',
    'ironspear':'legendary',
    'bottle':'common',
    'waterbottle':'common'
}


def load_image(name, colorkey=None):
    fullname = os.path.join('Icons', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением'{fullname}' не найден")
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
            self.dropitem(item)

    def dropitem(self, item):
        from sprite_objects import SpriteObject
        x = Item(item).item
        self.sprites.list_of_objects.append(SpriteObject(x, (self.player.x // TILE + 0.6, self.player.y // TILE - 0.6), name=item))


    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, mouse_pos)

    def get_cell(self, pos, need=False):
        cell = ((pos[0] - self.left) / self.cellsize, (pos[1] - self.top) / self.cellsize)
        if need:
            return (int(cell[0]), int(cell[1]))
        elif cell[0] < 0 or cell[0] > self.width or cell[1] < 0 or cell[1] > self.height:
            return None
        else:
            return (int(cell[0]), int(cell[1]))

    def render(self, screen, quests, level, xp):
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
        pygame.draw.rect(screen, DARKGRAY, (10, 10, 300, HEIGHT - 30))
        font = pygame.font.SysFont('Arial', 12, bold=True)
        text = font.render('QUESTS', 0, WHITE)
        screen.blit(text, (134, 12))
        coutni = 0
        for j in quests:
            text = font.render(f"Need {j[0]} {j[1]}{'s' if j[0] > 1 else ''} | Award : {j[2]} {j[3]}{'s' if j[2] > 1 else ''}", 0, WHITE)
            screen.blit(text, (12, 12 + (13 * (coutni + 1))))
            coutni += 1
        font = pygame.font.SysFont('Arial', 12, bold=True)
        text = font.render(f'YOUR LEVEL IS {level}', 0, BLACK)
        screen.blit(text, (HALF_WIDTH + 30, 24))
        font = pygame.font.SysFont('Arial', 12, bold=True)
        text = font.render(f'XP: {xp}/{level * 10}', 0, BLACK)
        screen.blit(text, (HALF_WIDTH + 30, 48))

    def render_trade(self, screen, trades):
        for y in range(self.height):
            for x in range(self.width):
                screen.blit(pygame.image.load("sprites/inventory/emptyslot.png"),
                            (self.left + (x * self.cellsize), self.top + (y * self.cellsize)))
                if self.invent[x][y]:
                    screen.blit(pygame.image.load(f"sprites/inventory/{self.invent[x][y]}icon.png"),
                                (self.left + 2 + (x * self.cellsize), self.top + 2 + (y * self.cellsize)))


    def on_click(self, cell, pos):
        if self.moving == False and cell and cell != (13, 5) and cell != (13, 6):
            self.dx = cell[0] * self.cellsize + self.left - pos[0]
            self.dy = cell[1] * self.cellsize + self.top - pos[1]
            self.moving = self.invent[cell[0]][cell[1]]
            self.invent[cell[0]][cell[1]] = False
        else:
            try:
                x, y = self.get_cell(pos, True)
                if (x, y) != (13, 5) and (x, y) != (13, 6):
                    if self.invent[x][y]:
                        self.invent[x][y], self.moving = self.moving, self.invent[x][y]
                    else:
                        self.invent[x][y] = self.moving
                        self.moving = False
                elif (x, y) == (13, 5) and self.moving in ['woodensword', 'magicwand', 'golemgun', 'bow',
                                                           'crashedironsword', 'ironsword', 'ironspear']:
                    self.melee, self.moving = self.moving, self.melee
                elif (x, y) == (13, 6) and self.moving in ['woodensword', 'magicwand', 'golemgun', 'bow',
                                                           'crashedironsword', 'ironsword', 'ironspear']:
                    self.range, self.moving = self.moving, self.range
            except Exception:
                if self.moving:
                    self.dropitem(self.moving)
                    self.moving = False

    def draw(self, screen):
        if self.moving:
            x, y = pygame.mouse.get_pos()
            screen.blit(pygame.image.load(f"sprites/inventory/{self.moving}icon.png"), (x + self.dx, y + self.dy))