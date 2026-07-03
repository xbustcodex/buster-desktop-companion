import json
from pathlib import Path


DEFAULT_CONFIG = {
    "version_file": "version.json",
    "backup_directory": ".lifecycle_backups",
    "cache_directory": ".lifecycle_cache",
    "log_directory": ".lifecycle_logs",
    "history_file": "data/lifecycle_history.json",
    "health_file": "data/lifecycle_health.json",
    "manifest_file": "data/upgrade_manifest.json",
    "max_backups": 5,
    "verify_after_upgrade": True,
    "auto_rollback_on_failure": True,
    "exclude_patterns": [".git", "__pycache__", "*.pyc", ".env", "venv", ".venv"],
    "components": {
        "core": {"critical": True},
        "ui": {"critical": False},
        "memory": {"critical": True},
        "agents": {"critical": True},
        "plugins": {"critical": False},
        "themes": {"critical": False},
        "assets": {"critical": False}
    }
}


def load_config(root: Path) -> dict:
    config_path = root / "config" / "lifecycle_config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)

    if not config_path.exists():
        config_path.write_text(json.dumps(DEFAULT_CONFIG, indent=4), encoding="utf-8")
        return DEFAULT_CONFIG.copy()

    try:
        loaded = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        loaded = {}

    config = DEFAULT_CONFIG.copy()
    config.update(loaded)
    return config
