from email import message

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame, QComboBox, QPushButton
from PySide6.QtCore import QThread, Slot, Signal


class InstallerView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("InstallerView")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title_label = QLabel("Install Apps")
        title_label.setObjectName("PageTitle")

        subtitle_label = QLabel("Install apps with winget module")
        subtitle_label.setObjectName("PageSubtitle")

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)

        self.app_combo = QComboBox()
        
        self.app_combo.addItems(["Microsoft.VisualStudioCode", "Google.Chrome", "7zip.7zip"])


        self.install_button = QPushButton("Install")
        self.status_label = QLabel("Ready")
        self.status_label.setWordWrap(True)

        layout.addWidget(self.app_combo)
        layout.addWidget(self.install_button)
        layout.addWidget(self.status_label)

        self.install_button.clicked.connect(self.handle_install)

    @Slot()

    def handle_install(self):

        selected_app = self.app_combo.currentText()

        if not selected_app:
            return
        

        self.install_button.setEnabled(False)
        self.status_label.setText(f"Starting installition for: {selected_app}..")


        self.worker = InstallitionWorker(selected_app)



        self.worker.progress.connect(self.update_status)
        self.worker.finished.connect(self.on_installation_finished)

        self.worker.start()

    @Slot(str)

    def update_status(self,message):
        self.status_label.setText(message)


    @Slot(bool)
    def on_installation_finished(self, success, message):
        self.install_button.setEnabled(True)

        if success:
            self.status_label.setText("Installation completed")

        else:

            self.status_label.setText(f"Installation failed:{message}")




class InstallerBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setObjectName("InstallerBox")


class InstallitionWorker(QThread):

    progress = Signal(str)
    finished = Signal(bool, str)

    def __init__(self, winget_id):
        super().__init__()
        self.winget_id = winget_id

    def run(self):
        try:
            from core.installer import install_by_winget_id

            exit_code, output = install_by_winget_id(self.winget_id)

            if exit_code == 0:
                self.finished.emit(True, "Installation completed successfully.")
            else:
                self.finished.emit(False, output)

        except Exception as e:
            self.finished.emit(False, str(e))