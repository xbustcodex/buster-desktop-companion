from pathlib import Path


def test_imports():
    from buster.mind import MindEngine, AttentionSystem, WorkingMemory, GoalManager, CuriosityEngine, ReflectionCycle
    assert MindEngine
    assert AttentionSystem
    assert WorkingMemory
    assert GoalManager
    assert CuriosityEngine
    assert ReflectionCycle


def test_attention_working_memory_goal_flow():
    from buster.mind import MindEngine
    mind = MindEngine()
    event = mind.perceive(
        source="ears",
        kind="wake_word",
        title="Adam said Buster",
        details="Wake word detected by microphone",
        importance=0.9,
        urgency=0.85,
        confidence=0.95,
    )
    assert event["focused"] is True
    assert event["priority"] >= 0.72
    goal = mind.create_goal_from_focus()
    assert goal is not None
    assert goal["status"] == "active"
    thought = mind.think()
    assert thought["working_memory"]["active_items"] >= 1
    assert len(thought["active_goals"]) >= 1


def test_bridges_and_dashboard():
    from buster.perception.mind_bridge import PerceptionMindBridge
    from buster.brain.planner.mind_planner_bridge import MindPlannerBridge
    from buster.workspace.mind_dashboard import MindDashboard
    bridge = PerceptionMindBridge()
    result = bridge.submit_observation({
        "source": "camera",
        "kind": "user_returned",
        "title": "User returned to desk",
        "importance": 0.8,
        "urgency": 0.6,
        "confidence": 0.8,
    })
    assert "priority" in result
    planner = MindPlannerBridge()
    ctx = planner.prepare_planning_context()
    assert "working_memory" in ctx
    dash = MindDashboard().snapshot()
    assert dash["title"] == "Buster Mind"


def test_reflection_and_files_exist():
    from buster.mind import MindEngine
    reflection = MindEngine().reflect()
    assert reflection["title"] == "Daily reflection"
    for p in [
        "data/mind_state.json",
        "data/attention_focus.json",
        "data/attention_events.json",
        "data/working_memory.json",
        "data/goals.json",
        "data/reflection_journal.json",
    ]:
        assert Path(p).exists()


if __name__ == "__main__":
    test_imports()
    test_attention_working_memory_goal_flow()
    test_bridges_and_dashboard()
    test_reflection_and_files_exist()
    print("SUCCESS: v5.3 Buster Mind tests passed")
