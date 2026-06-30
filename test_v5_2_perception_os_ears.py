import json
from pathlib import Path

from buster.perception.perception_os import PerceptionOS
from buster.perception.ears import EarSystem
from buster.perception.eyes import EyeSystem
from buster.perception.attention import AttentionSystem
from buster.perception.privacy import PrivacyGate
from buster.world_model.perception_bridge import PerceptionWorldBridge
from buster.workspace.perception_dashboard import PerceptionDashboard
from buster.brain.planner.perception_planner_bridge import PerceptionPlannerBridge


def assert_true(x, msg):
    if not x:
        raise AssertionError(msg)


def main():
    os = PerceptionOS(mode="companion")
    audio = os.observe_audio(sound_type="speech", text="Buster can you hear me", speaker="Adam", confidence=0.95)
    assert_true(audio["recorded"], "audio should record")
    assert_true(audio["attention"]["importance"] >= 0.7, "wake word should be important")

    visual = os.observe_visual(objects=["person", "laptop", "esp32"], scene="development", confidence=0.9)
    assert_true(visual["recorded"], "visual should record")

    status = os.status()
    assert_true("attention" in status, "status has attention")

    bridge = PerceptionWorldBridge()
    event = bridge.observation_to_world_event(audio["observation"])
    assert_true(event["type"] == "perception_observation", "world event type")

    snap = PerceptionDashboard().snapshot()
    assert_true("focus" in snap, "dashboard has focus")

    suggestion = PerceptionPlannerBridge().suggest(snap)
    assert_true("action" in suggestion, "planner suggestion")

    blocked = PerceptionOS(mode="privacy").observe_audio(sound_type="speech", text="hello", confidence=0.9)
    assert_true(not blocked["recorded"], "privacy mode blocks microphone")

    for path in [
        "data/perception_os_state.json",
        "data/perception_observations.json",
        "data/audio_learning_memory.json",
        "data/attention_state.json",
        "data/perception_privacy_settings.json",
    ]:
        assert_true(Path(path).exists(), f"missing {path}")

    print("SUCCESS: v5.2 Perception OS + Ears tests passed")

if __name__ == "__main__":
    main()
