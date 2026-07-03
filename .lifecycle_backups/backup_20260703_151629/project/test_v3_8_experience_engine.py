from __future__ import annotations
import json
from pathlib import Path

def assert_true(value, message):
    if not value:
        raise AssertionError(message)

def main() -> None:
    required = [
        "buster/experience/__init__.py", "buster/experience/engine.py", "buster/experience/records.py",
        "buster/experience/skills.py", "buster/experience/design_decisions.py", "buster/experience/project_experience.py",
        "buster/experience/user_overrides.py", "buster/intelligence/experience_advisor.py",
        "buster/brain/planner/experience_planner.py", "buster/workspace/experience_dashboard.py",
        "data/experience_memory.json", "data/skill_profiles.json", "data/project_experience_index.json", "data/user_overrides.json",
    ]
    for rel in required: assert_true(Path(rel).exists(), f"Missing {rel}")
    from buster.experience.engine import ExperienceEngine
    from buster.experience.records import make_experience_record
    from buster.intelligence.experience_advisor import ExperienceAdvisor
    from buster.brain.planner.experience_planner import ExperiencePlanner
    from buster.workspace.experience_dashboard import ExperienceDashboard
    engine = ExperienceEngine("data")
    before = engine.summary()["records"]
    record = make_experience_record(project="v3_8_test_project", project_type="python_gui", task="build test app", strategy="builder_tester_verifier", outcome="success", confidence=0.93, agents=["builder", "tester", "verifier"], design_choices=["modular_services", "event_driven_updates"], fixes=["none"])
    saved = engine.record_outcome(record)
    assert_true(saved.success, "ExperienceRecord success property failed")
    rec = engine.recommend_for_project("python_gui", "build another app")
    assert_true("recommended_strategy" in rec, "recommendation missing strategy")
    assert_true(rec["confidence"] >= 0.35, "recommendation confidence too low")
    advisor = ExperienceAdvisor("data")
    advice = advisor.advise("python_gui", "build another app")
    assert_true(advice.get("reason"), "advisor did not include reason")
    planner = ExperiencePlanner("data")
    plan = planner.plan_with_experience("python_gui", "build another app")
    assert_true("record_experience" in plan["steps"], "planner does not record experience")
    dashboard = ExperienceDashboard("data")
    snap = dashboard.snapshot()
    assert_true(snap.get("available") is True, "dashboard unavailable")
    assert_true(snap.get("records", 0) >= before + 1, "experience record count did not increase")
    for rel in ["data/experience_memory.json", "data/skill_profiles.json", "data/project_experience_index.json"]:
        json.loads(Path(rel).read_text(encoding="utf-8"))
    print("SUCCESS: v3.8 Experience Engine tests passed")
if __name__ == "__main__": main()
