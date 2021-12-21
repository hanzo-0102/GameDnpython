import pygame
import copy
import os
import sys


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


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0 for i in range(width)] for j in range(height)]

        self.left = 40
        self.top = 40
        self.cell_size = 30

    def view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, (0, 0, 0),
                                 (self.cell_size * x + self.left,
                                 self.cell_size * y + self.top,
                                 self.cell_size, self.cell_size))
                pygame.draw.rect(screen, (255, 255, 255),
                                 (self.cell_size * x + self.left,
                                  self.cell_size * y + self.top,
                                  self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if not(self.left <= x <= self.left + self.width * self.cell_size) or \
                not(self.top <= y <= self.top + self.height * self.cell_size):
            return None
        x -= self.left
        y -= self.top
        return x // self.cell_size, y // self.cell_size

    def on_click(self, cell):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


class Icon(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.image_name = kwargs["image"]
        self.image = load_image(kwargs["image"])
        self.rect = self.image.get_rect()
        self.type = kwargs["type"]

    def up(self, pos, inv):
        x, y = pos
        if self.rect.y <= y <= self.rect.y + self.rect.height and \
                self.rect.x <= x <= self.rect.width + self.rect.x:
            inv.current_image = self
            inv.render(screen)
            print(f"Вы перешли во вкладку {self.type}")


pygame.init()
size = width, height = 1250, 650
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()

icon_swords = Icon(image="Sword_table_icon.jpg", type="swords")

icon_potions = Icon(image="Potions_table_icon.jpg", type="potions")


class Item:
    def __init__(self, image, type_of_item, parametres, price=0, name="unnamed"):
        self.image = load_image(image, colorkey=-1)
        self.name = name
        self.image_name = image
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.sprite.rect = self.sprite.image.get_rect()
        self.parametres = parametres
        self.type_item = type_of_item
        self.price = price


ex = None


class Inventory(Board):
    def __init__(self, width, height, icons):
        super().__init__(width, height)
        self.icons = [Icon(image=i.image_name, type=i.type) for i in icons]
        self.current_image = self.icons[0]
        self.inv_collection = [[None for i in range(width)] for j in range(height)]

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)
        for i in self.icons:
            i.up(mouse_pos, self)

    def take_item(self, item):
        for i in range(self.height):
            for j in range(self.width):
                if self.inv_collection[i][j] is None:
                    self.inv_collection[i][j] = Item(image=item.image_name,
                                                     type_of_item=item.type_item,
                                                     price=item.price, parametres=item.parametres)
                    self.render(screen)
                    return

    def render(self, screen):
        super().render(screen)
        for i in range(len(self.icons)):
            all_sprites.add(self.icons[i])
            self.icons[i].rect.x = self.left - 30
            if i > 0:
                self.icons[i].rect.x = self.icons[i - 1].rect.x + self.icons[i - 1].rect.width
            self.icons[i].rect.y = self.top - 30
        k = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.inv_collection[i][j] is not None:
                    all_sprites.remove(self.inv_collection[i][j].sprite)
        for i in range(len(self.inv_collection)):
            for j in range(len(self.inv_collection[i])):
                if self.inv_collection[i][j] is not None:
                    if self.inv_collection[i][j].type_item == self.current_image.type:
                        sprite = self.inv_collection[i][j].sprite
                        sprite.rect.x = self.left + self.cell_size * j
                        sprite.rect.y = self.top + self.cell_size * i
                        k += 1
                        all_sprites.add(sprite)
        all_sprites.draw(screen)

    def destroy_item(self, cell):
        x, y = cell[0], cell[1]
        if self.inv_collection[y][x] is not None and \
                self.inv_collection[y][x].type_item == self.current_image.type:
            all_sprites.remove(self.inv_collection[y][x].sprite)
            self.inv_collection[y][x] = None
        self.render(screen)

    def on_click(self, cell):
        if cell is not None:
            if is_alone and self.inv_collection[cell[1]][cell[0]] is not None:
                global ex
                if ex is not None:
                    ex.clear()
                ex = ExtraMenu(self.inv_collection[cell[1]][cell[0]])
                ex.render(screen)
            elif self.inv_collection[cell[1]][cell[0]] is not None:
                print(f"Вы удалили {self.inv_collection[cell[1]][cell[0]].name}")
                self.destroy_item(cell)


player_balance = 0


class Merchantry:
    def __init__(self, player_inventory, balance_m, name):
        self.inventory = Inventory(19, 19, copy.copy([icon_swords, icon_potions]))
        self.inventory.left = 650
        self.name = name
        self.player_inventory = player_inventory
        self.balance = balance_m

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if not (self.inventory.left <= x <= self.inventory.left +
                self.inventory.width * self.inventory.cell_size) or \
                not (self.inventory.top <= y <= self.inventory.top +
                     self.inventory.height * self.inventory.cell_size):
            return None
        x -= self.inventory.left
        y -= self.inventory.top
        return x // self.inventory.cell_size, y // self.inventory.cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)
        for i in self.inventory.icons:
            i.up(mouse_pos, self.inventory)

    def on_click(self, cell):
        if cell is not None:
            t = copy.copy(self.inventory.inv_collection[cell[1]][cell[0]])
            if t is not None:
                self.inventory.destroy_item(cell)
                self.player_inventory.take_item(t)
                print(f"Обмен осуществлён между {self.name} и Player")


class UpgradeButton:
    def __init__(self):
        pass


class ExtraMenu:
    def __init__(self, item):
        self.parametres = item.parametres
        self.top, self.left = 100, 650
        self.all_texts = []

    def render(self, screen):
        self.clear()
        k = 0
        for i in self.parametres.keys():
            fonts = pygame.font.Font(None, 50)
            texts = fonts.render(str(i), True, (255, 255, 255))
            text_xs, text_ys = self.left, self.top + k * texts.get_height()
            text_ws, text_hs = texts.get_width(), texts.get_height()
            d = texts
            screen.blit(texts, (text_xs, text_ys))
            self.all_texts.append((d, text_xs, text_ys))
            texts = fonts.render(str(self.parametres[i]), True, (255, 255, 255))
            text_xs, text_ys = self.left + d.get_width() + 10, self.top + k * texts.get_height()
            text_ws, text_hs = texts.get_width(), texts.get_height()
            screen.blit(texts, (text_xs, text_ys))
            self.all_texts.append((texts, text_xs, text_ys))
            k += 1

    def clear(self):
        for i in self.all_texts:
            i[0].fill((0, 0, 0))
            screen.blit(i[0], (i[1], i[2]))


inventory = Inventory(19, 19, [icon_swords, icon_potions])

temp = Item("knife.jpg", "swords", {'damage': 100})

inventory.take_item(temp)

font = pygame.font.Font(None, 50)
text = font.render(str(player_balance), True, (255, 255, 255))
text_x, text_y = 500, 10
text_w, text_h = text.get_width(), text.get_height()
screen.blit(text, (text_x, text_y))

p = Item("Potion_healthy.jpg", "potions", {'duration': 60, 'power': 1})
inventory.take_item(p)

is_alone = False
Ludovik = Merchantry(inventory, 1000, "Ludovik")
Ludovik.inventory.current_image = Ludovik.inventory.icons[1]
Ludovik.inventory.take_item(p)
Ludovik.inventory.render(screen)

all_sprites.draw(screen)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                inventory.get_click(event.pos)
                Ludovik.get_click(event.pos)
            else:
                inventory.get_click(event.pos)

    inventory.render(screen)
    Ludovik.inventory.render(screen)
    pygame.display.flip()

pygame.quit()