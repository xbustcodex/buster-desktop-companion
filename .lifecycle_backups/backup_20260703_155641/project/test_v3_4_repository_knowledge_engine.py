from pathlib import Path

from buster.knowledge.knowledge_engine import RepositoryKnowledgeEngine


def main():
    root = Path(__file__).parent
    engine = RepositoryKnowledgeEngine(root)
    knowledge = engine.build()

    print("=== Buster v3.4 Repository Knowledge Engine Test ===")
    print("Stats:")
    for k, v in engine.stats().items():
        print(f"{k}: {v}")

    print()
    print('Ask: "summarize file buster\\vision\\engine.py"')
    print(engine.ask("summarize file buster\\vision\\engine.py"))

    print()
    print('Ask: "what depends on openrouter"')
    print(engine.ask("what depends on openrouter"))

    print()
    print('Ask: "rename impact start"')
    print(engine.ask("rename impact start"))

    print()
    print('Ask: "Which classes inherit Agent?"')
    print(engine.ask("Which classes inherit Agent?"))

    print()
    print("SUCCESS: v3.4 Repository Knowledge Engine installed.")


if __name__ == "__main__":
    main()
