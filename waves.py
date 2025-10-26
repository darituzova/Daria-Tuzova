import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter

class Waves(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Волны')
        self.resize(1000, 700)
        
        self.setStyleSheet('background-color: #42aaff')
        
app = QApplication(sys.argv)

window_waves = Waves()
window_waves.show()

sys.exit(app.exec_())