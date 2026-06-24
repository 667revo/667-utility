def get_stylesheet() -> str:
    return """
    QWidget {
        color: #F5F2FF;
        font-family: 'JetBrainsMono Nerd Font';
        font-size: 14px;
    }

    QMainWindow, #RootWidget {
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 #080614,
            stop:0.5 #0D0920,
            stop:1 #0A0618
        );
    }

    QScrollBar:vertical {
        background: transparent;
        width: 4px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(168, 85, 247, 0.6),
            stop:1 rgba(139, 92, 246, 0.3)
        );
        border-radius: 2px;
        min-height: 30px;
    }

    QScrollBar::handle:vertical:hover {
        background: rgba(168, 85, 247, 0.9);
    }

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical,
    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {
        background: transparent;
        height: 0px;
    }

    #Sidebar {
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(8, 4, 20, 0.98),
            stop:1 rgba(14, 8, 32, 0.92)
        );
        border: none;
        border-right: 1px solid rgba(168, 85, 247, 0.12);
        padding: 20px 8px;
        margin: 0px;
        outline: none;
    }

    QListWidget {
        background: transparent;
        border: none;
        outline: none;
    }

    QListWidget::item {
        border-radius: 10px;
        padding: 12px 18px;
        color: rgba(180, 160, 220, 0.6);
        margin: 2px 4px;
        font-size: 13px;
        border: 1px solid transparent;
    }

    QListWidget::item:hover {
        background: rgba(168, 85, 247, 0.08);
        color: rgba(220, 200, 255, 0.85);
        border: 1px solid rgba(168, 85, 247, 0.15);
    }

    QListWidget::item:selected {
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(168, 85, 247, 0.25),
            stop:1 rgba(139, 92, 246, 0.12)
        );
        border: 1px solid rgba(168, 85, 247, 0.4);
        color: #F0E8FF;
        font-weight: 600;
    }

    #PageTitle {
        font-size: 26px;
        font-weight: 700;
        color: #F5F2FF;
    }

    #PageSubtitle {
        font-size: 12px;
        color: rgba(157, 142, 196, 0.8);
        margin-bottom: 4px;
    }

    #SectionTitle {
        font-size: 14px;
        font-weight: 600;
        color: #E9DDFD;
        margin-top: 8px;
    }

    #StatCard {
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(22, 14, 44, 0.85),
            stop:1 rgba(14, 8, 30, 0.7)
        );
        border: 1px solid rgba(167, 139, 250, 0.14);
        border-radius: 16px;
        padding: 14px;
    }

    #StatCard:hover {
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(32, 20, 60, 0.92),
            stop:1 rgba(20, 12, 42, 0.85)
        );
        border: 1px solid rgba(168, 85, 247, 0.32);
    }

    #CardTitle {
        font-size: 11px;
        color: rgba(157, 142, 196, 0.7);
        font-weight: 500;
        letter-spacing: 0.8px;
    }

    #CardValue {
        font-size: 26px;
        font-weight: 700;
        color: #F5F2FF;
    }

    #ActionCard {
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(20, 13, 40, 0.8),
            stop:1 rgba(12, 7, 26, 0.65)
        );
        border: 1px solid rgba(167, 139, 250, 0.11);
        border-radius: 12px;
        padding: 12px;
    }

    #ActionCard:hover {
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(30, 18, 56, 0.88),
            stop:1 rgba(18, 10, 38, 0.78)
        );
        border: 1px solid rgba(168, 85, 247, 0.3);
    }

    #ActionTitle {
        font-size: 13px;
        font-weight: 600;
        color: #F5F2FF;
    }

    #ActionSubtitle {
        font-size: 11px;
        color: rgba(157, 142, 196, 0.75);
    }

    QLineEdit {
        background: rgba(14, 9, 30, 0.75);
        border: 1px solid rgba(167, 139, 250, 0.14);
        border-radius: 10px;
        padding: 10px 14px;
        color: #F5F2FF;
        font-size: 13px;
        selection-background-color: rgba(168, 85, 247, 0.4);
    }

    QLineEdit:focus {
        border: 1px solid rgba(168, 85, 247, 0.55);
        background: rgba(20, 12, 42, 0.9);
    }

    QComboBox {
        background: rgba(14, 9, 30, 0.75);
        border: 1px solid rgba(167, 139, 250, 0.14);
        border-radius: 10px;
        padding: 8px 14px;
        color: #F5F2FF;
        font-size: 13px;
    }

    QComboBox:hover {
        border: 1px solid rgba(168, 85, 247, 0.35);
    }

    QComboBox::drop-down {
        border: none;
        width: 20px;
    }

    QComboBox QAbstractItemView {
        background: #100B28;
        border: 1px solid rgba(168, 85, 247, 0.22);
        border-radius: 10px;
        color: #F5F2FF;
        selection-background-color: rgba(168, 85, 247, 0.25);
        padding: 4px;
        outline: none;
    }

    QLabel {
        background: transparent;
    }

    QFrame {
        background: transparent;
    }

    QTabBar::tab {
        background: transparent;
        color: rgba(157, 142, 196, 0.7);
        padding: 9px 22px;
        border: none;
        font-size: 13px;
        border-bottom: 2px solid transparent;
    }

    QTabBar::tab:selected {
        color: #C084FC;
        border-bottom: 2px solid #A855F7;
    }

    QTabBar::tab:hover {
        color: #D4C5F9;
        border-bottom: 2px solid rgba(168, 85, 247, 0.3);
    }

    QCheckBox {
        spacing: 8px;
        color: #D4C5F9;
        font-size: 13px;
    }

    QCheckBox::indicator {
        width: 17px;
        height: 17px;
        border-radius: 5px;
        border: 1px solid rgba(167, 139, 250, 0.28);
        background: rgba(14, 9, 30, 0.6);
    }

    QCheckBox::indicator:checked {
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 #A855F7,
            stop:1 #7C3AED
        );
        border: 1px solid #A855F7;
    }

    QCheckBox::indicator:hover {
        border: 1px solid rgba(168, 85, 247, 0.55);
    }

    QPushButton {
        border-radius: 9px;
        padding: 7px 18px;
        font-size: 13px;
        font-weight: 600;
    }
    """