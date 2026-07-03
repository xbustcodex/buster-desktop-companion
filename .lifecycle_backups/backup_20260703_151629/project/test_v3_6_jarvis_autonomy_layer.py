"""Buster v3.6 Jarvis Autonomy Layer test."""
from __future__ import annotations

from pathlib import Path
import tempfile


def make_engine(root: Path):
    from buster.autonomy import AutonomyEngine
    from buster.learning import LearningEngine
    from buster.plugins.registry import PluginRegistry

    learning = LearningEngine(
        memory_path=root / "learning_memory.json",
        strategies_path=root / "build_strategies.json",
        patterns_path=root / "design_patterns.json",
    )
    registry = PluginRegistry(root / "plugin_registry.json")
    registry.register(
        name="python_tools",
        module="buster.plugins.builtin.ollama_plugin",
        capabilities=["python", "desktop", "tests"],
    )
    return AutonomyEngine(
        state_path=root / "autonomy_state.json",
        history_path=root / "autonomy_history.json",
        learning=learning,
        registry=registry,
    )


def test_decide_next_action() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        engine = make_engine(root)
        decision = engine.decide_next_action(
            "Build a Python desktop timer app",
            project_type="python",
        )
        assert decision.recommended_action == "plan_build_test_fix_verify"
        assert decision.confidence > 0.7
        assert "python_tools" in decision.plugins


def test_job_completion_feeds_learning() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        engine = make_engine(root)
        engine.set_mode("assisted")
        job = engine.create_job(
            title="Build timer",
            request="Build a Python desktop timer app",
            project="timer_app",
            project_type="python",
        )
        status_before = engine.status()
        assert status_before["active_jobs"] == 1

        completed = engine.complete_job(
            job.job_id,
            success=True,
            result={
                "what_worked": ["Small UI module and immediate test run"],
                "reusable_patterns": ["Keep Tkinter callbacks separate from layout creation"],
            },
        )
        assert completed["status"] == "completed"
        status_after = engine.status()
        assert status_after["active_jobs"] == 0
        assert status_after["completed_jobs"] == 1
        assert status_after["learning"]["records"] == 1
        assert status_after["learning"]["patterns"] >= 1


def test_dashboard_and_autonomy_planner() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        engine = make_engine(root)

        from buster.autonomy.dashboard import AutonomyDashboard
        from buster.brain.planner.autonomy_planner import AutonomyPlanner

        planner = AutonomyPlanner(engine)
        plan = planner.plan_next("Fix the last error and verify it", project_type="python", context={"error_count": 1})
        assert plan["next_action"] == "fix_then_verify"
        assert plan["strategy"]

        dashboard = AutonomyDashboard(engine)
        snap = dashboard.snapshot()
        assert snap["title"] == "Jarvis Autonomy"
        assert snap["last_action"] == "fix_then_verify"


if __name__ == "__main__":
    test_decide_next_action()
    test_job_completion_feeds_learning()
    test_dashboard_and_autonomy_planner()
    print("SUCCESS: v3.6 Jarvis Autonomy Layer tests passed")
