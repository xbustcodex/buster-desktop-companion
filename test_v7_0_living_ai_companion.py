import tempfile
from pathlib import Path

from buster.living_companion import LivingAICompanionRuntime, VoiceRuntime, DailyRhythm
from buster.skills import SkillGrowthEngine
from buster.ui.widgets.living_companion_widget import LivingCompanionWidgetModel


def test_voice_runtime_queue_and_drain():
    with tempfile.TemporaryDirectory() as td:
        voice = VoiceRuntime(data_dir=td)
        voice.enqueue("Good morning Adam.", reason="test")
        spoken = voice.drain()
        assert spoken[0]["message"] == "Good morning Adam."


def test_skill_growth_engine_records_events():
    with tempfile.TemporaryDirectory() as td:
        engine = SkillGrowthEngine(data_dir=td)
        result = engine.record_event({"type": "android", "summary": "Android build completed"}, success=True)
        assert result["name"] == "android_build"
        assert result["level"]["successes"] == 1


def test_living_companion_start_context_and_mission():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "platformio.ini").write_text("[env]\n", encoding="utf-8")
        companion = LivingAICompanionRuntime(data_dir=root / "data")
        start = companion.start_day("Adam")
        assert any("Good morning" in m["message"] or "Good afternoon" in m["message"] or "Good evening" in m["message"] for m in start["voice"]["spoken"])

        context = companion.handle_workspace_context({
            "apps": ["Android Studio"],
            "devices": ["ESP32 USB serial"],
            "project_path": str(root),
        })
        assert context["intent"]["intent"] == "hardware_android_development"

        mission = companion.run_development_mission("Build Android ESP32 workflow", intent="hardware_android_development")
        assert mission["mission"]["status"] == "completed"
        assert mission["skills"]["skills"]


def test_living_companion_widget():
    with tempfile.TemporaryDirectory() as td:
        widget = LivingCompanionWidgetModel(data_dir=td)
        data = widget.data()
        assert data["title"] == "Living AI Companion"
        assert "skill_count" in data
