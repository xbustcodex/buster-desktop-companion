from pathlib import Path
from buster.runtime import BusterRuntimeEngine, RuntimeScheduler, RuntimeDispatcher, IdleManager, IntentPredictionEngine
from buster.workspace.runtime_dashboard import RuntimeDashboard
from buster.ui.widgets.runtime_widget import RuntimeWidgetModel
from buster.brain.planner.runtime_planner_bridge import runtime_context_for_planner
from buster.companion.runtime_speech_bridge import get_pending_runtime_speech


def main():
    observations = [
        {'source': 'screen', 'type': 'app_opened', 'summary': 'Android Studio opened with Pixel connected', 'confidence': 0.95},
        {'source': 'hardware', 'type': 'usb', 'summary': 'Pixel device detected', 'confidence': 0.9},
    ]
    engine = BusterRuntimeEngine(observation_provider=lambda: observations)
    started = engine.start()
    assert started['runtime_status'] == 'running'
    result = engine.tick_once()
    assert result['heartbeat']['tick'] >= 1
    assert result['prediction']['intent'] == 'android_development'
    assert result['speech'] is not None
    assert Path('data/buster_runtime_state.json').exists()
    assert Path('data/runtime_events.json').exists()
    assert Path('data/mission_control_unified.json').exists()

    predictor = IntentPredictionEngine()
    esp = predictor.predict([{'summary': 'ESP32 serial monitor connected'}])
    assert esp['intent'] == 'embedded_development'

    idle = IdleManager()
    for _ in range(5):
        idle_state = idle.observe_activity(False)
    assert idle_state['dream_mode_ready'] is True

    scheduler = RuntimeScheduler()
    scheduler.add_job('test_job', 1, lambda: 'ok')
    jobs = scheduler.run_due(1)
    assert jobs and jobs[0]['result'] == 'ok'

    seen=[]
    dispatcher = RuntimeDispatcher()
    dispatcher.subscribe('unit.event', lambda event: seen.append(event))
    dispatcher.publish('unit.event', {'ok': True})
    assert seen and seen[0]['payload']['ok'] is True

    planner_context = runtime_context_for_planner()
    assert 'runtime_tick' in planner_context
    dashboard = RuntimeDashboard().snapshot()
    assert dashboard['title'] == 'Runtime Integration'
    widget = RuntimeWidgetModel().build()
    assert widget['heading'] == 'Buster Runtime'
    speech = get_pending_runtime_speech()
    assert isinstance(speech, list)
    engine.stop()
    print('SUCCESS: v5.6 Runtime Integration tests passed')

if __name__ == '__main__':
    main()
