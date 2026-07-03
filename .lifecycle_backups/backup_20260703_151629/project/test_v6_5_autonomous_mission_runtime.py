import tempfile

from buster.mission_runtime import AutonomousMissionRuntime, CapabilityRegistry
from buster.ui.widgets.autonomous_mission_widget import AutonomousMissionWidgetModel


def test_capability_registry_defaults():
    registry = CapabilityRegistry()
    registry.install_defaults()
    assert registry.provider_for("build.compile") == "builder"
    assert registry.provider_for("test.run") == "tester"
    assert registry.provider_for("learning.record") == "learning"


def test_autonomous_development_mission_runs_to_completion():
    with tempfile.TemporaryDirectory() as td:
        runtime = AutonomousMissionRuntime(data_dir=td)
        result = runtime.run_development_mission("Build Android app", intent="android_development")
        assert result["status"] == "completed"
        assert len(result["steps"]) >= 8
        assert all(step["status"] == "completed" for step in result["steps"])

        messages = " ".join(m["message"] for m in runtime.status()["companion"]["messages"])
        assert "Builder Agent finished compiling" in messages
        assert "recorded a new build strategy" in messages


def test_autonomous_mission_widget_model():
    with tempfile.TemporaryDirectory() as td:
        widget = AutonomousMissionWidgetModel(data_dir=td)
        data = widget.data()
        assert data["title"] == "Autonomous Mission Runtime"
        assert "capability_count" in data
