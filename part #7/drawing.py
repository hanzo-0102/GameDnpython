import pygame
from settings import *
from ray_casting import ray_casting
from map import mini_map
from collections import deque
from random import  randrange
import sys

class Drawing:
    def __init__(self, sc, sc_map, player, clock, sc_gui):
        self.sc = sc
        self.sc_map = sc_map
        self.sc_gui = sc_gui
        self.player = player
        self.clock = clock
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.font_win = pygame.font.Font('font/font.ttf', 144)
        self.textures = {1: pygame.image.load('img/wall3.png').convert(),
                         2: pygame.image.load('img/wall4.png').convert(),
                         3: pygame.image.load('img/wall5.png').convert(),
                         4: pygame.image.load('img/wall6.png').convert(),
                         5: pygame.image.load('img/wall7.png').convert(),
                         6: pygame.image.load('img/wall8.png').convert(),
                         7: pygame.image.load('img/wall9.png').convert(),
                         8: pygame.image.load('img/wall10.png').convert(),
                         9: pygame.image.load('img/wall11.png').convert(),
                         10: pygame.image.load('img/wall12.png').convert(),
                         11: pygame.image.load('img/wall13.png').convert(),
                         'S': pygame.image.load('img/sky2.png').convert()
                         }
        # menu
        self.menu_trigger = True
        self.menu_picture = pygame.image.load('img/bg.jpg').convert()
        #endmenu
        self.endmenu_trigger = True
        self.endmenu_picture = pygame.image.load('img/bgfinal.jpg').convert()
        # weapon parameters
        self.weaponi = self.player.weaponi
        self.weapon_base_sprite = pygame.image.load(f'sprites/weapons/{self.weaponi}/base/0.png')
        self.weapon_shot_animation = [pygame.image.load(f'sprites/weapons/{self.weaponi}/shot/{i}.png').convert_alpha()
                                            for i in range(7)]
        self.weapon_rect = self.weapon_base_sprite.get_rect()
        self.weapon_pos = (WIDTH - 375 - self.weapon_rect.width // 2, HEIGHT - self.weapon_rect.height)
        self.shot_length = len(self.weapon_shot_animation)
        self.shot_length_count = 0
        self.shot_animation_speed = 2
        self.shot_animation_count = 0
        self.shot_animation_trigger = True
        self.shot_sound = pygame.mixer.Sound(f'sound/{self.weaponi}.mp3')
        # sfx parameters
        self.sfx = deque([pygame.image.load(f'sprites/weapons/sfx/{i}.png').convert_alpha() for i in range(9)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)

    def background(self, angle):
        sky_offset = -10 * math.degrees(angle) % WIDTH
        self.sc.blit(self.textures['S'], (sky_offset, 0))
        self.sc.blit(self.textures['S'], (sky_offset - WIDTH, 0))
        self.sc.blit(self.textures['S'], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.sc.blit(object, object_pos)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, WHITE)
        self.sc.blit(render, FPS_POS)

    def mini_map(self, player, sprites):
        self.sc_map.fill(BLACK)
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pygame.draw.line(self.sc_map, YELLOW, (map_x, map_y), (map_x + 6 * math.cos(player.angle),
                                                 map_y + 6 * math.sin(player.angle)), 1)
        pygame.draw.circle(self.sc_map, RED, (int(map_x), int(map_y)), 2.5)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, DARKBROWN, (x, y, MAP_TILE, MAP_TILE))
        for i in sprites.list_of_objects:
            if (i.flag == 'npc' or i.flag == 'human' or i.flag == 'horse0') and i.is_dead != 'immortal':
                x, y = i.pos
                pygame.draw.circle(self.sc_map, WHITE, (x // MAP_SCALE, y // MAP_SCALE), 1.5)
            elif i.flag == 'trader':
                x, y = i.pos
                pygame.draw.circle(self.sc_map, SKYBLUE, (x // MAP_SCALE, y // MAP_SCALE), 1.5)
            elif i.flag == 'dragon_old' or i.flag == 'dragon_baby' or i.flag == 'dragon_young':
                x, y = i.pos
                pygame.draw.circle(self.sc_map, RED, (x // MAP_SCALE, y // MAP_SCALE), 1.5)
            elif i.flag == 'horse1':
                x, y = i.pos
                pygame.draw.circle(self.sc_map, PURPLE, (x // MAP_SCALE, y // MAP_SCALE), 1.5)
            elif i.flag == 'drop':
                x, y = i.pos
                pygame.draw.circle(self.sc_map, SANDY, (x // MAP_SCALE, y // MAP_SCALE), 1.5)
        self.sc.blit(self.sc_map, MAP_POS)

    def gui(self, player):
        self.sc_gui.fill(BLACK)
        pygame.draw.rect(self.sc_gui, WHITE, (5, 5, 400, 40))
        pygame.draw.rect(self.sc_gui, GREEN, (5, 5, 400 * (player.hp / player.max_hp), 20))
        pygame.draw.rect(self.sc_gui, SKYBLUE, (5, 25, 400 * (player.mana / player.max_mana), 20))
        self.sc.blit(self.sc_gui, (30, 740))

    def player_weapon(self, shots):
        if self.player.shot:
            if not self.shot_length_count:
                self.shot_sound.play()
            self.shot_projection = min(shots)[1] // 2
            if self.weaponi not in ['woodensword', 'crashedironsword', 'ironsword', 'ironspear']:
                self.bullet_sfx()
            shot_sprite = self.weapon_shot_animation[self.shot_length_count]
            self.sc.blit(shot_sprite, self.weapon_pos)
            self.shot_animation_count += 1
            if self.shot_animation_count == self.shot_animation_speed:
                self.shot_animation_count = 0
                self.shot_length_count += 1
                self.shot_animation_trigger = False
            if self.shot_length_count == self.shot_length:
                self.player.shot = False
                self.shot_length_count = 0
                self.sfx_length_count = 0
                self.shot_animation_trigger = True
        else:
            self.sc.blit(self.weapon_base_sprite, self.weapon_pos)

    def bullet_sfx(self):
        if self.sfx_length_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.sc.blit(sfx, (HALF_WIDTH - sfx_rect.w // 2, HALF_HEIGHT - sfx_rect.h // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)

    def menu(self):
        x = 0
        button_font = pygame.font.Font('font/font.ttf', 72)
        label_font = pygame.font.Font('font/font1.otf', 300)
        start = button_font.render('START', 1, pygame.Color('black'))
        button_start = pygame.Rect(0, 0, 400, 150)
        button_start.center = HALF_WIDTH, HALF_HEIGHT
        exit = button_font.render('EXIT', 1, pygame.Color('black'))
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200
        step = 1

        while self.menu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.sc.blit(self.menu_picture, (0, 0), (x, HALF_HEIGHT, WIDTH, HEIGHT))
            x += step
            if x == 0:
                step = 1
            elif x == WIDTH:
                step = -1

            pygame.draw.rect(self.sc, BLACK, button_start, border_radius=25, width=10)
            self.sc.blit(start, (button_start.centerx - 130, button_start.centery - 70))

            pygame.draw.rect(self.sc, BLACK, button_exit, border_radius=25, width=10)
            self.sc.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))

            label = label_font.render('DNPython', 1, (15, 70, 50))
            self.sc.blit(label, (15, -30))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_start.collidepoint(mouse_pos):
                pygame.draw.rect(self.sc, WHITE, button_start, border_radius=25)
                self.sc.blit(start, (button_start.centerx - 130, button_start.centery - 70))
                if mouse_click[0]:
                    self.menu_trigger = False
            elif button_exit.collidepoint(mouse_pos):
                pygame.draw.rect(self.sc, WHITE, button_exit, border_radius=25)
                self.sc.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(20)


    def end(self, loseorwin, seconds):
        button_font = pygame.font.Font('font/font.ttf', 72)
        label_font = pygame.font.Font('font/font1.otf', 300)
        label_font_smaller = pygame.font.Font('font/font1.otf', 90)
        exit = button_font.render('EXIT', 1, pygame.Color('black'))
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = HALF_WIDTH, HALF_HEIGHT + 300
        step = 1

        while self.endmenu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.sc.blit(self.endmenu_picture, (0, 0), (0, 0, WIDTH, HEIGHT))

            pygame.draw.rect(self.sc, BLACK, button_exit, border_radius=25, width=10)
            self.sc.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))

            label = label_font.render(f'YOU {loseorwin}', 1, (15, 70, 50))
            self.sc.blit(label, (15, -30))
            label = label_font_smaller.render(f'It takes {seconds} seconds', 1, (15, 70, 50))
            self.sc.blit(label, (215, 170))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_exit.collidepoint(mouse_pos):
                pygame.draw.rect(self.sc, WHITE, button_exit, border_radius=25)
                self.sc.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(20)