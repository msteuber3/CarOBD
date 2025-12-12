from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QFont, QColor, QPen

from custom_widgets.DisplayMeter import DisplayMeter
from utils.OBDConstants import OBDConstants


class PlainTextDisplay(DisplayMeter):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.widget_color = QColor('#2c3e50')

    def _draw_widget(self, painter):
        self.__draw_background(painter)
        self.__draw_text(painter)

    def __draw_background(self, painter):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.widget_color)
        painter.drawRoundedRect(QRectF(-100, -100, 200, 200), 20, 20)

        pen_width = 4
        inset = int(pen_width / 2)
        painter.setPen(QPen(QColor(0, 0, 0), pen_width))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(-100 + inset, -100 + inset, 200 - 2 * inset, 200 - 2 * inset), 15, 15)

    def __draw_text(self, painter):
        value_font = QFont("TypeWriter", 32)
        name_font = QFont("Arial", 18)
        painter.setFont(value_font)
        painter.setPen(self.text_color)
        fm = painter.fontMetrics()

        value_display = f"{float(self.value)}"
        value_width = fm.horizontalAdvance(value_display)
        name_width = fm.horizontalAdvance(self.name)

        painter.drawText(int(-value_width / 2), 0, value_display)

        painter.setFont(name_font)
        painter.drawText(
            -int((OBDConstants.WIDGET_INNER_WIDTH.value / 2) - name_width / 2),
            int(OBDConstants.WIDGET_NAME_POS.value),
            self.name
        )