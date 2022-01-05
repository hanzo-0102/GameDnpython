import timeit

import pygame

from player import Player
from sprite_objects import *
from ray_casting import ray_casting_walls
from drawing import Drawing
from interaction import Interaction
from map import world_map
from inventory_test import Inventory, items_rare
from pygame.event import Event
from threading import Timer

indexes = {
    'magicwand': 0,
    'woodensword': 1,
    'golemgun': 2
}

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface(MINIMAP_RES)
sc_gui = pygame.Surface((410, 30))
sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc, sc_map, player, clock, sc_gui)
interaction = Interaction(player, sprites, drawing)
inventory = Inventory(10, 10, 200, 450, 36, player, sprites)
mode = 'game'
drawing.menu()
pygame.mouse.set_visible(False)
interaction.play_music()
font = pygame.font.SysFont('Arial', 12, bold=True)
while True:
    pygame.mixer.music.set_volume(VOLUME / 100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and mode == 'game':
            if event.button == 1 and not player.shot:
                player.shot = True
        elif event.type == pygame.MOUSEBUTTONDOWN and mode == 'inventory':
            if event.button == 1:
                inventory.get_click(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                player.weaponi = inventory.melee
                drawing.curwep = indexes[player.weaponi]
            elif event.key == pygame.K_2:
                player.weaponi = inventory.range
                drawing.curwep = indexes[player.weaponi]
            elif event.key == pygame.K_e:
                pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
                mode = 'inventory' if mode == 'game' else 'game'
    if mode == 'game':
        pygame.mouse.set_visible(False)
        player.movement()
        drawing.background(player.angle)
        walls, wall_shot = ray_casting_walls(player, drawing.textures)
        drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
        drawing.fps(clock)
        drawing.mini_map(player, sprites)
        drawing.gui(player)
        drawing.player_weapon([wall_shot, sprites.sprite_shot])
        for i in sprites.list_of_objects:
            if not(i.is_dead):
                if (abs(i.pos[0] - player.x) + abs(i.pos[1] - player.y) < i.distance):
                    player.dmg(i.damag)
            if i.flag == 'bullet':
                if (abs(i.pos[0] - player.x) + abs(i.pos[1] - player.y) < i.distance):
                    player.dmg(i.damag)
                    del sprites.list_of_objects[sprites.list_of_objects.index(i)]

        sprites.clearing(player, world_map, inventory)
        interaction.interaction_objects()
        interaction.npc_action()
        sprites.list_of_objects = interaction.sprites.list_of_objects
        interaction.clear_world()
        inventory.sprites = sprites
    elif mode == 'inventory':
        pygame.mouse.set_visible(True)
        sc.blit(pygame.image.load('img/inventory.jpg'), (0, 0))
        drawing.fps(clock)
        inventory.render(sc)
        inventory.draw(sc)
        x, y = pygame.mouse.get_pos()
        cell = inventory.get_cell((x, y), True)
        try:
            if cell and cell != (13, 5) and cell != (13, 6) and inventory.invent[cell[0]][cell[1]]:
                widthi = len(f"{inventory.invent[cell[0]][cell[1]].capitalize()}-{items_rare[inventory.invent[cell[0]][cell[1]]]}")
                pygame.draw.rect(sc, DARKGRAY, (x, y, 8 * widthi, 40))
                pygame.draw.rect(sc, DARKGRAY, (x, y, 100, 40))
                text = font.render(f"{inventory.invent[cell[0]][cell[1]].capitalize()}-{items_rare[inventory.invent[cell[0]][cell[1]]]}",
                                   0, WHITE)
                sc.blit(text, (x + 3, y + 13))
            elif cell and cell == (13, 5):
                widthi = len(f"{inventory.melee.capitalize()}-{items_rare[inventory.melee]}")
                pygame.draw.rect(sc, DARKGRAY, (x, y, 8 * widthi, 40))
                text = font.render(
                    f"{inventory.melee.capitalize()}-{items_rare[inventory.melee]}",
                    0, WHITE)
                sc.blit(text, (x + 3, y + 13))
            elif cell and cell == (13, 6):
                widthi = len(f"{inventory.range.capitalize()}-{items_rare[inventory.range]}")
                pygame.draw.rect(sc, DARKGRAY, (x, y, 8 * widthi, 40))
                text = font.render(
                    f"{inventory.range.capitalize()}-{items_rare[inventory.range]}",
                    0, WHITE)
                sc.blit(text, (x + 3, y + 13))
        except Exception:
            pass
        sprites.list_of_objects = inventory.sprites.list_of_objects


    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()