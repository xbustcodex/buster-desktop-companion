from buster.builder.doctor import BusterDoctor
from buster.builder.repair import BusterRepair
from buster.perception.real_perception_loop import RealPerceptionLoop


def test_real_perception_loop_basic():
    loop = RealPerceptionLoop(auto_persist=False)
    status = loop.start()
    assert status["running"] is True
    obs = loop.observe("camera", "object", "desk visible", confidence=0.9, importance=0.6)
    assert obs["source"] == "camera"
    assert loop.tick()["tick"] >= 1
    assert len(loop.drain_recent()) == 1
    loop.stop()


def test_buster_doctor_and_repair():
    repair = BusterRepair()
    repair_report = repair.run()
    assert repair_report["ok"] is True
    doctor = BusterDoctor()
    report = doctor.run()
    assert "issues" in report
    assert isinstance(report["issue_count"], int)
