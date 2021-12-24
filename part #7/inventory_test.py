import pygame
import copy
import os
import sys


balance = 0


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

        self.left = 30
        self.top = 30
        self.cell_size = 33

    def view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                screen.blit(load_image('emptyslot.png'),
                            (x * self.cell_size + self.left, y * self.cell_size + self.top))

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
    def __init__(self, image, type_of_item, price=0):
        self.image = load_image(image, colorkey=-1)
        self.image_name = image
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.image
        self.sprite.rect = self.sprite.image.get_rect()
        self.type_item = type_of_item
        self.price = price


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
                                                     type_of_item=item.type_item, price=item.price)
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
        if self.inv_collection[y][x] is not None:
            all_sprites.remove(self.inv_collection[y][x].sprite)
            self.inv_collection[y][x] = None
        self.render(screen)

    def on_click(self, cell):
        if cell is not None:
            self.destroy_item(cell)


class Merchantry:
    def __init__(self, player_inventory, balance_m, name):
        self.inventory = Inventory(10, 10, copy.copy([icon_swords, icon_potions]))
        self.inventory.left = 650
        self.name = name
        self.player_inventory = player_inventory
        self.balance = balance_m

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if not (self.inventory.left <= x <= self.inventory.left + self.inventory.width * self.inventory.cell_size) or \
                not (self.inventory.top <= y <= self.inventory.top + self.inventory.height * self.inventory.cell_size):
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


inventory = Inventory(10, 10, [icon_swords, icon_potions])

temp = Item("knife.jpg", "swords")

inventory.take_item(temp)

font = pygame.font.Font(None, 50)
text = font.render(str(balance), True, (255, 255, 255))
text_x, text_y = 500, 10
text_w, text_h = text.get_width(), text.get_height()
screen.blit(text, (text_x, text_y))

p = Item("Potion_healthy.jpg", "potions")

inventory.take_item(p)

Luis = Merchantry(inventory, 1000, "Luis")
Luis.inventory.current_image = Luis.inventory.icons[1]
Luis.inventory.take_item(p)
Luis.inventory.render(screen)

all_sprites.draw(screen)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            inventory.get_click(event.pos)
            Luis.get_click(event.pos)

    inventory.render(screen)
    Luis.inventory.render(screen)
    pygame.display.flip()

pygame.quit()