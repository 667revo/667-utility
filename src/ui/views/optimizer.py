from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame, QScrollArea, QHBoxLayout
from src.ui.theme import Colors
from src.ui.views.optimizer_card import OptimizerCard
from src.ui.views.modern_button import ModernButton

class OptimizerView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # şimdilik placeholder, sonra doldururuz
        layout = QVBoxLayout(self)
        label = QLabel("Optimizer")
        layout.addWidget(label)

class OptimizerPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Başlık
        header = QVBoxLayout()
        title = QLabel("System Optimizer")
        title.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 700;
        """)
        subtitle = QLabel("Apply tweaks to improve performance and responsiveness.")
        header.addWidget(title)
        header.addWidget(subtitle)
        layout.addLayout(header)

        # Scroll alanı
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        scroll_content = QWidget()
        cards_layout = QVBoxLayout(scroll_content)
        cards_layout.setSpacing(12)
        cards_layout.setContentsMargins(0, 0, 0, 0)

        # Kartlar — bunlar optimizer seçeneklerin
        optimizations = [
            ("Disable SysMain (Superfetch)",
             "Reduces disk usage on SSDs. Recommended for systems with 8GB+ RAM.",
             "safe"),
            ("Set High Performance Power Plan",
             "Maximizes CPU performance. Increases power consumption on laptops.",
             "warning"),
            ("Disable Telemetry Services",
             "Stops Windows data collection. May affect Windows Update in rare cases.",
             "warning"),
            ("Clear Temp Files",
             "Removes temporary files from %TEMP% and Windows\\Temp folders.",
             "safe"),
            ("Disable Xbox Game Bar",
             "Frees up background resources. Disables overlay and recording features.",
             "safe"),
            ("Disable Search Indexing",
             "Reduces CPU/disk usage. Search results may be slower to appear.",
             "danger"),
        ]

        for title_text, desc, status in optimizations:
            card = OptimizerCard(title_text, desc, status)
            cards_layout.addWidget(card)

        cards_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Alt butonlar
        bottom = QHBoxLayout()
        apply_all = ModernButton("Apply All Safe", variant="primary")
        apply_all.setFixedWidth(160)
        reset = ModernButton("Reset Defaults", variant="ghost")
        reset.setFixedWidth(140)

        bottom.addStretch()
        bottom.addWidget(reset)
        bottom.addWidget(apply_all)
        layout.addLayout(bottom)