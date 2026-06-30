#!/usr/bin/env python3
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def assert_exists(path: str):
    p = ROOT / path
    assert p.exists(), f"Missing: {path}"


def main():
    required = [
        "buster/collaboration/__init__.py",
        "buster/collaboration/agent_state.py",
        "buster/collaboration/activity_feed.py",
        "buster/collaboration/conversation.py",
        "buster/collaboration/proactive_voice.py",
        "buster/collaboration/engine.py",
        "buster/collaboration/event_bridge.py",
        "buster/workspace/collaboration_dashboard.py",
        "buster/ui/widgets/agent_collaboration_widget.py",
        "buster/brain/planner/collaboration_planner_bridge.py",
        "data/proactive_voice_settings.json",
    ]
    for path in required:
        assert_exists(path)

    from buster.collaboration.engine import CollaborativeAgentEngine
    from buster.collaboration.agent_state import AgentStatus
    from buster.collaboration.event_bridge import CollaborationEventBridge
    from buster.workspace.collaboration_dashboard import CollaborationDashboard
    from buster.ui.widgets.agent_collaboration_widget import AgentCollaborationWidgetModel
    from buster.brain.planner.collaboration_planner_bridge import CollaborationPlannerBridge

    engine = CollaborativeAgentEngine()
    event = engine.set_agent_state(
        "Builder",
        AgentStatus.BUILDING,
        "Builder is generating project structure.",
        confidence=0.91,
        risk="low",
        mission_id="test",
        talk=True,
    )
    assert event["agent"] == "Builder"
    assert event["status"] == AgentStatus.BUILDING

    bridge = CollaborationEventBridge(engine)
    bridged = bridge.handle_event({
        "type": "tests_failed",
        "payload": {
            "message": "Tester found one failure.",
            "confidence": 0.72,
            "risk": "medium",
            "mission_id": "test",
            "talk": True,
        }
    })
    assert bridged is not None
    assert bridged["agent"] == "Tester"

    planner = CollaborationPlannerBridge(engine)
    plan_event = planner.announce_plan("Build Android app", confidence=0.88, risk="medium")
    assert plan_event["agent"] == "Planner"

    story = engine.mission_story_demo("story-test")
    assert len(story) >= 5

    snapshot = CollaborationDashboard(engine).snapshot()
    model = AgentCollaborationWidgetModel().render_model(snapshot)
    assert model["active_count"] >= 1
    assert "conversation" in model
    assert "voice_queue" in model

    pending = engine.voice.pending()
    assert pending, "Expected proactive voice messages to be queued"

    print("SUCCESS: v4.3 Collaborative Agent System tests passed")


if __name__ == "__main__":
    main()
