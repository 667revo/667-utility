from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel,QGraphicsDropShadowEffect
from src.ui.views.modern_button import ModernButton
from PySide6.QtGui import QColor
from src.ui.theme import Colors
from typing import Callable
from PySide6.QtCore import QThread, Signal
import subprocess

class OptimizerWork(QThread):
    finished = Signal(bool)

    def __init__(self,callback):
        super().__init__()
        self.callback=callback

    def run(self):
        try:
            result = self.callback()
            self.finished.emit(True if result is None else bool(result))
        except Exception as e:
            print(f"Error: {e}")
            self.finished.emit(False)


class OptimizerCard(QFrame):
    def __init__(self, title, description, status="safe",
                 callback: Callable | None = None,
                 undo_callback: Callable | None = None,
                 parent=None):

        super().__init__(parent)
        self.setObjectName("OptimizerCard")
        self.callback = callback
        self.undo_callback = undo_callback
        self.is_applied = False
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
        self.action_btn = ModernButton(btn_text, variant=btn_variant)
        self.action_btn.setFixedWidth(110)
        self.action_btn.clicked.connect(self._on_click)

        layout.addWidget(indicator)
        layout.addLayout(text_layout, stretch=1)
        layout.addWidget(self.action_btn)

    def _on_click(self): 
        if not self.is_applied:
            if self.callback:
                self.worker = OptimizerWork(self.callback)
                self.worker.finished.connect(self._on_apply_done)
                self.action_btn.setEnabled(False)
                self.action_btn.setText("Running..")
                self.worker.start()
        else:
            if self.undo_callback:
                self.worker = OptimizerWork(self.undo_callback)
                self.worker.finished.connect(self._on_revert_done)
                self.action_btn.setEnabled(False)
                self.action_btn.setText("Running..")
                self.worker.start()

    def _on_apply_done(self, success):
        self.action_btn.setEnabled(True)
        if success:
            self.is_applied = True
            self.action_btn.setText("Revert")

        else:
            self.action_btn.setText("Apply")

    def _on_revert_done(self, success):
        self.action_btn.setEnabled(True)
        if success:
            self.is_applied = False
            self.action_btn.setText("Apply")
        else:
            self.action_btn.setText("Revert")

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