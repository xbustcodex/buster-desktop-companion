import tempfile
from buster.multi_agent import MultiAgentCollaborationRuntime, DelegationPlanner, CollaborationBlackboard, AgentNegotiator
from buster.ui.widgets.multi_agent_widget import MultiAgentWidgetModel

def test_delegation_and_negotiation():
    planner = DelegationPlanner()
    plan = planner.plan("fix regression in Android build", intent="debugging_tests")
    assert "tester" in plan["agents"]
    assert "fixer" in plan["agents"]
    board = CollaborationBlackboard()
    negotiator = AgentNegotiator(board)
    result = negotiator.negotiate("fix regression failure", ["builder", "tester", "fixer"])
    assert result["decision"]["chosen_agent"] in {"tester", "fixer"}
    assert board.status()["decisions"]

def test_multi_agent_runtime_mission():
    with tempfile.TemporaryDirectory() as td:
        runtime = MultiAgentCollaborationRuntime(data_dir=td)
        result = runtime.run_mission("fix regression in Android ESP32 workflow", intent="debugging_tests")
        timeline_text = " ".join(str(item) for item in result["blackboard"]["timeline"])
        messages = " ".join(m["message"] for m in result["companion"]["messages"])
        assert "Tester" in timeline_text
        assert "Fixer" in timeline_text
        assert "Learning" in timeline_text
        assert "regression" in messages
        assert "teamwork strategy" in messages

def test_multi_agent_widget_model():
    with tempfile.TemporaryDirectory() as td:
        widget = MultiAgentWidgetModel(data_dir=td)
        data = widget.data()
        assert data["title"] == "Multi-Agent Collaboration"
        assert "timeline" in data
