from pathlib import Path
import tempfile

from buster.intent_os import MissionIntentRuntime, IntentActivityEngine, ActivitySignal
from buster.ui.widgets.intent_widget import IntentWidgetModel


def test_intent_engine_infers_android_esp32():
    with tempfile.TemporaryDirectory() as td:
        engine = IntentActivityEngine(data_dir=td)
        engine.add_signal(ActivitySignal(source="test", type="app.active", summary="Android Studio is active"))
        engine.add_signal(ActivitySignal(source="test", type="hardware.esp32", summary="ESP32 device detected"))
        hypothesis = engine.infer()
        assert hypothesis.intent == "hardware_android_development"
        assert hypothesis.confidence >= 0.9
        assert "prepare build/test agents" in hypothesis.recommended_actions


def test_mission_intent_runtime_speaks_with_companion_policy():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "platformio.ini").write_text("[env]\n", encoding="utf-8")

        runtime = MissionIntentRuntime(data_dir=root / "data", mode="companion")
        runtime.start()
        result = runtime.process_workspace({
            "apps": ["Android Studio"],
            "devices": ["ESP32 USB serial"],
            "project_path": str(root),
        })

        assert result["hypothesis"]["intent"] == "hardware_android_development"
        assert result["speech"] is not None
        assert "Android" in result["speech"]["message"]


def test_intent_widget_model():
    with tempfile.TemporaryDirectory() as td:
        widget = IntentWidgetModel(data_dir=td)
        data = widget.data()
        assert data["title"] == "Intent Intelligence"
        assert "policy" in data
