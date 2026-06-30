from buster.sdk import BusterSDK
from buster.runtime.v6_foundation import V6FoundationRuntime


def test_sdk_events_and_services():
    sdk = BusterSDK(data_dir="data")
    seen = []
    sdk.subscribe("test.event", lambda event: seen.append(event))
    event = sdk.publish("test.event", {"ok": True}, source="test")
    assert event.type == "test.event"
    assert seen and seen[0].payload["ok"] is True

    service = object()
    sdk.register_service("demo", service)
    assert sdk.require_service("demo") is service


def test_sdk_lifecycle_runtime():
    runtime = V6FoundationRuntime(data_dir="data")
    status = runtime.start()
    assert status["running"] is True
    assert runtime.status()["running"] is True
    stopped = runtime.stop()
    assert stopped["running"] is False


def test_sdk_companion_learning_goal_helpers():
    sdk = BusterSDK(data_dir="data")
    sdk.observe("screen active", source="test")
    sdk.speak("Hello Adam", reason="test")
    sdk.learn("reusable pattern", {"project": "buster"})
    sdk.create_goal("finish v6 foundation")
    assert sdk.status()["events"] == 4
