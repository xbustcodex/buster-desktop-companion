from pathlib import Path

ROOT = Path.cwd()

files = {
    "buster/services/lifecycle_service.py": r'''import json
from pathlib import Path

from buster.lifecycle.manager import LifecycleManager


class LifecycleService:
    def __init__(self, root=None):
        self.root = Path(root or Path.cwd()).resolve()
        self.manager = LifecycleManager(self.root)

    def status(self):
        return self.manager.status()

    def health(self):
        return self.manager.run_health()

    def verify(self):
        return self.manager.verify()

    def plan(self):
        return self.manager.plan()

    def backup(self):
        return {"backup_path": self.manager.backup()}

    def rollback(self):
        return {"success": self.manager.rollback()}

    def snapshot(self):
        status = self.status()
        health = self.health()
        verify = self.verify()
        plan = self.plan()

        return {
            "status": status,
            "health": health,
            "verify": verify,
            "plan": plan,
        }
''',

    "buster/services/__init__.py": r'''from .lifecycle_service import LifecycleService
''',

    "buster/ui/v9/panels/lifecycle_panel.py": r'''from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QTextEdit,
)

from buster.services.lifecycle_service import LifecycleService


class LifecyclePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.service = LifecycleService()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Lifecycle Manager")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        self.summary = QLabel("Loading lifecycle status...")
        self.summary.setWordWrap(True)
        self.summary.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.summary)

        button_row = QHBoxLayout()

        self.scan_btn = QPushButton("Refresh")
        self.verify_btn = QPushButton("Verify")
        self.backup_btn = QPushButton("Backup")
        self.health_btn = QPushButton("Health")
        self.plan_btn = QPushButton("Plan")
        self.rollback_btn = QPushButton("Rollback")

        for btn in [
            self.scan_btn,
            self.verify_btn,
            self.backup_btn,
            self.health_btn,
            self.plan_btn,
            self.rollback_btn,
        ]:
            button_row.addWidget(btn)

        layout.addLayout(button_row)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Lifecycle output will appear here...")
        layout.addWidget(self.output, 1)

        self.scan_btn.clicked.connect(self.refresh)
        self.verify_btn.clicked.connect(self.verify)
        self.backup_btn.clicked.connect(self.backup)
        self.health_btn.clicked.connect(self.health)
        self.plan_btn.clicked.connect(self.plan)
        self.rollback_btn.clicked.connect(self.rollback)

        self.refresh()

    def _pretty(self, data):
        import json
        return json.dumps(data, indent=4)

    def refresh(self):
        data = self.service.snapshot()

        status = data.get("status", {})
        health = data.get("health", {})
        verify = data.get("verify", {})

        self.summary.setText(
            f"Version: {status.get('version', 'unknown')}  |  "
            f"Files: {status.get('files', 0)}  |  "
            f"Size: {round(status.get('size', 0) / 1024 / 1024, 2)} MB  |  "
            f"Backups: {status.get('backups', 0)}  |  "
            f"Health: {health.get('overall_score', 0)}%  |  "
            f"Verify: {'PASS' if verify.get('passed') else 'CHECK'}"
        )

        self.output.setPlainText(self._pretty(data))

    def verify(self):
        self.output.setPlainText(self._pretty(self.service.verify()))

    def backup(self):
        self.output.setPlainText(self._pretty(self.service.backup()))
        self.refresh()

    def health(self):
        self.output.setPlainText(self._pretty(self.service.health()))

    def plan(self):
        self.output.setPlainText(self._pretty(self.service.plan()))

    def rollback(self):
        self.output.setPlainText(self._pretty(self.service.rollback()))
        self.refresh()
''',

    "test_lifecycle_panel.py": r'''import sys
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
'''
}

for rel, content in files.items():
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"created/updated: {rel}")

print()
print("Lifecycle Mission Control integration added.")
print()
print("Test standalone panel:")
print("  python test_lifecycle_panel.py")
print()
print("CLI still works:")
print("  python run_lifecycle.py status")
print("  python run_lifecycle.py health")