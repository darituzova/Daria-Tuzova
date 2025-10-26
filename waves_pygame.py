import pygame
import sys
import numpy as np
import math


def set_shift_vertical_to_sinusoids(sinusoids, screen_height, spacing=20):
    total_amplitude = sum(2 * sinusoid.amplitude for sinusoid in sinusoids)
    
    all_spacing = spacing * (len(sinusoids) - 1)
    avail_height = screen_height - all_spacing
    need_height = total_amplitude + all_spacing
    
    if need_height <= screen_height:
        center = screen_height // 2
        current_y = center - need_height // 2
        flag_scale = False
    else:
        scale = avail_height / need_height
        current_y = 0
        flag_scale = True
        
    for sinusoid in sinusoids:
        if flag_scale:
            sinusoid.amplitude *= scale
        sinusoid.vertical_shift = current_y + sinusoid.amplitude
        current_y = sinusoid.vertical_shift + sinusoid.amplitude + spacing
        
class Sinusoid:
    def __init__(self, amplitude=50, frequency=0.2, speed=0.1, color=(128, 128, 128), line_width=1, step=1, time_step=0.05):
        self.amplitude = amplitude
        self.frequency = frequency
        self.speed = speed
        self.color = color
        self.line_width = line_width
        self.step = step
        self.time_step = time_step
        
        self.vertical_shift = 0
        self.t = 0
        self.points = []
    
    def create_sinusoid(self, screen_width):
        x = np.arange(0, screen_width, self.step)
        y = self.amplitude * np.sin(self.frequency * x + self.speed * self.t) + self.vertical_shift
        
        points = np.stack((x, y.astype(np.int32)), axis=1)
        self.points = points.tolist()
        
        self.t += self.time_step
        
    def draw_sinusoid(self, screen):
        self.create_sinusoid(screen.get_width())
        pygame.draw.lines(screen, self.color, False, self.points, self.line_width)    
        

pygame.init()

screen = pygame.display.set_mode()

sinusoids = [Sinusoid(), Sinusoid(200, 0.02, 0.04, (255, 0, 0), 3), Sinusoid(100, 0.07, 0.05, (0, 0, 255), 2)]
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