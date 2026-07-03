from pathlib import Path

from buster.workspace.ai_os import AIOSCore
from buster.repository.project_model import ProjectAnalyzer


def main():
    root = Path(__file__).parent

    print("=== Buster v3.2 AI OS Core Test ===")

    analyzer = ProjectAnalyzer(root)
    model = analyzer.analyze()

    print("Project Model")
    print("Files:", model.files)
    print("Python files:", model.python_files)
    print("Classes:", model.classes)
    print("Functions:", model.functions)
    print("Imports:", model.imports)
    print("TODOs:", model.todos)
    print("Errors:", model.errors)

    ai_os = AIOSCore(root)
    job = ai_os.rebuild_project_model()

    print()
    print("Started background job:", job.id, job.title)

    import time
    for _ in range(20):
        status = ai_os.status()
        job_status = status["jobs"][0]["status"]
        print("Job status:", job_status)
        if job_status in ("finished", "failed"):
            break
        time.sleep(0.2)

    print()
    print("AI OS Status:")
    print(ai_os.status())

    print()
    print("SUCCESS: v3.2 AI OS Core installed.")


if __name__ == "__main__":
    main()
