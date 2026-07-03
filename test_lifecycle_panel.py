import sys
from PySide6.QtWidgets import QApplication

from buster.ui.v9.panels.lifecycle_panel import LifecyclePanel


def main():
    app = QApplication(sys.argv)
    panel = LifecyclePanel()
    panel.resize(1000, 700)
    panel.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
