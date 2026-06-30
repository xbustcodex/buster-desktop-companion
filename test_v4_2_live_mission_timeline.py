#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json

def assert_file(path: str) -> None:
    if not Path(path).exists():
        raise AssertionError(f"Missing file: {path}")

def main() -> None:
    required = [
        "buster/living/mission_events.py",
        "buster/living/live_timeline.py",
        "buster/living/event_bridge.py",
        "buster/workspace/live_mission_timeline.py",
        "buster/ui/widgets/live_mission_timeline_widget.py",
        "buster/brain/planner/timeline_planner_bridge.py",
        "data/live_mission_timeline_state.json",
        "data/mission_timeline_live.json",
    ]
    for item in required:
        assert_file(item)
    from buster.living.live_timeline import LiveMissionTimeline
    from buster.living.event_bridge import MissionTimelineEventBridge
    from buster.living.mission_events import MissionEventType
    from buster.workspace.live_mission_timeline import LiveMissionTimelineView
    from buster.ui.widgets.live_mission_timeline_widget import LiveMissionTimelineWidgetModel
    from buster.brain.planner.timeline_planner_bridge import TimelinePlannerBridge
    timeline = LiveMissionTimeline()
    timeline.clear()
    event = timeline.record(MissionEventType.PLANNER_CREATED_MISSION, "created mission: Test build", confidence=0.95, risk="low")
    assert event["source"] == "Planner"
    assert "Test build" in timeline.lines(1)[0]
    assert "confidence 95%" in timeline.lines(1)[0]
    bridge = MissionTimelineEventBridge(timeline)
    bridge.handle({"type": MissionEventType.REPOSITORY_INDEXED, "payload": {"message": "indexed project: demo"}})
    bridge.handle({"type": MissionEventType.BUILDER_GENERATED_CODE, "payload": {"message": "generated code: main.py", "confidence": 0.88, "risk": "low"}})
    bridge.handle({"type": MissionEventType.TESTER_FOUND_FAILURE, "payload": {"message": "found 1 failure", "risk": "medium", "level": "warning"}})
    bridge.handle({"type": MissionEventType.FIXER_REPAIRED_ISSUE, "payload": {"message": "repaired issue", "confidence": 0.82}})
    bridge.handle({"type": MissionEventType.VERIFIER_APPROVED_BUILD, "payload": {"message": "approved build"}})
    bridge.handle({"type": MissionEventType.LEARNING_RECORDED_PATTERN, "payload": {"message": "recorded new pattern"}})
    bridge.handle({"type": MissionEventType.EXPERIENCE_UPDATED_SKILL, "payload": {"message": "updated Python skill (+0.2%)"}})
    recent = timeline.recent(10)
    assert len(recent) >= 8
    assert any(e["source"] == "Tester" for e in recent)
    assert any("Python skill" in e["message"] for e in recent)
    view = LiveMissionTimelineView().get_view_model()
    assert view["title"] == "Live Mission Timeline"
    assert view["lines"]
    widget = LiveMissionTimelineWidgetModel().get_view_model()
    assert "empty_message" in widget
    assert "events" in widget
    planner = TimelinePlannerBridge()
    planner.mission_created("Planner bridge build", 0.91, "low", "test")
    planner.agent_step("Builder", "generated code", 0.89, "low")
    assert any("Planner bridge build" in line for line in timeline.lines(10))
    data = json.loads(Path("data/mission_timeline_live.json").read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert data
    print("SUCCESS: v4.2 Live Mission Timeline tests passed")

if __name__ == "__main__":
    main()
