import pygame
import sys

pygame.init()

screen = pygame.display.set_mode()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    pygame.display.flip()

pygame.quit()
sys.exit()