from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPainter, QFont, QColor
from PyQt6.QtWidgets import QWidget, QSlider, QVBoxLayout

class DisplayMeter(QWidget):
    def __init__(self, name, parent=None):
        super().__init__(parent)

        self.value = 0
        self.min_value = 0
        self.max_value = 260
        self.name = name
        self.text_color = QColor(20, 20, 20)

    def set_value(self, value):
        """
        Sets the real internal value and repaints the widget
        value: The new value to set
        """
        self.value = value
        self.update()

    def sizeHint(self):
        return QSize(400, 400)

    def paintEvent(self, event):
        painter = QPainter(self)

        width = self.width()
        height = self.height()

        painter.translate(width / 2, height / 2)
        scale_factor = min(width, height) / 200
        painter.scale(scale_factor, scale_factor)

        self._draw_widget(painter)

        painter.end()

    def _draw_widget(self, painter):
        pass