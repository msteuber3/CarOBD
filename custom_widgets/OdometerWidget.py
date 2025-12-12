from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QColor, QPen, QPolygonF, QFont

from custom_widgets.DisplayMeter import DisplayMeter


class OdometerWidget(DisplayMeter):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)

        self.num_ticks = 14
        self.tick_diff = 20

        self.widget_color = QColor('#2c3e50')
        self.tick_color = QColor(224, 38, 9)
        self.needle_color = QColor('#e74c3c')

        self.start_angle = 150 # angle at which 0 is displayed
        self.span_angle = 240 # total angle covered by the odom'

    def _draw_widget(self, painter):
        self.__draw_background(painter)
        self.__draw_ticks(painter)
        self.__draw_needle(painter)
        self.__draw_bottom_text(painter)

    def __draw_background(self, painter):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.widget_color)
        painter.drawEllipse(-100, -100, 200, 200)

        # Draw border
        pen_width = 5
        inset = int(pen_width / 2)
        painter.setPen(QPen(QColor(0, 0, 0), pen_width))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(-100 + inset, -100 + inset, 200 - 2*inset, 200 - 2*inset)

    def __draw_ticks(self, painter):
        painter.setPen(QPen(self.tick_color, 2))
        font = QFont("Arial", 8)
        painter.setFont(font)

        for i in range(self.num_ticks):
            current_tick_val = self.min_value + (i * (self.max_value - self.min_value) / (self.num_ticks - 1))
            painter.save()

            # Degrees between each tick
            angle_step = -self.span_angle / (self.num_ticks - 1)
            # Angle of the current tick from 0
            rotation_angle = self.start_angle - angle_step * i

            # Rotate the painter to draw the tick at the correct angle. After this, the 'dometer is positioned such that the y-axis points in the direction of the tick
            painter.rotate(rotation_angle - 90)
            # ^ that allows me to draw the line from 0 -> 0 on the x-axis
            painter.drawLine(0, 85, 0, 95)

            # reset the 'dom so that the numbers can be drawn inside the ticks
            painter.translate(0, 75)
            painter.rotate(-(rotation_angle - 90))

            text = f"{int(current_tick_val)}"

            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(text)
            text_height = fm.height()
            painter.drawText(int(-text_width / 2), int(text_height / 4), text)

            painter.restore()

    def __draw_needle(self, painter):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.needle_color)

        painter.save()

        needle_val = max(self.min_value, min(self.value, self.max_value))

        value_range = self.max_value - self.min_value
        value_ratio = (needle_val - self.min_value) / value_range if value_range else 0
        current_angle = self.start_angle + (value_ratio * self.span_angle)

        painter.rotate(current_angle - 90)

        needle = QPolygonF([QPointF(0, -10), QPointF(-5, 0), QPointF(0, 80), QPointF(5, 0)])

        painter.drawConvexPolygon(needle)

        painter.setBrush(self.tick_color)
        painter.drawEllipse(-8, -8, 16, 16)

        painter.restore()

    def __draw_bottom_text(self, painter):
        font = QFont("TypeWriter", 12)
        painter.setFont(font)
        painter.setPen(self.text_color)
        fm = painter.fontMetrics()

        unit_text = "MPH"
        value_display = f"{float(self.value)}"

        unit_width = fm.horizontalAdvance(unit_text)
        value_width = fm.horizontalAdvance(value_display)
        name_width = fm.horizontalAdvance(self.name)

        painter.drawText(int(-unit_width / 2), 50, unit_text)
        painter.drawText(int(-value_width / 2), 70, value_display)
        painter.drawText(int(-name_width / 2), 90, self.name)

