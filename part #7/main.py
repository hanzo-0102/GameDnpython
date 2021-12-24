import pygame

from player import Player
from sprite_objects import *
from ray_casting import ray_casting_walls
from drawing import Drawing
from interaction import Interaction
from map import world_map

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface(MINIMAP_RES)
sc_gui = pygame.Surface((410, 30))

sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc, sc_map, player, clock, sc_gui)
interaction = Interaction(player, sprites, drawing)
drawing.menu()
pygame.mouse.set_visible(False)
interaction.play_music()

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

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()