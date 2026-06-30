"""Buster v3.5 Learning + Plugin OS test."""
from __future__ import annotations

from pathlib import Path
import tempfile


def test_learning_engine_roundtrip() -> None:
    from buster.learning import LearningEngine

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        engine = LearningEngine(
            memory_path=root / "learning_memory.json",
            strategies_path=root / "build_strategies.json",
            patterns_path=root / "design_patterns.json",
        )

        engine.learn_from_job(
            task="Build Tkinter calculator",
            project="python",
            success=True,
            strategy="plan_build_test_fix_verify",
            what_worked=["Small files and immediate test run"],
            reusable_patterns=["For Tkinter apps, isolate UI creation from command callbacks."],
            tags=["tkinter", "gui"],
        )

        summary = engine.summary()
        assert summary["records"] == 1
        assert summary["successes"] == 1
        assert summary["patterns"] == 1

        rec = engine.recommend_strategy("python", "tkinter calculator")
        assert "strategy" in rec
        assert rec["strategy"]["name"]


def test_plugin_registry_and_marketplace() -> None:
    from buster.plugins.registry import PluginRegistry
    from buster.plugins.marketplace import PluginMarketplace

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        registry = PluginRegistry(root / "plugin_registry.json")
        marketplace = PluginMarketplace(root / "plugin_marketplace.json")

        android = marketplace.install("android", registry=registry)
        assert android["name"] == "android"
        assert registry.find_by_capability("gradle")
        registry.enable("android", False)
        assert not registry.find_by_capability("gradle")


def test_strategy_planner() -> None:
    from buster.brain.planner.strategy_planner import StrategyPlanner
    from buster.learning import LearningEngine
    from buster.plugins.registry import PluginRegistry

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        learning = LearningEngine(
            memory_path=root / "learning_memory.json",
            strategies_path=root / "build_strategies.json",
            patterns_path=root / "design_patterns.json",
        )
        registry = PluginRegistry(root / "plugin_registry.json")
        registry.register(
            name="python_tools",
            module="buster.plugins.builtin.ollama_plugin",
            capabilities=["python", "desktop"],
        )

        planner = StrategyPlanner(learning=learning, registry=registry)
        plan = planner.plan("Build a desktop timer app", project_type="python")
        assert plan["recommended_strategy"]["name"]
        assert plan["plugins"]
        assert "Record outcome in Learning Engine" in plan["steps"]


if __name__ == "__main__":
    test_learning_engine_roundtrip()
    test_plugin_registry_and_marketplace()
    test_strategy_planner()
    print("SUCCESS: v3.5 Learning + Plugin OS tests passed")
