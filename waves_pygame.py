import pygame
import sys
import numpy as np

class Sinusoid:
    def __init__(self, amplitude, frequency, speed, phase, color, line_width):
        self.amplitude = amplitude
        self.frequency = frequency
        self.speed = speed 
        self.phase = phase
        self.color = color
        self.line_width = line_width
        
        self.t = 0
        self.points = []
    
    def create_sinusoid(self, screen_width, screen_height):
        shift_vertical = screen_height // 2
        
        x = np.arange(0, screen_width, 2)
        y = self.amplitude * np.sin(self.frequency * x + self.speed * self.t + self.phase) + shift_vertical
        
        points = np.stack((x, y.astype(np.int32)), axis=1)
        
        self.points = points.tolist()
        
        self.t += 0.05
        
    def draw_sinusoid(self, screen):
        
        self.create_sinusoid(screen.get_width(), screen.get_height())
        
        pygame.draw.lines(screen, self.color, False, self.points, self.line_width)    
        
pygame.init()

screen = pygame.display.set_mode()

sinusoid = Sinusoid(100, 0.02, 0.1, 0, (0, 255, 0), 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    screen.fill((0, 0, 0)) 
    sinusoid.draw_sinusoid(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit()