from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QBrush
import random

_COLORS = [
    (255, 255, 255),   # beyaz
    (200, 150, 255),   # soft mor
    (150, 190, 255),   # soft mavi
    (220, 130, 255),   # canlı mor
]


class RainEffect(QWidget):
    def __init__(self, parent=None, drop_count=80):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.drop_count = drop_count
        self.drops = []
        self._init_drops()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(16)

    def _init_drops(self):
        w = self.parent().width() if self.parent() else 800
        h = self.parent().height() if self.parent() else 600
        self.drops = [self._new_drop(w, h, spawn_anywhere=True) for _ in range(self.drop_count)]

    def _new_drop(self, w, h, spawn_anywhere=False):
        r, g, b = random.choice(_COLORS)
        return {
            'x': random.uniform(0, w),
            'y': random.uniform(-h, h) if spawn_anywhere else random.uniform(-60, -10),
            'speed': random.uniform(3.5, 11.0),
            'length': random.uniform(14, 48),
            'alpha': random.randint(30, 85),
            'width': random.uniform(0.8, 2.0),
            'drift': random.uniform(-0.3, 0.3),
            'r': r, 'g': g, 'b': b,
        }

    def _tick(self):
        h = self.height() or (self.parent().height() if self.parent() else 600)
        w = self.width() or (self.parent().width() if self.parent() else 800)
        for i, d in enumerate(self.drops):
            d['y'] += d['speed']
            d['x'] += d['drift']
            if d['y'] > h + d['length']:
                self.drops[i] = self._new_drop(w, h)
        self.update()

    def resizeEvent(self, event):
        self.setGeometry(self.parent().rect() if self.parent() else self.rect())
        QWidget.resizeEvent(self, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        for d in self.drops:
            x = d['x']
            y = d['y']
            length = d['length']
            w = d['width']
            alpha = d['alpha']
            r, g, b = d['r'], d['g'], d['b']

            grad = QLinearGradient(x, y, x, y + length)
            grad.setColorAt(0.0, QColor(r, g, b, 0))
            grad.setColorAt(0.5, QColor(r, g, b, alpha // 4))
            grad.setColorAt(1.0, QColor(r, g, b, alpha))

            painter.setBrush(QBrush(grad))
            painter.drawRect(QRectF(x - w / 2, y, w, length))
