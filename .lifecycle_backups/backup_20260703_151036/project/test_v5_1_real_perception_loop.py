import tempfile
from pathlib import Path

from buster.perception.real_perception_loop import RealPerceptionLoop
from buster.vision.perception_feed import VisionPerceptionFeed
from buster.brain.planner.perception_planner_bridge import PerceptionPlannerBridge
from buster.workspace.perception_dashboard import PerceptionDashboard
from buster.ui.widgets.perception_loop_widget import PerceptionLoopWidgetModel


def test_real_perception_loop():
    with tempfile.TemporaryDirectory() as td:
        loop = RealPerceptionLoop(data_dir=td)
        result = loop.observe(
            source="screen",
            observation_type="app_context",
            summary="Android Studio is active",
            confidence=0.92,
            importance=0.8,
            data={"app": "Android Studio", "project": "Android Toolbox"},
        )
        assert result["observation"]["summary"] == "Android Studio is active"
        assert result["world_update"]["world_observations"] >= 1
        assert result["speech"] is not None
        assert "Android Studio" in result["speech"]["message"]

        feed = VisionPerceptionFeed(data_dir=td)
        feed.feed_camera_detection("ESP32 board", confidence=0.88, extra={"device": "ESP32", "importance": 0.9})

        bridge = PerceptionPlannerBridge(data_dir=td)
        ctx = bridge.context_for_planner()
        assert ctx["recent_observations"]
        assert "Prepare" in ctx["suggestion"]

        dash = PerceptionDashboard(data_dir=td).snapshot()
        assert dash["observations_seen"] >= 2

        widget = PerceptionLoopWidgetModel(data_dir=td).data()
        assert widget["title"] == "Real Perception Loop"


if __name__ == "__main__":
    test_real_perception_loop()
    print("SUCCESS: v5.1 Real Perception Loop tests passed")
