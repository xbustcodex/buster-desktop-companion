from buster.agent_os import AgentRuntime, LivingCompanionRuntime
from buster.ui.widgets.agent_os_widget import AgentOSWidgetModel


def test_agent_runtime_registers_agents():
    runtime = AgentRuntime(data_dir="data")
    runtime.install_default_agents()
    status = runtime.status()
    assert status["agents"]["count"] >= 10
    assert "builder" in status["agents"]["agents"]
    assert "tester" in status["agents"]["agents"]


def test_living_companion_demo_messages():
    companion = LivingCompanionRuntime(data_dir="data")
    companion.start()
    status = companion.run_coding_demo()
    messages = " ".join(m["message"] for m in status["messages"])
    assert "Android Studio" in messages
    assert "ESP32" in messages
    assert "Builder Agent" in messages
    assert "recorded a new build strategy" in messages


def test_agent_os_widget_model():
    widget = AgentOSWidgetModel(data_dir="data")
    data = widget.data()
    assert data["title"] == "Agent Runtime & Living Companion"
    assert "agent_count" in data
