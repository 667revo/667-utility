from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from src.ui.theme import Colors

class ModernButton(QPushButton):
    def __init__(self, text, variant="primary", parent=None):
        super().__init__(text, parent)
        self.variant = variant
        self._apply_style()
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(38)
 
    def _apply_style(self):
        if self.variant == "primary":
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colors.ACCENT};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 0 20px;
                    font-weight: 600;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    background-color: {Colors.ACCENT_HOVER};
                }}
                QPushButton:pressed {{
                    background-color: #5A52E0;
                }}
            """)
 
        elif self.variant == "danger":
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {Colors.DANGER};
                    border: 1px solid {Colors.DANGER};
                    border-radius: 8px;
                    padding: 0 20px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: rgba(248, 113, 113, 0.1);
                }}
            """)
 
        elif self.variant == "ghost":
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {Colors.TEXT_SECONDARY};
                    border: 1px solid {Colors.BORDER};
                    border-radius: 8px;
                    padding: 0 20px;
                }}
                QPushButton:hover {{
                    background-color: {Colors.BG_TERTIARY};
                    color: {Colors.TEXT_PRIMARY};
                }}
            """)
 