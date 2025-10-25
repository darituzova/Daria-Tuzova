import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter

class Waves(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(500, 600, 1000, 700)

app = QApplication(sys.argv)

window_waves = Waves()
window_waves.show()

sys.exit(app.exec_())