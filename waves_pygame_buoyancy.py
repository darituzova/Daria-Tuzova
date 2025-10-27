import pygame
import sys
import numpy as np
import json


def set_shift_vertical_to_sinusoids(sinusoids, screen_height, spacing=20, padding=10):
    total_amplitude = sum(2 * sinusoid.amplitude for sinusoid in sinusoids)
    
    all_spacing = spacing * (len(sinusoids) - 1)
    avail_height = screen_height - 2 * padding
    need_height = total_amplitude + all_spacing
    
    if need_height <= avail_height:
        center = screen_height // 2
        current_y = center - need_height // 2
    else:
        scale = avail_height / need_height
        for sinusoid in sinusoids:
            sinusoid.amplitude *= scale
        
        total_amplitude_after = sum(2 * sinusoid.amplitude for sinusoid in sinusoids)
        need_height_after = total_amplitude_after + all_spacing
        
        current_y = padding + (avail_height - need_height_after) / 2
    
    for sinusoid in sinusoids:
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
        y = self.amplitude * np.sin(self.frequency * x - self.speed * self.t) + self.vertical_shift
        
        points = np.stack((x, y.astype(np.int32)), axis=1)
        self.points = points.tolist()
        
        self.t += self.time_step
    
    def draw(self, screen):
        self.create_sinusoid(screen.get_width())
        pygame.draw.lines(screen, self.color, False, self.points, self.line_width)
        
        self.update_circles(screen.get_width())
        for circle in self.circles:
            circle.draw(screen, edge_color=self.color)
        
    def attach_circle(self, circle, x=0):
        circle.x = x
        self.circles.append(circle)
    
    def update_circles(self, screen_width):
        for circle in self.circles:
            if circle.x == 0:
                circle.x = screen_width // 2

            base_y = int(self.amplitude * np.sin(self.frequency * circle.x - self.speed * self.t) + self.vertical_shift)
            circle.y = base_y - circle.buoyancy_offset

class Circle:
    def __init__(self, sinusoid, weight=50, volume=60, radius=15, color=(0, 0, 255), x=0):
        self.sinusoid = sinusoid
        self.weight = weight
        self.volume = volume
        self.radius = radius
        self.color = color
        
        self.density = self.weight / self.volume
        self.x = x
        self.y = sinusoid.vertical_shift
        
        self.gravity = 9.8  # ускорение свободного падения
        self.water_density = 1000  # плотность воды (кг/м³)
        self.buoyancy_offset = self.calculate_buoyancy_offset()
        
        sinusoid.attach_circle(self, x)
    
    def calculate_buoyancy_offset(self):
        gravity_force = self.weight * self.gravity
        buoyancy_force = self.volume * self.water_density * 0.001 * self.gravity # - коэффициент 0.001 используется для масштабирования к пиксельным размерам
        net_force = buoyancy_force - gravity_force

        max_offset = self.sinusoid.amplitude * 1.2 # - чтобы шар не улетал слишком далеко от волны

        buoyancy_offset = net_force * 0.1 # # - коэффициент 0.1 подобран эмпирически для красивого отображения
        buoyancy_offset = max(-max_offset, min(max_offset, buoyancy_offset))
        
        return int(buoyancy_offset)
    
    def draw(self, screen, edge_color):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, edge_color, (self.x, self.y), self.radius, 2)
        
        # Отладочная информация (можно убрать)
        font = pygame.font.Font(None, 24)
        density_text = font.render(f"ρ={self.density:.1f}", True, (0, 0, 0))
        screen.blit(density_text, (self.x - 15, self.y - 30))

def load_config_json(file='configs_json/config6.json'):
    try:
        with open(file, 'r', encoding='UTF-8') as f:
            return json.load(f)
    except Exception as e:
        print(f'Ошибка: {e}')
        
def create_sinusoids_from_config(config):
    sinusoids = []
    for sinusoid_config in config.get('sinusoids', []):
        sinusoid = Sinusoid(amplitude=sinusoid_config.get('amplitude', 50), frequency=sinusoid_config.get('frequency', 0.2),
                            speed=sinusoid_config.get('speed', 0.1), color=tuple(sinusoid_config.get('color', [255, 0, 0])),
                            line_width=sinusoid_config.get('line_width', 3), step=sinusoid_config.get('step', 1),
                            time_step=sinusoid_config.get('time_step', 0.05))
        sinusoids.append(sinusoid)
    return sinusoids

def create_circles_from_config(config, sinusoids):
    circles = []
    for i, sinusoid in enumerate(sinusoids):
        circle_configs = config.get('circles', [])
        if i < len(circle_configs):
            circle_config = circle_configs[i]
            circle = Circle(sinusoid, weight=circle_config.get('weight', 50), volume=circle_config.get('volume', 60),
                            radius=circle_config.get('radius', 15), color=tuple(circle_config.get('color', [0, 0, 255])))
        else:
            circle = Circle(sinusoid)
        circles.append(circle)  
    return circles

pygame.init()

config = load_config_json()

screen = pygame.display.set_mode((config.get('window', {}).get('width', 0), config.get('window', {}).get('height', 0)), pygame.RESIZABLE)
pygame.display.set_caption(config.get('window', {}).get('title', 'Волны'))

background_color = tuple(config.get('background_color', [239, 238, 238]))

sinusoids = create_sinusoids_from_config(config)
circles = create_circles_from_config(config, sinusoids)

layout = config.get('layout', {})
set_shift_vertical_to_sinusoids(sinusoids, screen.get_height(), spacing=layout.get('spacing', 20), padding=layout.get('padding', 10))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(background_color)
    for sinusoid in sinusoids: 
        sinusoid.draw(screen)

    pygame.display.flip()

pygame.quit()

sys.exit()