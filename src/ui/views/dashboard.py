from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame, QFormLayout
from src.ui.process import get_system_info


class StatCard(QFrame):
    def __init__(self, title: str, value: str):
        super().__init__()
        self.setObjectName("StatCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        title_label = QLabel(title)
        title_label.setObjectName("CardTitle")
        self.value_label = QLabel(value)
        self.value_label.setObjectName("CardValue")
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)

    def set_value(self, value: str):
        self.value_label.setText(value)


class ActionCard(QFrame):
    def __init__(self, title: str, subtitle: str):
        super().__init__()
        self.setObjectName("ActionCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(4)
        title_label = QLabel(title)
        title_label.setObjectName("ActionTitle")
        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("ActionSubtitle")
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)


class DashboardView(QWidget):
    def __init__(self, optimizer_page=None):
        super().__init__()
        self.optimizer_page = optimizer_page

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QLabel("667 Utility")
        header.setObjectName("PageTitle")

        subtitle = QLabel("Main Page")
        subtitle.setObjectName("PageSubtitle")

        stat_grid = QGridLayout()
        stat_grid.setHorizontalSpacing(16)
        stat_grid.setVerticalSpacing(16)

        self.installed_card = StatCard("Installed Apps", "0")
        self.tweaks_card = StatCard("Applied Tweaks", "0")

        stat_grid.addWidget(self.installed_card, 0, 0)
        stat_grid.addWidget(self.tweaks_card, 0, 1)

        section = QLabel("System")
        section.setObjectName("SectionTitle")

        info = get_system_info()

        action_grid = QFormLayout()
        action_grid.setVerticalSpacing(16)
        action_grid.addRow("OS", QLabel(info["os"]))
        action_grid.addRow("CPU", QLabel(info["cpu_name"]))
        action_grid.addRow("CPU Usage", QLabel(f"{info['cpu_usage']:.0f}%"))
        action_grid.addRow("RAM", QLabel(f"{info['ram_total']:.1f} GB"))
        action_grid.addRow("RAM Usage", QLabel(f"{info['ram_used']:.1f} GB"))

        layout.addWidget(header)
        layout.addWidget(subtitle)
        layout.addLayout(stat_grid)
        layout.addWidget(section)
        layout.addLayout(action_grid)

        self.refresh()

    def refresh(self):
        count = self.optimizer_page.applied_count() if self.optimizer_page else 0
        self.tweaks_card.set_value(str(count))