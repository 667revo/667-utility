from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QListWidget, QStackedWidget
from src.ui.views.dashboard import DashboardView
from src.ui.style import get_stylesheet
from src.ui.views.optimizer import OptimizerView
from src.ui.views.uninstaller import UninstallerView
from src.ui.views.installer import InstallerView
from src.ui.views.optimizer import OptimizerView, OptimizerCard, OptimizerPage
from src.ui.rain import RainEffect


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("667 Utility")
        self.resize(1100, 700)

        root = QWidget()
        self.setCentralWidget(root)

        layout = QHBoxLayout(root)

        self.sidebar = QListWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.addItems(["Dashboard", "Optimizer", "Installer", "Uninstaller"])
        self.sidebar.setFixedWidth(220)

        self.pages = QStackedWidget()
        self.dashboard = DashboardView()
        self.optimizer = OptimizerPage()
        self.installer = InstallerView()
        self.uninstaller = UninstallerView()
        self.pages.addWidget(self.dashboard)
        self.pages.addWidget(self.optimizer)
        self.pages.addWidget(self.installer)
        self.pages.addWidget(self.uninstaller)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages)

        self.sidebar.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

        self.rain_background = RainEffect(root, drop_count=120)
        self.rain_background.setGeometry(root.rect())
        self.rain_background.lower()

        self.setStyleSheet(get_stylesheet())

    def resizeEvent(self, event):
        if hasattr(self, 'rain_background'):
            self.rain_background.setGeometry(self.centralWidget().rect())
        super().resizeEvent(event)