import sys
import pygame

screen = pygame.display.set_mode((400, 400))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)


    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 0, 255), (0, 0, 20, 20), 0)
    pygame.display.flip()
