import random
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
from skill_tree import SkillTree

indexes = {
    'magicwand': 0,
    'woodensword': 1,
    'golemgun': 2
}

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface(MINIMAP_RES)
sc_gui = pygame.Surface((410, 50))
sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc, sc_map, player, clock, sc_gui)
interaction = Interaction(player, sprites, drawing)
inventory = Inventory(10, 10, 200, 450, 36, player, sprites)
skilltree = SkillTree([['NatureSheild', 'NatureSheild2', 'NatureSheild3', 'MagicSheild', 'MagicSheild2'],
                       ['FastSteps', 'LikeTornado', 'LikeTornado2', 'Uncatchable', 'SpeedOfTheif'],
                       ['SharpSword', 'IronFist', 'IronFist2', 'KungFu', 'OnePunchMan'],
                       ['YoungStudent', 'GraduateStudent', 'MasterOfWater', 'MasterOfFire', 'MagisterOfMagic'],
                       ['StrongShot', 'StrongShot2', 'StrongShot3', 'StrongShot4', 'GoodEye']],
                      [[1, 2, 2, 3, 3], [1, 2, 2, 3, 4], [1, 2, 2, 3, 4], [1, 2, 3, 3, 4], [1, 1, 2, 3, 4]],
                      [['Decrease incoming damage by 10 %', 'Decrease incoming damage by 20 %', 'Decrease incoming damage by 30 %', 'Decrease incoming damage by 50 %', 'Decrease incoming damage by 70 %'],
                       ['Increase speed by 10 %', 'Increase speed by 25 %', 'Increase speed by 40 %', 'Increase speed by 65 %', 'Increase speed by 100 %'],
                       ['Increase melee damage by 10 %', 'Increase melee damage by 25 %', 'Increase melee damage by 40 %', 'Increase melee damage by 60 %', 'Increase melee damage by 80 %'],
                       ['Decrease mana cost by 10 %', 'Decrease mana cost by 20 %', 'Decrease mana cost by 40 %', 'Decrease mana cost by 60 %', 'Regenerate 2 % mana for tick'],
                       ['Increase range damage by 10 %', 'Increase range damage by 20 %', 'Increase range damage by 40 %', 'Increase range damage by 60 %', 'You wont lose mana if you miss']],
                      [])
mode = 'game'
drawing.menu()
pygame.mouse.set_visible(False)
interaction.play_music()
font = pygame.font.SysFont('Arial', 12, bold=True)
fontBigger = pygame.font.SysFont('Arial', 48, bold=True)
avaliable_dialog = False
num_of_dialog = 0
dialog_list = []
answer = False
take = False
quests = []
was_quests = []
can_miss = True
while True:
    pygame.mixer.music.set_volume(VOLUME / 100)
    interaction.player = player
    if player.hp <= 0:
        break

    if 'NatureSheild' in skilltree.learned:
        player.sheild = 0.9
    if 'NatureSheild2' in skilltree.learned:
        player.sheild = 0.8
    if 'NatureSheild3' in skilltree.learned:
        player.sheild = 0.7
    if 'MagicSheild' in skilltree.learned:
        player.sheild = 0.5
    if 'MagicSheild2' in skilltree.learned:
        player.sheild = 0.3

    if 'FastSteps' in skilltree.learned:
        player.sheild = 1.1
    if 'LikeTornado' in skilltree.learned:
        player.sheild = 1.25
    if 'LikeTornado2' in skilltree.learned:
        player.sheild = 1.4
    if 'Uncatchable' in skilltree.learned:
        player.sheild = 1.65
    if 'SpeedOfTheif' in skilltree.learned:
        player.sheild = 2

    if 'SharpSword' in skilltree.learned:
        player.sheild = 1.1
    if 'IronFist' in skilltree.learned:
        player.sheild = 1.25
    if 'IronFist2' in skilltree.learned:
        player.sheild = 1.4
    if 'KungFu' in skilltree.learned:
        player.sheild = 1.6
    if 'OnePunchMan' in skilltree.learned:
        player.sheild = 1.8

    if 'YoungStudent' in skilltree.learned:
        player.sheild = 0.9
    if 'GraduateStudent' in skilltree.learned:
        player.sheild = 0.8
    if 'MasterOfWater' in skilltree.learned:
        player.sheild = 0.6
    if 'MasterOfFire' in skilltree.learned:
        player.sheild = 0.4
    if 'MagisterOfMagic' in skilltree.learned:
        player.managen = 0.02

    if 'StrongShot' in skilltree.learned:
        player.rangedmg = 1.1
    if 'StrongShot2' in skilltree.learned:
        player.rangedmg = 1.2
    if 'StrongShot3' in skilltree.learned:
        player.rangedmg = 1.4
    if 'StrongShot4' in skilltree.learned:
        player.rangedmg = 1.6
    if 'GoodEye' in skilltree.learned:
        can_miss = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and mode == 'game':
            if event.button == 1 and not player.shot and player.mana >= player.weapon().manacost * player.manacost:
                player.shot = True
                if can_miss or any([obj.is_on_fire[1] for obj in sprites.list_of_objects]):
                    player.mana -= player.weapon().manacost * player.manacost
        elif event.type == pygame.MOUSEBUTTONDOWN and mode == 'skilltree':
            if event.button == 1:
                skilltree.get_click(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONDOWN and mode == 'inventory':
            if event.button == 1:
                inventory.get_click(pygame.mouse.get_pos())
            if event.button == 3:
                cell = inventory.get_cell(pygame.mouse.get_pos())
                if cell:
                    if inventory.invent[cell[0]][cell[1]] == 'manashroom':
                        inventory.invent[cell[0]][cell[1]] = False
                        player.mana = min(player.max_mana, player.mana + 2)
                    elif inventory.invent[cell[0]][cell[1]] == 'healshroom':
                        inventory.invent[cell[0]][cell[1]] = False
                        player.hp = min(player.max_hp, player.hp + 1.2)
                    elif inventory.invent[cell[0]][cell[1]] == 'cabage':
                        inventory.invent[cell[0]][cell[1]] = False
                        player.hp = min(player.max_hp, player.hp + 0.9)
                    elif inventory.invent[cell[0]][cell[1]] == 'carrot':
                        inventory.invent[cell[0]][cell[1]] = False
                        player.hp = min(player.max_hp, player.hp + 0.6)
                    elif inventory.invent[cell[0]][cell[1]] == 'chiken':
                        inventory.invent[cell[0]][cell[1]] = False
                        player.hp = min(player.max_hp, player.hp + 2)
                        player.mana = min(player.max_mana, player.mana + 1)
        elif event.type == pygame.MOUSEBUTTONDOWN and mode == 'dialog':
            if event.button == 1 and dialog_list[num_of_dialog].split()[0] == 'T':
                num_of_dialog += 1
                pygame.mixer.music.load('sound/bell.mp3')
                pygame.mixer.music.play(1)
            elif event.button == 1 and dialog_list[num_of_dialog].split()[0] == 'Q':
                if pygame.mouse.get_pos()[0] > HALF_WIDTH:
                    mode = 'game'
                else:
                    num_of_dialog += 1
                    pygame.mixer.music.load('sound/bell.mp3')
                    pygame.mixer.music.play(1)
            elif event.button == 1 and dialog_list[num_of_dialog].split()[0] == 'R':
                need = dialog_list[num_of_dialog].split('--')[1]
                need = need[1:len(need) - 1].split(', ')
                reward = dialog_list[num_of_dialog].split('--')[2]
                reward = reward[1:len(reward) - 1].split(', ')
                if [int(need[0]), need[1], int(reward[0]), reward[1]] not in quests and [int(need[0]), need[1], int(reward[0]), reward[1]] not in was_quests:
                    num_of_dialog += 1
                    pygame.mixer.music.load('sound/bell.mp3')
                    pygame.mixer.music.play(1)
            elif event.button == 1 and dialog_list[num_of_dialog].split()[0] == 'D':
                pygame.mixer.music.load('sound/bell.mp3')
                pygame.mixer.music.play(1)
                mode = 'game'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                player.weaponi = inventory.melee
                drawing.weaponi = player.weaponi
                drawing.weapon_base_sprite = pygame.image.load(f'sprites/weapons/{drawing.weaponi}/base/0.png')
                drawing.weapon_shot_animation = [
                    pygame.image.load(f'sprites/weapons/{drawing.weaponi}/shot/{i}.png').convert_alpha()
                    for i in range(7)]
                drawing.shot_sound = pygame.mixer.Sound(f'sound/{drawing.weaponi}.mp3')
            elif event.key == pygame.K_2:
                player.weaponi = inventory.range
                drawing.weaponi = player.weaponi
                drawing.weapon_base_sprite = pygame.image.load(f'sprites/weapons/{drawing.weaponi}/base/0.png')
                drawing.weapon_shot_animation = [
                    pygame.image.load(f'sprites/weapons/{drawing.weaponi}/shot/{i}.png').convert_alpha()
                    for i in range(7)]
                drawing.shot_sound = pygame.mixer.Sound(f'sound/{drawing.weaponi}.mp3')
            elif event.key == pygame.K_e:
                pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
                mode = 'inventory' if mode == 'game' else 'game'
            elif event.key == pygame.K_TAB:
                pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
                mode = 'skilltree' if mode == 'game' else 'game'
            elif event.key == pygame.K_f and avaliable_dialog:
                mode = 'dialog'
                num_of_dialog = 0
            elif event.key == pygame.K_f:
                take = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                take = False
    if mode == 'game':
        pygame.mouse.set_visible(False)
        player.mana = min(player.max_mana, player.mana + (player.mana * player.managen))
        player.movement()
        player.level_up()
        skilltree.skillpoints = player.skillpoints
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
                    player.dmg(i.damag * player.sheild)
            if i.flag == 'bullet':
                if (abs(i.pos[0] - player.x) + abs(i.pos[1] - player.y) < i.distance):
                    player.dmg(i.damag)
                    del sprites.list_of_objects[sprites.list_of_objects.index(i)]
            if i.flag == 'trader' and (abs(i.pos[0] - player.x) + abs(i.pos[1] - player.y) < 120):
                render = fontBigger.render('press [F] to interract', 0, DARKORANGE)
                avaliable_dialog = i.pos
                dialog_list = i.dialog_list
                sc.blit(render, (HALF_WIDTH - 220, HALF_HEIGHT + 80))
            elif i.flag == 'trader' and (abs(i.pos[0] - player.x) + abs(i.pos[1] - player.y) >= 120) and avaliable_dialog == i.pos:
                avaliable_dialog = False
            if i.flag == 'farmland' and i.stage == 3 and (abs(i.pos[0] - player.x) + abs(i.pos[1] - player.y) < 120):
                if not(take):
                    render = fontBigger.render('press [F] to interract', 0, DARKORANGE)
                    sc.blit(render, (HALF_WIDTH - 220, HALF_HEIGHT + 80))
                else:
                    take = False
                    inventory.additem(i.item)
                    i.stage = 1
                    i.object = pygame.image.load(f'sprites/{i.item}/base/{i.stage - 1}.png').convert_alpha()
                    i.time_to_grow = random.randint(1000, 10000)
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
        inventory.render(sc, quests, player.lvl, player.xp)
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
    elif mode == 'skilltree':
        pygame.mouse.set_visible(True)
        player.skillpoints = skilltree.skillpoints
        sc.blit(pygame.image.load('img/skilltree.png'), (0, 0))
        drawing.fps(clock)
        skilltree.render(sc, player.lvl)
        x, y = pygame.mouse.get_pos()
        cell = skilltree.get_cell((x, y))
        if cell:
            try:
                pygame.draw.rect(sc, DARKGRAY, (x, y, 260, 40))
                text = font.render(f"{skilltree.skills[cell[0]][cell[1]]} Cost: {skilltree.need[cell[0]][cell[1]]}",
                                   0, WHITE)
                sc.blit(text, (x + 3, y + 13))
                text = font.render(f"EFFECT : {skilltree.effect[cell[0]][cell[1]]}",
                                   0, WHITE)
                sc.blit(text, (x + 3, y + 26))
            except Exception:
                pass
    elif mode == 'dialog':
        pygame.mouse.set_visible(True)
        drawing.background(player.angle)
        walls, wall_shot = ray_casting_walls(player, drawing.textures)
        drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
        drawing.fps(clock)
        pygame.draw.rect(sc, DARKGRAY, (0, HALF_HEIGHT + 60, WIDTH, HALF_HEIGHT - 60))
        if dialog_list[num_of_dialog].split()[0] == 'T':
            text = fontBigger.render(dialog_list[num_of_dialog][2:], 0, WHITE)
            sc.blit(text, (3, HALF_HEIGHT + 63))
        elif dialog_list[num_of_dialog].split()[0] == 'Q':
            text = fontBigger.render(dialog_list[num_of_dialog][2:], 0, WHITE)
            sc.blit(text, (3, HALF_HEIGHT + 63))
            text = fontBigger.render('YES', 0, WHITE)
            sc.blit(text, (30, HEIGHT - 60))
            text = fontBigger.render('NO', 0, WHITE)
            sc.blit(text, (HALF_WIDTH + 30, HEIGHT - 60))
        elif dialog_list[num_of_dialog].split('--')[0] == 'R':
            need = dialog_list[num_of_dialog].split('--')[1]
            need = need[1:len(need) - 1].split(', ')
            reward = dialog_list[num_of_dialog].split('--')[2]
            reward = reward[1:len(reward) - 1].split(', ')
            counti = 0
            needcounti = int(need[0])
            for i in inventory.invent:
                for j in i:
                    if j == need[1]:
                        counti += 1
            if needcounti <= counti:
                for i in range(len(inventory.invent)):
                    for j in range(len(inventory.invent[0])):
                        if inventory.invent[i][j] == need[1] and needcounti != 0:
                            inventory.invent[i][j] = False
                            needcounti -= 1
                for i in range(int(reward[0])):
                    inventory.additem(reward[1])
                text = fontBigger.render(dialog_list[num_of_dialog].split()[3], 0, WHITE)
                sc.blit(text, (3, HALF_HEIGHT + 63))
            else:
                if [int(need[0]), need[1], int(reward[0]), reward[1]] not in quests and [int(need[0]), need[1], int(reward[0]), reward[1]] not in was_quests:
                    quests.append([int(need[0]), need[1], int(reward[0]), reward[1]])
                mode = 'game'

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()