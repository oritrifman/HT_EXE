from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt, QTimer


class CandleSlider(QSlider):

    def __init__(self, parent=None):
        super().__init__(Qt.Orientation.Vertical, parent)
        self.flame_styles = [
            self.candle_style(30, "0 -9px 0 -9px", 0.70),
            self.candle_style(34, "-3px -8px 0 -10px", 0.62),
            self.candle_style(27, "2px -10px 0 -8px", 0.78),
            self.candle_style(32, "-1px -9px 0 -9px", 0.66),
        ]
        self.flame_index = 0
        self.flicker_timer = QTimer()
        self.flicker_timer.timeout.connect(self.flicker)
        self.setStyleSheet(self.flame_styles[0])

    def candle_style(self, flame_height, flame_margin, flame_center):
        return f"""
            QSlider {{ background: transparent; }}
            QSlider::groove:vertical {{ width: 14px; background: transparent; }}
            QSlider::sub-page:vertical {{ background: transparent; }}
            QSlider::add-page:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb(30, 70, 160), stop:0.45 rgb(170, 205, 255), stop:1 rgb(30, 70, 160));
                border: 1px solid rgb(20, 45, 110);
                border-radius: 3px;
            }}
            QSlider::handle:vertical {{
                height: {flame_height}px;
                margin: {flame_margin};
                border-radius: 15px;
                background: qradialgradient(cx:0.5, cy:{flame_center}, radius:0.6, fx:0.5, fy:{flame_center + 0.1},
                    stop:0 rgb(255, 255, 230), stop:0.3 rgb(255, 225, 90), stop:0.65 rgb(255, 140, 30),
                    stop:1 rgba(255, 70, 0, 0));
            }}
        """

    def enterEvent(self, event):
        self.flicker_timer.start(90)

    def leaveEvent(self, event):
        self.flicker_timer.stop()
        self.flame_index = 0
        self.setStyleSheet(self.flame_styles[0])

    def flicker(self):
        self.flame_index = (self.flame_index + 1) % len(self.flame_styles)
        self.setStyleSheet(self.flame_styles[self.flame_index])