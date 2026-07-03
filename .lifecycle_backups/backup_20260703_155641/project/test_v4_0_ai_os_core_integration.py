from pathlib import Path
import tempfile

from buster.ai_os import BusterAIOS
from buster.ai_os.planning_pipeline import PlanningPipeline
from buster.workspace.ai_os_unified import UnifiedAIOSWorkspace


def test_pipeline_build_plan():
    pipe = PlanningPipeline()
    plan = pipe.make_plan("build my Android app")
    assert plan["intent"] == "build"
    assert "builder" in [x.lower() for x in plan["strategy"]]
    assert "Builder" in plan["agents"]


def test_aios_status_written():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "data").mkdir()
        aios = BusterAIOS(root=root)
        plan = aios.think("fix this Python crash")
        status = aios.status()
        assert plan["intent"] == "fix"
        assert status["current_mission"] == "fix this Python crash"
        assert (root / "data" / "ai_os_status.json").exists()
        assert (root / "data" / "mission_control_unified.json").exists()


def test_workspace_wrapper():
    with tempfile.TemporaryDirectory() as d:
        ws = UnifiedAIOSWorkspace(root=Path(d))
        plan = ws.submit_command("index repository")
        assert plan["intent"] == "repository"
        assert ws.get_status()["online"] is True


if __name__ == "__main__":
    test_pipeline_build_plan()
    test_aios_status_written()
    test_workspace_wrapper()
    print("SUCCESS: v4.0 AI OS Core Integration tests passed")
