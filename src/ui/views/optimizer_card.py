from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel,QGraphicsDropShadowEffect
from src.ui.views.modern_button import ModernButton
from PySide6.QtGui import QColor
from src.ui.theme import Colors
from typing import Callable
import subprocess

class OptimizerCard(QFrame):
    def __init__(self, title, description, status="safe", callback: Callable | None = None, parent=None):
        super().__init__(parent)
        self.setObjectName("OptimizerCard")
        self.callback = callback
        self._build_ui(title, description, status)
        self._apply_style()
        self._add_shadow()

    def _build_ui(self, title, description, status):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)

        # Sol: status indicator (renkli çizgi)
        indicator = QFrame()
        indicator.setFixedWidth(3)
        indicator.setFixedHeight(40)

        # Orta: metin
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: 600; font-size: 14px;")

        desc_label = QLabel(description)
        desc_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 12px;")
        desc_label.setWordWrap(True)

        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)

        # Sağ: buton
        btn_text = "Apply" if status != "danger" else "Apply Risk"
        btn_variant = "primary" if status == "safe" else "danger"
        action_btn = ModernButton(btn_text, variant=btn_variant)
        action_btn.setFixedWidth(110)
        action_btn.clicked.connect(self._on_click)

        layout.addWidget(indicator)
        layout.addLayout(text_layout, stretch=1)
        layout.addWidget(action_btn)

    def _on_click(self): 
        if self.callback:
            self.callback()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QFrame#OptimizerCard {{
                background-color: {Colors.BG_2};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
            }}
            QFrame#OptimizerCard:hover {{
                border: 1px solid {Colors.ACCENT};
                background-color: {Colors.BG_TERTIARY};
            }}
        """)

    def _add_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)