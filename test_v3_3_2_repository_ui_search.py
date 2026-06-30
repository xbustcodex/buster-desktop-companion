from pathlib import Path

from buster.ui.widgets.ai_os_dashboard import launch_ai_os_dashboard


if __name__ == "__main__":
    project_root = Path(__file__).parent
    launch_ai_os_dashboard(project_root)
