import pygame
import sys
import numpy as np


def set_shift_vertical_to_sinusoids(sinusoids, screen_height, spacing=20, padding=10):
    total_amplitude = sum(2 * sinusoid.amplitude for sinusoid in sinusoids)
    
    all_spacing = spacing * (len(sinusoids) - 1)
    avail_height = screen_height - 2 * padding
    need_height = total_amplitude + all_spacing
    
    if need_height <= avail_height:
        center = screen_height // 2
        current_y = center - need_height // 2
        flag_scale = False
    else:
        scale = (avail_height + all_spacing) / need_height
        current_y = padding
        flag_scale = True
    
    for sinusoid in sinusoids:
        if flag_scale:
            sinusoid.amplitude *= scale
        sinusoid.vertical_shift = current_y + sinusoid.amplitude
        current_y = sinusoid.vertical_shift + sinusoid.amplitude + spacing
        
class Sinusoid:
    def __init__(self, amplitude=50, frequency=0.2, speed=0.1, color=(255, 0, 0), line_width=3, step=1, time_step=0.05):
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
        
        self.circles = []
    
    def create_sinusoid(self, screen_width):
        x = np.arange(0, screen_width, self.step)
        y = self.amplitude * np.sin(self.frequency * x + self.speed * self.t) + self.vertical_shift
        
        points = np.stack((x, y.astype(np.int32)), axis=1)
        self.points = points.tolist()
        
        self.t += self.time_step
    
    def draw(self, screen):
        self.create_sinusoid(screen.get_width())
        pygame.draw.lines(screen, self.color, False, self.points, self.line_width)
        
        self.update_circles(screen.get_width())
        for circle in self.circles:
            circle.draw_circle(screen, edge_color=self.color)
        
    def attach_circle(self, circle, x=0):
        circle.x = x
        self.circles.append(circle)
    
    def update_circles(self, screen_width):
        for circle in self.circles:
            if circle.x == 0:
                circle.x = screen_width // 2
            circle.y = int(self.amplitude * np.sin(self.frequency * circle.x + self.speed * self.t) + self.vertical_shift)

class Circle:
    def __init__(self, sinusoid, weight=50, volume=60, radius=15, color=(0, 0, 255), x=0):
        self.sinusoid = sinusoid
        self.weight = weight
        self.volume = volume
        self.radius = radius
        self.color = color
        
        self.density = self.weight / self.volume
        
        self.x = x
        self.y = 0
        
        sinusoid.attach_circle(self, x)
    
    def draw_circle(self, screen, edge_color):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, edge_color, (self.x, self.y), self.radius, 2)


pygame.init()

screen = pygame.display.set_mode()
sinusoids = [Sinusoid(amplitude=100, frequency=0.07, speed=0.07), Sinusoid(amplitude=100, frequency=0.05, speed=0.05), Sinusoid(amplitude=100, frequency=0.03, speed=0.03), Sinusoid(amplitude=100, frequency=0.01, speed=0.1)]
set_shift_vertical_to_sinusoids(sinusoids, screen.get_height())

circles = [Circle(sinusoids[0]), Circle(sinusoids[1]), Circle(sinusoids[2]), Circle(sinusoids[3])]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    screen.fill((239, 238, 238))
    for sinusoid in sinusoids: 
        sinusoid.draw(screen)

    pygame.display.flip()

pygame.quit()

sys.exit()