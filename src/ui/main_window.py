from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QListWidget,
                                QStackedWidget, QGraphicsOpacityEffect)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from src.ui.views.dashboard import DashboardView
from src.ui.style import get_stylesheet
from src.ui.views.optimizer import OptimizerPage
from src.ui.views.uninstaller import UninstallerView
from src.ui.views.installer import InstallerView
from src.ui.rain import RainEffect


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("667 Utility")
        self.resize(1100, 700)
        self.setMinimumSize(900, 600)

        root = QWidget()
        root.setObjectName("RootWidget")
        self.setCentralWidget(root)

        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = QListWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.addItems(["  Dashboard", "  Optimizer", "  Installer", "  Uninstaller"])
        self.sidebar.setFixedWidth(200)

        self.pages = QStackedWidget()
        self.optimizer = OptimizerPage()
        self.dashboard = DashboardView(optimizer_page=self.optimizer)
        self.installer = InstallerView()
        self.uninstaller = UninstallerView()

        self._page_list = [self.dashboard, self.optimizer, self.installer, self.uninstaller]
        self._effects = []
        self._fade_anims = []

        for page in self._page_list:
            self.pages.addWidget(page)
            effect = QGraphicsOpacityEffect()
            effect.setOpacity(1.0)
            page.setGraphicsEffect(effect)
            self._effects.append(effect)

            anim = QPropertyAnimation(effect, b"opacity")
            anim.setDuration(200)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            self._fade_anims.append(anim)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages, stretch=1)

        self._current_index = 0
        self._animating = False

        self._anim_sidebar_pulse = QPropertyAnimation(self.sidebar, b"maximumWidth")
        self._anim_sidebar_pulse.setDuration(150)
        self._anim_sidebar_pulse.setEasingCurve(QEasingCurve.OutCubic)

        self.sidebar.currentRowChanged.connect(self._switch_page)
        self.sidebar.setCurrentRow(0)

        self.rain_background = RainEffect(root, drop_count=80)
        self.rain_background.setGeometry(root.rect())
        self.rain_background.lower()

        self.setStyleSheet(get_stylesheet())

    def _switch_page(self, index):
        if self._animating or index == self._current_index:
            return
        self._animating = True
        self._next_index = index
        if index == 0:
            self.dashboard.refresh()
        self._sidebar_pulse()
        self._fade_out(self._current_index)

    def _fade_out(self, index):
        anim = self._fade_anims[index]
        anim.stop()
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        try:
            anim.finished.disconnect()
        except RuntimeError:
            pass
        anim.finished.connect(lambda: self._on_fade_out_done(index))
        anim.start()

    def _on_fade_out_done(self, old_index):
        try:
            self._fade_anims[old_index].finished.disconnect()
        except RuntimeError:
            pass
        self.pages.setCurrentIndex(self._next_index)
        self._current_index = self._next_index
        self._fade_in(self._next_index)

    def _fade_in(self, index):
        anim = self._fade_anims[index]
        anim.stop()
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        try:
            anim.finished.disconnect()
        except RuntimeError:
            pass
        anim.finished.connect(self._on_fade_in_done)
        anim.start()

    def _on_fade_in_done(self):
        try:
            self._fade_anims[self._current_index].finished.disconnect()
        except RuntimeError:
            pass
        self._animating = False

    def _sidebar_pulse(self):
        self._anim_sidebar_pulse.stop()
        self._anim_sidebar_pulse.setStartValue(200)
        self._anim_sidebar_pulse.setEndValue(206)
        self._anim_sidebar_pulse.finished.connect(self._sidebar_pulse_back)
        self._anim_sidebar_pulse.start()

    def _sidebar_pulse_back(self):
        self._anim_sidebar_pulse.finished.disconnect(self._sidebar_pulse_back)
        self._anim_sidebar_pulse.setStartValue(206)
        self._anim_sidebar_pulse.setEndValue(200)
        self._anim_sidebar_pulse.start()

    def resizeEvent(self, event):
        if hasattr(self, 'rain_background'):
            self.rain_background.setGeometry(self.centralWidget().rect())
        super().resizeEvent(event)