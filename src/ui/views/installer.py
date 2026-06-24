import json
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                                QHBoxLayout, QScrollArea, QFrame,
                                QCheckBox, QTabBar, QStackedWidget)
from PySide6.QtCore import QThread, Signal
from src.ui.views.modern_button import ModernButton
from src.ui.theme import Colors


def load_apps() -> dict:
    path = os.path.join(os.path.dirname(__file__), "..", "..", "apps.json")
    try:
        with open(os.path.abspath(path), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"apps.json yüklenemedi: {e}")
        return {}


class InstallWorker(QThread):
    progress = Signal(str)
    finished = Signal(bool, str)

    def __init__(self, winget_ids: list[str]):
        super().__init__()
        self.winget_ids = winget_ids

    def run(self):
        from core.installer import install_by_winget_id
        total = len(self.winget_ids)
        failed = []
        for i, winget_id in enumerate(self.winget_ids):
            self.progress.emit(f"Installing {winget_id} ({i+1}/{total})...")
            code, out = install_by_winget_id(winget_id)
            if code != 0:
                failed.append(winget_id)

        if failed:
            self.finished.emit(False, f"Failed: {', '.join(failed)}")
        else:
            self.finished.emit(True, f"{total} app(s) installed successfully.")


class SearchWorker(QThread):
    result = Signal(bool, str)

    def __init__(self, query: str):
        super().__init__()
        self.query = query

    def run(self):
        try:
            from core.search import search_first_package_id
            ok, res = search_first_package_id(self.query)
            self.result.emit(ok, res)
        except Exception as e:
            self.result.emit(False, str(e))


class AppCheckBox(QFrame):
    def __init__(self, name: str, winget_id: str, parent=None):
        super().__init__(parent)
        self.winget_id = winget_id
        self._build_ui(name, winget_id)
        self._apply_style()

    def _build_ui(self, name, winget_id):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)

        self.checkbox = QCheckBox()
        self.checkbox.setStyleSheet(f"""
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 5px;
                border: 1px solid {Colors.BORDER};
                background: transparent;
            }}
            QCheckBox::indicator:checked {{
                background: {Colors.ACCENT};
                border: 1px solid {Colors.ACCENT};
            }}
        """)

        name_label = QLabel(name)
        name_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-size: 13px;")

        id_label = QLabel(winget_id)
        id_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 11px;")

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        text_layout.addWidget(name_label)
        text_layout.addWidget(id_label)

        layout.addWidget(self.checkbox)
        layout.addLayout(text_layout, stretch=1)

    def is_checked(self) -> bool:
        return self.checkbox.isChecked()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QFrame {{
                background: {Colors.BG_2};
                border: 1px solid {Colors.BORDER};
                border-radius: 8px;
            }}
            QFrame:hover {{
                border: 1px solid {Colors.ACCENT};
            }}
        """)


class CategoryTab(QWidget):
    def __init__(self, apps: dict, parent=None):
        super().__init__(parent)
        self.app_rows: list[AppCheckBox] = []
        self._build_ui(apps)

    def _build_ui(self, apps):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(6)

        for name, winget_id in apps.items():
            row = AppCheckBox(name, winget_id)
            self.app_rows.append(row)
            layout.addWidget(row)

        layout.addStretch()

    def get_selected(self) -> list[str]:
        return [row.winget_id for row in self.app_rows if row.is_checked()]


class InstallerView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("InstallerView")
        self.worker = None
        self.search_worker = None
        self.category_tabs: list[CategoryTab] = []
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        # Başlık
        title = QLabel("Install Apps")
        title.setObjectName("PageTitle")
        subtitle = QLabel("Select apps to install via winget")
        subtitle.setObjectName("PageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Arama
        search_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search winget packages (e.g. 7zip, chrome)...")
        self.search_btn = ModernButton("Search", variant="ghost")
        self.search_btn.setFixedWidth(90)
        self.search_btn.clicked.connect(self._handle_search)
        search_row.addWidget(self.search_input)
        search_row.addWidget(self.search_btn)
        layout.addLayout(search_row)

        # Arama sonucu
        self.search_result = QLabel("")
        self.search_result.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 12px;")
        layout.addWidget(self.search_result)

        # Kategorili tab bar
        self.tab_bar = QTabBar()
        self.tab_bar.setStyleSheet(f"""
            QTabBar::tab {{
                background: transparent;
                color: {Colors.TEXT_SECONDARY};
                padding: 8px 18px;
                border: none;
                font-size: 13px;
                border-bottom: 2px solid transparent;
            }}
            QTabBar::tab:selected {{
                color: {Colors.ACCENT};
                border-bottom: 2px solid {Colors.ACCENT};
            }}
            QTabBar::tab:hover {{
                color: {Colors.TEXT_PRIMARY};
            }}
        """)
        self.tab_bar.currentChanged.connect(self._on_tab_changed)
        layout.addWidget(self.tab_bar)

        # Tab içerikleri
        self.stack = QStackedWidget()
        apps_data = load_apps()

        for category, apps in apps_data.items():
            self.tab_bar.addTab(category)
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setFrameShape(QFrame.NoFrame)
            scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

            tab = CategoryTab(apps)
            tab.setStyleSheet("background: transparent;")
            scroll.setWidget(tab)
            self.category_tabs.append(tab)
            self.stack.addWidget(scroll)

        layout.addWidget(self.stack)

        # Alt butonlar
        bottom = QHBoxLayout()
        self.status_label = QLabel("")
        self.status_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 12px;")

        self.install_btn = ModernButton("Install Selected", variant="primary")
        self.install_btn.setFixedWidth(150)
        self.install_btn.clicked.connect(self._handle_install)

        bottom.addWidget(self.status_label, stretch=1)
        bottom.addWidget(self.install_btn)
        layout.addLayout(bottom)

    def _on_tab_changed(self, index):
        self.stack.setCurrentIndex(index)

    def _handle_install(self):
        current_tab = self.category_tabs[self.tab_bar.currentIndex()]
        selected = current_tab.get_selected()

        if not selected:
            self.status_label.setText("No apps selected.")
            return

        self.install_btn.setEnabled(False)
        self.install_btn.setText("Installing...")
        self.status_label.setText(f"Starting installation of {len(selected)} app(s)...")

        self.worker = InstallWorker(selected)
        self.worker.progress.connect(self.status_label.setText)
        self.worker.finished.connect(self._on_install_done)
        self.worker.start()

    def _on_install_done(self, success, message):
        self.install_btn.setEnabled(True)
        self.install_btn.setText("Install Selected")
        self.status_label.setText(message)

    def _handle_search(self):
        query = self.search_input.text().strip()
        if not query:
            return
        self.search_btn.setEnabled(False)
        self.search_result.setText(f"Searching for '{query}'...")
        self.search_worker = SearchWorker(query)
        self.search_worker.result.connect(self._on_search_done)
        self.search_worker.start()

    def _on_search_done(self, ok, result):
        self.search_btn.setEnabled(True)
        if ok:
            self.search_result.setText(f"Found: {result} — you can install it directly via winget.")
        else:
            self.search_result.setText("Not found.")