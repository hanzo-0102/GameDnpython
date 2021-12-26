import pygame

pygame.init()
size = WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode(size)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
