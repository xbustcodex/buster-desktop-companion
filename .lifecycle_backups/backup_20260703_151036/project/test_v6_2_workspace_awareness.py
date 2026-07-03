from pathlib import Path
import tempfile
import subprocess

from buster.workspace_awareness import WorkspaceAwarenessRuntime
from buster.ui.widgets.workspace_awareness_widget import WorkspaceAwarenessWidgetModel


def test_workspace_awareness_detects_apps_devices_and_project():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "requirements.txt").write_text("pytest\n", encoding="utf-8")

        runtime = WorkspaceAwarenessRuntime(data_dir=root / "data")
        runtime.start()
        result = runtime.scan({
            "apps": ["Android Studio", "Code.exe"],
            "devices": ["ESP32 USB serial", "Pixel adb"],
            "project_path": str(root),
        })

        summaries = " ".join(e["summary"] for e in result["events"])
        messages = " ".join(m["message"] for m in result["companion_messages"])

        assert "Android Studio" in summaries
        assert "ESP32" in summaries
        assert "Python project" in summaries
        assert "Android Studio" in messages
        assert "ESP32" in messages


def test_workspace_awareness_git_changes():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        subprocess.run(["git", "init"], cwd=root, capture_output=True, text=True)
        (root / "README.md").write_text("hello\n", encoding="utf-8")

        runtime = WorkspaceAwarenessRuntime(data_dir=root / "data")
        runtime.start()
        result = runtime.scan({"project_path": str(root)})

        assert any(e["type"] == "git.changed" for e in result["events"])


def test_workspace_awareness_widget():
    with tempfile.TemporaryDirectory() as td:
        widget = WorkspaceAwarenessWidgetModel(data_dir=td)
        data = widget.data()
        assert data["title"] == "Workspace Awareness"
        assert "event_count" in data
