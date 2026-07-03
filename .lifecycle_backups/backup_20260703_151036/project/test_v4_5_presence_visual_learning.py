#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import tempfile

def main() -> None:
    from buster.presence import PresenceEngine, ConversationDirector, PresenceMode
    from buster.visual_learning import VisualLearningEngine
    from buster.vision.learning_bridge import VisionLearningBridge
    from buster.workspace.presence_dashboard import PresenceDashboard
    from buster.ui.widgets.presence_widget import PresenceWidgetModel
    from buster.brain.planner.presence_planner_bridge import PresencePlannerBridge
    with tempfile.TemporaryDirectory() as tmp:
        data = Path(tmp)
        director = ConversationDirector(data)
        state = director.set_mode(PresenceMode.COMPANION)
        assert state["mode"] == "companion"
        greeting = director.greeting("Adam")
        assert greeting["approved"] is True and "Good morning Adam" in greeting["message"]
        presence = PresenceEngine(str(data))
        result = presence.on_activity("Builder generated code", "The Builder Agent is generating the project structure.")
        assert result["emotion"] == "working" and result["speech"]["approved"] is True
        ctx = presence.inspect_context(active_window="Android Studio", idle_minutes=21)
        assert ctx["suggestions"]
        visual = VisualLearningEngine(str(data))
        visual.record_camera_observation("Android Studio", 0.91, "coding workspace")
        visual.record_camera_observation("Android Studio", 0.94, "coding workspace")
        learned = visual.learn_from_recent_camera()
        assert learned["patterns_found"] >= 1
        bridge = VisionLearningBridge(str(data))
        rec = bridge.record_detection("ESP32 board", 0.88, "electronics desk")
        assert rec["ok"] is True
        bridge.record_detection("ESP32 board", 0.90, "electronics desk")
        learned2 = bridge.learn()
        assert learned2["ok"] is True and learned2["patterns_found"] >= 1
        dash = PresenceDashboard(str(data)).snapshot()
        assert dash["status"] == "alive" and "camera_learning" in dash["capabilities"]
        wd = PresenceWidgetModel().update(emotion="thinking", message="I am deciding what to do next.")
        assert wd["emotion"] == "thinking"
        ann = PresencePlannerBridge(str(data)).announce_plan("Build and verify app", 0.96, "low")
        assert ann["ok"] is True
    print("SUCCESS: v4.5 Presence + Visual Learning tests passed")
if __name__ == "__main__": main()
