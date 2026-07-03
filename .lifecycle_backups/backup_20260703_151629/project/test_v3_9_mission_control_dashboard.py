from pathlib import Path
import json


def assert_exists(path):
    assert Path(path).exists(), f"Missing: {path}"


def main():
    required = [
        "buster/workspace/mission_status.py",
        "buster/workspace/mission_metrics.py",
        "buster/workspace/mission_control_dashboard.py",
        "buster/ui/widgets/mission_control_widget.py",
        "buster/brain/planner/mission_planner.py",
        "BUSTER_AI_OS_ARCHITECTURE.md",
        "data/mission_control_dashboard.json",
        "data/mission_timeline.json",
        "data/ai_os_architecture_state.json",
    ]
    for p in required:
        assert_exists(p)

    from buster.workspace.mission_control_dashboard import MissionControlDashboard
    from buster.brain.planner.mission_planner import MissionPlanner

    dashboard = MissionControlDashboard(data_dir="data")
    dashboard.record_event("TEST", "Mission Control test event", "test")
    snap = dashboard.snapshot()

    assert snap["version"] == "3.9"
    assert snap["title"] == "Buster Mission Control"
    assert "status" in snap
    assert "metrics" in snap
    assert snap["health"] in ("GOOD", "WATCH", "CAUTION")

    text = dashboard.render_text()
    assert "BUSTER MISSION CONTROL" in text

    planner = MissionPlanner(data_dir="data")
    rec = planner.recommend("build project")
    assert "recommended_actions" in rec
    assert isinstance(rec["recommended_actions"], list)

    state = json.loads(Path("data/mission_control_dashboard.json").read_text(encoding="utf-8"))
    assert state.get("version") == "3.9"

    print("SUCCESS: v3.9 Mission Control Dashboard tests passed")


if __name__ == "__main__":
    main()
