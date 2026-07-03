from pathlib import Path

REQUIRED = [
    "buster/mind/mission_context.py",
    "buster/mind/goal_loop.py",
    "buster/mind/context_priority.py",
    "buster/mind/companion_context.py",
    "buster/mind/work_loop.py",
    "buster/workspace/working_memory_goal_dashboard.py",
    "buster/ui/widgets/working_memory_goal_widget.py",
    "buster/brain/planner/goal_loop_planner_bridge.py",
    "data/mission_context.json",
    "data/goal_loop_state.json",
    "data/working_memory_goal_loop.json",
    "data/companion_context.json",
]

for path in REQUIRED:
    assert Path(path).exists(), f"Missing {path}"

from buster.mind.work_loop import WorkingMemoryGoalLoop
from buster.brain.planner.goal_loop_planner_bridge import GoalLoopPlannerBridge
from buster.workspace.working_memory_goal_dashboard import WorkingMemoryGoalDashboard

loop = WorkingMemoryGoalLoop()
mission = loop.start_mission("Debug Android project", priority=8)
assert mission["title"] == "Debug Android project"

snapshot = loop.ingest_observation({
    "source": "perception",
    "text": "Android Studio error failed build exception",
    "priority": 9,
    "risk": "high",
    "confidence": 0.92,
})
assert snapshot["goals"], "Observation should create a goal"
assert snapshot["mission"]["active_goal_ids"], "Mission should attach created goal"
assert "suggested_speech" in snapshot["companion_context"]

bridge = GoalLoopPlannerBridge(loop)
plan = bridge.plan_from_observation({"source": "vision", "text": "ESP32 connected", "priority": 7})
assert plan["should_plan"] is True

model = WorkingMemoryGoalDashboard().render_model(snapshot)
assert model["active_goals"] >= 1
assert model["mission_title"] == "Debug Android project"

print("SUCCESS: v5.4 Working Memory + Goal Loop tests passed")
