import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QColor

class Waves(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Волны')
        self.resize(1000, 700)
        
        self.setStyleSheet('background-color: #42aaff')
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        self.draw_sinusoid(painter)
        self.draw_circle(painter)
    
    def draw_sinusoid(self, painter):
        painter.setPen(QPen(QColor('#8b00ff'), 3))
        
        amplitude = 100
        frequency = 0.09
        shift_vertical = 300
        
        points = []
        
        for x in range(0, self.width(), 2):
            y = int(amplitude * math.sin(frequency * x) + shift_vertical)
            points.append((x, y))
        
        for i in range(1, len(points)):
            x1, y1 = points[i - 1]
            x2, y2 = points[i]
            painter.drawLine(x1, y1, x2, y2)
    
    def draw_circle(self, painter):
        painter.setBrush(QColor('#30d5c8'))
        
        amplitude = 100
        frequency = 0.09
        shift_vertical = 300
        
        x = 500
        y = int(amplitude * math.sin(frequency * x) + shift_vertical)
        
        painter.drawEllipse(x - 20, y - 20, 40, 40)

app = QApplication(sys.argv)

window_waves = Waves()
window_waves.show()

sys.exit(app.exec_())