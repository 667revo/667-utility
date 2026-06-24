from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                                QScrollArea, QFrame, QLineEdit)
from PySide6.QtCore import QThread, Signal
from src.ui.views.modern_button import ModernButton
from src.ui.theme import Colors
from core.uninstaller import get_installed_programs, uninstall_program, remove_bloatware


class WorkerThread(QThread):
    finished = Signal(bool)

    def __init__(self, fn, *args):
        super().__init__()
        self.fn = fn
        self.args = args

    def run(self):
        try:
            result = self.fn(*self.args)
            self.finished.emit(bool(result))
        except Exception as e:
            print(f"Error: {e}")
            self.finished.emit(False)


class ProgramRow(QFrame):
    def __init__(self, name: str, uninstall_str: str, parent=None):
        super().__init__(parent)
        self.name = name
        self.uninstall_str = uninstall_str
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)

        name_label = QLabel(self.name)
        name_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-size: 13px;")

        self.btn = ModernButton("Uninstall", variant="danger")
        self.btn.setFixedWidth(100)
        self.btn.clicked.connect(self._on_uninstall)

        layout.addWidget(name_label, stretch=1)
        layout.addWidget(self.btn)

    def _on_uninstall(self):
        self.btn.setEnabled(False)
        self.btn.setText("Removing...")
        self.worker = WorkerThread(uninstall_program, self.uninstall_str)
        self.worker.finished.connect(self._on_done)
        self.worker.start()

    def _on_done(self, success):
        if success:
            self.btn.setText("Done")
        else:
            self.btn.setEnabled(True)
            self.btn.setText("Failed")

    def _apply_style(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_2};
                border: 1px solid {Colors.BORDER};
                border-radius: 8px;
            }}
            QFrame:hover {{
                border: 1px solid {Colors.ACCENT};
            }}
        """)


class UninstallerView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("UninstallerView")
        self.all_programs = []
        self.rows = []
        self._build_ui()
        self._load_programs()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        # Başlık
        title = QLabel("Uninstall Tool")
        title.setObjectName("PageTitle")
        subtitle = QLabel("Uninstall selected programs from your computer")
        subtitle.setObjectName("PageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Bloatware butonu
        self.bloat_btn = ModernButton("Remove Windows Bloatware (include MSEdge)", variant="danger")
        self.bloat_btn.setFixedHeight(44)
        self.bloat_btn.clicked.connect(self._on_remove_bloatware)
        layout.addWidget(self.bloat_btn)

        # Arama
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search programs...")
        self.search.setStyleSheet(f"""
            QLineEdit {{
                background: {Colors.BG_2};
                border: 1px solid {Colors.BORDER};
                border-radius: 8px;
                padding: 8px 12px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border: 1px solid {Colors.ACCENT};
            }}
        """)
        self.search.textChanged.connect(self._filter)
        layout.addWidget(self.search)

        # Liste
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        self.list_widget = QWidget()
        self.list_widget.setStyleSheet("background: transparent;")
        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_layout.setSpacing(6)
        self.list_layout.setContentsMargins(0, 0, 0, 0)

        scroll.setWidget(self.list_widget)
        layout.addWidget(scroll)

    def _load_programs(self):
        self.all_programs = get_installed_programs()
        self._render(self.all_programs)

    def _render(self, programs):
        # Mevcut listeyi temizle
        for i in reversed(range(self.list_layout.count())):
            widget = self.list_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.rows = []

        for p in programs:
            row = ProgramRow(p["name"], p["uninstall_str"])
            self.list_layout.addWidget(row)
            self.rows.append(row)

        self.list_layout.addStretch()

    def _filter(self, text):
        filtered = [p for p in self.all_programs
                    if text.lower() in p["name"].lower()]
        self._render(filtered)

    def _on_remove_bloatware(self):
        self.bloat_btn.setEnabled(False)
        self.bloat_btn.setText("Removing bloatware...")
        self.worker = WorkerThread(remove_bloatware)
        self.worker.finished.connect(self._on_bloat_done)
        self.worker.start()

    def _on_bloat_done(self, success):
        self.bloat_btn.setText("Done!" if success else "Failed")