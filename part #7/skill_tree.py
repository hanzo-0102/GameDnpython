import pygame
import copy
import os
import sys
from collections import deque
from settings import *


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


class SkillTree:
    def __init__(self, skills, need, effect, learned):
        self.skills = skills
        self.skillpoints = 0
        self.effect = effect
        self.learned = learned
        self.need = need
        self.cellsize = 40
        self.width = 5
        self.height = 5
        self.left = 50
        self.top = 120

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def get_cell(self, pos):
        cell = ((pos[0] - self.left) / self.cellsize, (pos[1] - self.top) / self.cellsize)
        if cell[0] < 0 or cell[0] > self.width or cell[1] < 0 or cell[1] > self.height:
            return None
        else:
            return (int(cell[0]), int(cell[1]))

    def render(self, screen, level):
        for y in range(self.height):
            for x in range(self.width):
                if self.skills[x][y] in self.learned:
                    screen.blit(pygame.image.load(f"sprites/skill_tree/learned/{self.skills[x][y]}.png"),
                                (self.left + (x * self.cellsize), self.top + (y * self.cellsize)))
                else:
                    screen.blit(pygame.image.load(f"sprites/skill_tree/notlearned/{self.skills[x][y]}.png"),
                                (self.left + (x * self.cellsize), self.top + (y * self.cellsize)))
        font = pygame.font.SysFont('Arial', 18, bold=True)
        text = font.render(f"YOUR LEVEL IS {level}", 0, SKYBLUE)
        screen.blit(text, (13, 13))
        text = font.render(f"YOU HAVE {self.skillpoints} SKILLPOINT{'S' if self.skillpoints != 1 else ''}", 0, SKYBLUE)
        screen.blit(text, (13, 36))


    def on_click(self, cell):
        if self.skillpoints >= self.need[cell[0]][cell[1]] and (cell[1] == 0 or self.skills[cell[0]][cell[1] - 1] in self.learned):
            self.learned.append(self.skills[cell[0]][cell[1]])
            self.skillpoints -= self.need[cell[0]][cell[1]]