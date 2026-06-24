from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt


class ModernButton(QPushButton):
    def __init__(self, text, variant="primary", parent=None):
        super().__init__(text, parent)
        self.variant = variant
        self._apply_style()
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(38)

    def _apply_style(self):
        if self.variant == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #A855F7,
                        stop:1 #7C3AED
                    );
                    color: white;
                    border: none;
                    border-radius: 9px;
                    padding: 0 20px;
                    font-weight: 600;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #C084FC,
                        stop:1 #A855F7
                    );
                }
                QPushButton:pressed {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #7C3AED,
                        stop:1 #6D28D9
                    );
                }
            """)

        elif self.variant == "danger":
            self.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #F87171;
                    border: 1px solid rgba(248, 113, 113, 0.5);
                    border-radius: 9px;
                    padding: 0 20px;
                    font-weight: 600;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background: rgba(248, 113, 113, 0.1);
                    border: 1px solid rgba(248, 113, 113, 0.8);
                    color: #FCA5A5;
                }
                QPushButton:pressed {
                    background: rgba(248, 113, 113, 0.2);
                }
            """)

        elif self.variant == "ghost":
            self.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: rgba(180, 160, 220, 0.7);
                    border: 1px solid rgba(167, 139, 250, 0.18);
                    border-radius: 9px;
                    padding: 0 20px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background: rgba(168, 85, 247, 0.1);
                    color: #F0E8FF;
                    border: 1px solid rgba(168, 85, 247, 0.4);
                }
                QPushButton:pressed {
                    background: rgba(168, 85, 247, 0.18);
                }
            """)