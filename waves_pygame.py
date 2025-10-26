import pygame
import sys
import numpy as np
import math

def set_shift_vertical_to_sinusoids(sinusoids, screen_height):
    total_amplitude = sum(2 * sinusoid.amplitude for sinusoid in sinusoids)
    
    spacing = 20
    all_spacing = spacing * (len(sinusoids) - 1)
    avail_height = screen_height - all_spacing
    need_height = total_amplitude + all_spacing
    
    if need_height > avail_height:
        scale = avail_height / need_height
        for sinusoid in sinusoids:
            sinusoid.amplitude *= scale
        total_amplitude *= scale

    current_y = 0
    
    for sinusoid in sinusoids:
        sinusoid.vertical_shift = current_y + sinusoid.amplitude
        current_y = sinusoid.vertical_shift + sinusoid.amplitude + spacing
class Sinusoid:
    def __init__(self, amplitude, frequency, speed, color, line_width):
        self.amplitude = amplitude
        self.frequency = frequency
        self.speed = speed
        self.color = color
        self.line_width = line_width
        
        self.vertical_shift = 0
        self.t = 0
        self.points = []
    
    def create_sinusoid(self, screen_width, screen_height):
        x = np.arange(0, screen_width, 2)
        y = self.amplitude * np.sin(self.frequency * x + self.speed * self.t) + self.vertical_shift
        
        points = np.stack((x, y.astype(np.int32)), axis=1)
        
        self.points = points.tolist()
        
        self.t += 0.05
        
    def draw_sinusoid(self, screen):
        
        self.create_sinusoid(screen.get_width(), screen.get_height())
        
        pygame.draw.lines(screen, self.color, False, self.points, self.line_width)    
        
pygame.init()

screen = pygame.display.set_mode()

sinusoids = [Sinusoid(200, 0.1, 0.1, (0, 255, 0), 2), Sinusoid(200, 0.02, 0.04, (255, 0, 0), 2), Sinusoid(100, 0.5, 0.5, (0, 0, 255), 2)]

set_shift_vertical_to_sinusoids(sinusoids, screen.get_height())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    screen.fill((0, 0, 0))
    for sinusoid in sinusoids: 
        sinusoid.draw_sinusoid(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit()