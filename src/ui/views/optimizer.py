import subprocess

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea, QHBoxLayout
from src.ui.views.optimizer_card import OptimizerCard
from src.ui.views.modern_button import ModernButton
from core.optimizations import Optimizations


class OptimizerView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Optimizer")
        layout.addWidget(label)


class OptimizerPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def applied_count(self) -> int:
        return sum(1 for card in self.cards if card.is_applied)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        header = QVBoxLayout()
        title = QLabel("System Optimizer")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")
        subtitle = QLabel("Apply tweaks to improve performance and responsiveness.")
        header.addWidget(title)
        header.addWidget(subtitle)
        layout.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        cards_layout = QVBoxLayout(scroll_content)
        cards_layout.setSpacing(12)
        cards_layout.setContentsMargins(0, 0, 0, 0)

        optimizations = [
            (
                "Clear Temp Files",
                "Removes temporary files from %TEMP% and Windows\\Temp folders.",
                "safe",
                Optimizations.clear_temp,
                None,
            ),
            (
                "Disable SysMain (Superfetch)",
                "Reduces disk usage on SSDs. Recommended for systems with 8GB+ RAM.",
                "safe",
                Optimizations.disable_sysmain,
                Optimizations.enable_sysmain,
            ),
            (
                "Regedit Tweaks",
                "Applies all registry tweaks for CPU, GPU and system performance.",
                "warning",
                Optimizations.apply_all_reg,
                None,
            ),
            (
                "Lower Input Delay",
                "Lowers input delay with optimizing boot settings",
                "safe",
                Optimizations.lower_input_delay,
                None,
            ),
            (
                "Set High Performance Power Plan",
                "Maximizes CPU performance. Increases power consumption on laptops.",
                "safe",
                Optimizations.set_high_performance,
                None,
            ),
            (
                "Disable Telemetry Services",
                "Stops Windows data collection. May affect Windows Update in rare cases.",
                "safe",
                Optimizations.disable_telemetry,
                Optimizations.enable_telemetry,
            ),
            (
                "Disable Xbox Services and GameBar",
                "Frees up background resources. Disables overlay and recording features.",
                "safe",
                Optimizations.disable_xbox_services,
                Optimizations.enable_xbox_services,
            ),
            (
                "Disable Search Indexing",
                "Reduces CPU/disk usage. Search results may be slower to appear.",
                "warning",
                Optimizations.disable_search_index,
                Optimizations.enable_search_index,
            ),
            (
                "Service Reducer",
                "Reduces Services executed on CPU and gives smoother game experience",
                "safe",
                Optimizations.reduce_services,
                Optimizations.restore_services,
            ),
            (
                "Disable Background Apps",
                "Prevents UWP apps from running in the background.",
                "safe",
                Optimizations.disable_background_apps,
                Optimizations.enable_background_apps,
            ),
        ]

        self.cards = []
        for title_text, desc, status, callback, undo_callback in optimizations:
            card = OptimizerCard(
                title_text, desc, status,
                callback=callback,
                undo_callback=undo_callback
            )
            self.cards.append(card)
            cards_layout.addWidget(card)

        cards_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        def on_apply_all():
            for card in self.cards:
                if not card.is_applied and card.callback:
                    card._on_click()

        def on_reset_all():
            for card in self.cards:
                if card.is_applied and card.undo_callback:
                    card._on_click()



        bottom = QHBoxLayout()
        apply_all = ModernButton("Apply All Safe", variant="primary")
        apply_all.setFixedWidth(160)
        apply_all.clicked.connect(on_apply_all)
        reset = ModernButton("Reset Defaults", variant="ghost")
        reset.setFixedWidth(140)
        reset.clicked.connect(on_reset_all)


        bottom.addStretch()
        bottom.addWidget(reset)
        bottom.addWidget(apply_all)
        layout.addLayout(bottom)