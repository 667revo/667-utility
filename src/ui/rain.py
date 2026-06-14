from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QColor, QPen
import random

class RainEffect(QWidget):
    def __init__(self, parent=None, drop_count=100):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.drop_count = drop_count
        self.drops = []
        self._init_drops()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)

    def _init_drops(self):
        w = self.parent().width() if self.parent() else 800
        h = self.parent().height() if self.parent() else 600
        self.drops = []
        for _ in range(self.drop_count):
            self.drops.append({
                'x': random.uniform(0, w),
                'y': random.uniform(0, h),
                'speed': random.uniform(5.0, 10.0),
                'length': random.uniform(10, 25),
                'alpha': random.randint(30, 90),
                'width': random.uniform(0.5, 1.5)
            })

    def update_animation(self):
        h = self.height() or (self.parent().height() if self.parent() else 600)
        w = self.width() or (self.parent().width() if self.parent() else 800)
        for d in self.drops:
            d['y'] += d['speed']
            if d['y'] > h:
                d['y'] = -d['length']
                d['x'] = random.uniform(0, w)
        self.update()

    def resizeEvent(self, event):
        self.setGeometry(self.parent().rect() if self.parent() else self.rect())
        QWidget.resizeEvent(self, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for d in self.drops:
            color = QColor(255,255,255, d['alpha'])
            pen = QPen(color)
            pen.setWidthF(d['width'])
            painter.setPen(pen)
            painter.drawLine(QPointF(d['x'], d['y']), QPointF(d['x'], d['y'] + d['length']))