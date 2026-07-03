#!/usr/bin/env python3
from __future__ import annotations

import importlib
import json
from pathlib import Path

def assert_file(path: str) -> None:
    assert Path(path).exists(), f"Missing file: {path}"

def main() -> None:
    required = [
        "buster/intelligence/__init__.py",
        "buster/intelligence/confidence.py",
        "buster/intelligence/reasoning.py",
        "buster/intelligence/decision_tree.py",
        "buster/intelligence/strategy_selector.py",
        "buster/intelligence/risk_analysis.py",
        "buster/intelligence/scoring.py",
        "buster/core/event_bus.py",
        "buster/core/event_types.py",
        "buster/core/subscribers.py",
        "buster/workspace/mission_control.py",
        "data/intelligence_state.json",
        "data/event_history.json",
        "data/mission_control_state.json",
    ]
    for path in required:
        assert_file(path)

    reasoning_mod = importlib.import_module("buster.intelligence.reasoning")
    bus_mod = importlib.import_module("buster.core.event_bus")
    types_mod = importlib.import_module("buster.core.event_types")
    mc_mod = importlib.import_module("buster.workspace.mission_control")

    engine = reasoning_mod.ReasoningEngine()
    result = engine.reason("Build my Android app", {
        "tests_passed": True,
        "similar_success": True,
        "has_plugin": True,
    }).to_dict()

    assert result["strategy"]["name"] == "android_build_verify"
    assert result["confidence"]["score"] >= 0.85
    assert result["decision"] in {"auto_execute", "prepare_plan", "ask_user"}

    risky = engine.reason("delete and overwrite project", {"unknown_project": True}).to_dict()
    assert risky["risk"]["level"] in {"medium", "high", "blocked"}
    assert risky["confidence"]["should_ask_user"] is True

    bus = bus_mod.EventBus(history_path="data/event_history.json")
    captured = []
    def subscriber(event):
        captured.append(event.to_dict())

    bus.subscribe(types_mod.EventTypes.BUILD_COMPLETED, subscriber)
    bus.publish(types_mod.EventTypes.BUILD_COMPLETED, {"project": "test"}, source="test")

    assert captured, "Event subscriber did not capture event"
    assert captured[-1]["type"] == types_mod.EventTypes.BUILD_COMPLETED

    mission = mc_mod.MissionControl("data/mission_control_state.json")
    state = mission.update_from_reasoning(result)
    assert state["confidence"] == result["confidence"]["score"]
    assert "MISSION CONTROL" in mission.summary()

    for path in ["data/intelligence_state.json", "data/event_history.json", "data/mission_control_state.json"]:
        json.loads(Path(path).read_text(encoding="utf-8"))

    print("SUCCESS: v3.7 Intelligence Core + Event Bus tests passed")

if __name__ == "__main__":
    main()
