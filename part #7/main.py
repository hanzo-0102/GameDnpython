import pygame

from player import Player
from sprite_objects import *
from ray_casting import ray_casting_walls
from drawing import Drawing
from interaction import Interaction
from map import world_map
from inventory_test import Inventory

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface(MINIMAP_RES)
sc_gui = pygame.Surface((410, 30))

sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc, sc_map, player, clock, sc_gui)
interaction = Interaction(player, sprites, drawing)
inventory = Inventory(10, 10, 10, 300, 36, player, sprites)
mode = 'game'
drawing.menu()
pygame.mouse.set_visible(False)
interaction.play_music()
waiting = 0
while True:
    pygame.mixer.music.set_volume(VOLUME / 100)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        drawing.curwep = 0
        player.curwep = 0
        player.weapon = player.weapons[player.curwep]
    elif keys[pygame.K_2]:
        drawing.curwep = 1
        player.curwep = 1
        player.weapon = player.weapons[player.curwep]
    if keys[pygame.K_e] and waiting == 0:
        mode = 'inventory' if mode == 'game' else 'game'
        waiting = 100
    elif waiting > 1:
        waiting -= 1
    elif keys[pygame.K_e] and waiting == 1:
        waiting -= 1
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
                if (abs(i.pos[0] - player.x) + abs(i.pos[1] - player.y) < 170):
                    player.dmg(i.damag)

        sprites.clearing(player, world_map)
        interaction.interaction_objects()
        interaction.npc_action()
        interaction.clear_world()
    elif mode == 'inventory':
        pygame.mouse.set_visible(True)
        sc.blit(pygame.image.load('img/inventory.jpg'), (0, 0))
        inventory.render(sc)
        inventory.draw(sc)
        sprites.list_of_objects = inventory.sprites.list_of_objects


    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()