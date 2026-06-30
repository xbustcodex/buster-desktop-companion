import warnings
from pathlib import Path

from buster.utils import utc_timestamp, load_json, save_json, get_logger


def test_utils_datetime_json_logger(tmp_path):
    stamp = utc_timestamp()
    assert stamp.endswith("Z")
    assert "+00:00" not in stamp

    path = tmp_path / "nested" / "data.json"
    save_json(path, {"ok": True})
    assert load_json(path)["ok"] is True

    logger = get_logger("buster.test")
    assert logger.name == "buster.test"


def test_no_datetime_utcnow_usage_in_buster_source():
    root = Path("buster")
    offenders = []
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "datetime.utcnow(" in text:
            offenders.append(str(path))
    assert not offenders, "datetime.utcnow() still used in: " + ", ".join(offenders)
