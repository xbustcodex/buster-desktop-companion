import subprocess
import sys
from pathlib import Path


def run(question: str):
    root = Path(__file__).parent
    cmd = [sys.executable, str(root / "buster_knowledge.py"), question]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=root)

    print("=" * 60)
    print("QUESTION:", question)
    print("-" * 60)
    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise SystemExit(result.returncode)

    return result.stdout


def main():
    out1 = run("summarize file buster\\vision\\engine.py")
    out2 = run("what depends on openrouter")
    out3 = run("rename impact start")
    out4 = run("Which classes inherit Agent?")

    assert "File summary" in out1
    assert "Dependencies for openrouter" in out2
    assert "Rename impact" in out3
    assert "BuilderAgent" in out4

    print()
    print("SUCCESS: v3.4.1 Knowledge Engine CLI installed.")


if __name__ == "__main__":
    main()
