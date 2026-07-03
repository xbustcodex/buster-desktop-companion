#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def assert_file(path: str) -> None:
    if not Path(path).exists():
        raise AssertionError(f"Missing file: {path}")


def main() -> None:
    required = [
        "buster/living/__init__.py",
        "buster/living/state.py",
        "buster/living/timeline.py",
        "buster/living/notifications.py",
        "buster/living/face_controller.py",
        "buster/living/voice_vision_bridge.py",
        "buster/living/engine.py",
        "buster/living/dashboard.py",
        "buster/workspace/mission_activity.py",
        "buster/ui/widgets/living_os_widget.py",
        "buster/brain/planner/living_planner_bridge.py",
        "data/living_os_state.json",
        "data/mission_timeline_live.json",
        "data/decision_notifications.json",
        "data/voice_vision_state.json",
    ]
    for item in required:
        assert_file(item)

    from buster.living.engine import LivingOSEngine
    from buster.living.dashboard import LivingDashboard
    from buster.workspace.mission_activity import MissionActivityRecorder
    from buster.ui.widgets.living_os_widget import LivingOSWidgetModel
    from buster.brain.planner.living_planner_bridge import LivingPlannerBridge

    engine = LivingOSEngine()
    state = engine.set_mission("Test Jarvis mission", confidence=0.93, risk="low", reason="Test planner decision.")
    assert state["current_mission"] == "Test Jarvis mission"
    assert state["face"]["expression"] in {"happy", "focused", "thinking"}

    engine.voice_heard("Buster, check the project")
    engine.vision_seen("workspace is visible")
    engine.agent_update("Builder", "generated code")
    engine.success("approved build")

    dashboard = LivingDashboard()
    lines = dashboard.timeline_lines(5)
    assert lines, "Timeline lines should not be empty"

    recorder = MissionActivityRecorder()
    recorder.planner_created_mission("Example build", 0.91, "low")
    recorder.repository_indexed("example_project")
    recorder.builder_generated_code("main.py")
    recorder.tester_found_failure(1)
    recorder.fixer_repaired_issue("import error")
    recorder.verifier_approved_build()
    recorder.learning_recorded_pattern("safe import guard")
    recorder.experience_updated_skill("Python", 0.2)

    widget = LivingOSWidgetModel().get_view_model()
    assert "timeline" in widget
    assert "face" in widget
    assert widget["title"] == "Buster Living OS"

    bridge = LivingPlannerBridge()
    bridged = bridge.publish_plan({
        "mission": "Bridge test",
        "confidence": 0.88,
        "risk": "low",
        "reason": "Bridge integration test.",
    })
    assert bridged["current_mission"] == "Bridge test"

    state_data = json.loads(Path("data/living_os_state.json").read_text(encoding="utf-8"))
    assert "face" in state_data
    assert "recent_activity" in state_data

    print("SUCCESS: v4.1 Voice + Vision Living OS tests passed")


if __name__ == "__main__":
    main()
