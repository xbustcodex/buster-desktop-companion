from __future__ import annotations

import sys
from pathlib import Path

from buster.knowledge.knowledge_engine import RepositoryKnowledgeEngine


HELP = """
Buster Knowledge Engine CLI v3.4.1

Usage:
  python buster_knowledge.py "summarize file buster\\vision\\engine.py"
  python buster_knowledge.py "what depends on openrouter"
  python buster_knowledge.py "rename impact start"
  python buster_knowledge.py "Which classes inherit Agent?"
  python buster_knowledge.py "todo"
  python buster_knowledge.py "vision"

Examples:
  python buster_knowledge.py "summarize file buster\\brain\\engine.py"
  python buster_knowledge.py "what depends on cv2"
  python buster_knowledge.py "who calls start"
"""


def main():
    root = Path(__file__).parent

    if len(sys.argv) <= 1:
        print(HELP)
        return

    question = " ".join(sys.argv[1:]).strip()

    if question.lower() in {"help", "-h", "--help", "/?"}:
        print(HELP)
        return

    print("=== Buster Knowledge Engine v3.4.1 ===")
    print("Question:", question)
    print()

    engine = RepositoryKnowledgeEngine(root)
    answer = engine.ask(question)

    print(answer)


if __name__ == "__main__":
    main()
