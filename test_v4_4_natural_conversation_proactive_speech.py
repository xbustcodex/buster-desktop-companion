#!/usr/bin/env python3
"""Tests for Buster v4.4 Natural Conversation + Proactive Speech."""

from __future__ import annotations

import json
from pathlib import Path


def assert_exists(path: str) -> None:
    assert Path(path).exists(), f"Missing {path}"


def main() -> None:
    required = [
        "buster/conversation_os/__init__.py",
        "buster/conversation_os/modes.py",
        "buster/conversation_os/settings.py",
        "buster/conversation_os/speech_queue.py",
        "buster/conversation_os/speech_scheduler.py",
        "buster/conversation_os/explanations.py",
        "buster/conversation_os/natural_conversation.py",
        "buster/conversation_os/mission_voice.py",
        "buster/conversation_os/engine.py",
        "buster/collaboration/proactive_voice_runtime.py",
        "buster/brain/planner/conversation_planner_bridge.py",
        "buster/workspace/proactive_speech_dashboard.py",
        "buster/ui/widgets/proactive_speech_widget.py",
        "data/proactive_speech_settings.json",
        "data/proactive_speech_queue.json",
        "data/conversation_os_state.json",
    ]
    for path in required:
        assert_exists(path)

    from buster.conversation_os import ConversationOS, TalkMode, SpeechPriority
    from buster.conversation_os.explanations import DecisionExplainer
    from buster.workspace.proactive_speech_dashboard import ProactiveSpeechDashboard
    from buster.ui.widgets.proactive_speech_widget import ProactiveSpeechWidgetModel
    from buster.brain.planner.conversation_planner_bridge import ConversationPlannerBridge

    os = ConversationOS()
    os.queue.clear()
    os.set_talk_mode(TalkMode.JARVIS)
    status = os.status()
    assert status["settings"]["mode"] == TalkMode.JARVIS
    assert status["settings"]["enabled"] is True

    item = os.mission_event({
        "event": "planner_created",
        "actor": "Planner",
        "message": "Repository, Learning, Builder, Tester, Verifier are ready.",
        "confidence": 0.96,
        "risk": "low",
    })
    assert item["priority"] in {SpeechPriority.NORMAL, SpeechPriority.IMPORTANT, "normal", "important"}
    assert os.status()["pending_speech"] >= 1

    spoken = os.next_speech()
    assert spoken is not None
    assert "Confidence" in spoken["text"] or "confidence" in spoken["text"]

    explanation = DecisionExplainer().explain({
        "action": "use the learned Python strategy",
        "confidence": 0.97,
        "risk": "low",
        "reason": "similar projects succeeded before",
    })
    assert "97%" in explanation
    assert "similar projects" in explanation

    why = os.why({
        "action": "run tests",
        "reason": "the Builder changed code",
        "confidence": 0.91,
    })
    assert "run tests" in why
    assert "91%" in why

    bridge = ConversationPlannerBridge()
    queued = bridge.announce_plan({
        "goal": "Build a desktop tool",
        "summary": "I will use Repository, Learning, Builder, Tester, and Verifier.",
        "confidence": 0.94,
        "risk": "low",
    })
    assert queued["source"] == "mission_control"

    dashboard = ProactiveSpeechDashboard().snapshot()
    assert dashboard["available"] is True
    assert "pending_speech" in dashboard

    widget = ProactiveSpeechWidgetModel().render_model()
    assert widget["title"] == "Proactive Speech"
    assert widget["available"] is True

    settings_data = json.loads(Path("data/proactive_speech_settings.json").read_text(encoding="utf-8"))
    assert "mode" in settings_data

    print("SUCCESS: v4.4 Natural Conversation + Proactive Speech tests passed")


if __name__ == "__main__":
    main()
