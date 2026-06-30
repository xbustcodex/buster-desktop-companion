from pathlib import Path
import tempfile


def test_world_model_core():
    with tempfile.TemporaryDirectory() as d:
        from buster.world_model import WorldModelEngine
        wm = WorldModelEngine(data_dir=d)
        user = wm.add_entity("user", "Adam", {"role": "builder"})
        project = wm.add_entity("project", "Buster AI OS", {"version": "5.0"})
        wm.link(user["entity_id"], project["entity_id"], "builds")
        wm.observe("desktop", "Android Studio opened and Pixel connected", importance=0.8)
        status = wm.understand_now()
        assert status["context"]["mode"] == "android_development"
        assert status["observation_count"] >= 1
        dash = wm.dashboard()
        assert dash["status"] == "online"
        assert dash["recent_timeline"]


def test_perception_and_companion():
    with tempfile.TemporaryDirectory() as d:
        from buster.perception import PerceptionEngine
        from buster.companion import CompanionEngine
        p = PerceptionEngine(data_dir=d)
        result = p.perceive_text("desktop", "ESP32 connected and Arduino IDE opened", importance=0.8)
        assert result["understanding"]["context"]["mode"] == "hardware_development"
        c = CompanionEngine(data_dir=d, name="Adam")
        msg = c.morning_message()
        assert "Adam" in msg


def test_bridges_and_widget():
    with tempfile.TemporaryDirectory() as d:
        from buster.vision.world_model_bridge import VisionWorldModelBridge
        from buster.brain.planner.world_model_planner_bridge import WorldModelPlannerBridge
        from buster.workspace.world_model_dashboard import WorldModelDashboard
        from buster.ui.widgets.world_model_widget import WorldModelWidgetModel
        bridge = VisionWorldModelBridge(data_dir=d)
        out = bridge.record_scene("Camera sees user at desk with ESP32", objects=["person", "esp32"], confidence=0.8)
        assert out["ok"] is True
        plan = WorldModelPlannerBridge(data_dir=d).plan_from_world()
        assert "recommendation" in plan
        snap = WorldModelDashboard(data_dir=d).snapshot()
        lines = WorldModelWidgetModel(snap).as_lines()
        assert any("WORLD MODEL" in x for x in lines)


if __name__ == "__main__":
    test_world_model_core()
    test_perception_and_companion()
    test_bridges_and_widget()
    print("SUCCESS: v5.0 World Model AI OS tests passed")
