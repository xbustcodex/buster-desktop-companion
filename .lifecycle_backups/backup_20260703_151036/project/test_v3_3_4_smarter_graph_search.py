from pathlib import Path

from buster.knowledge.semantic_graph import SemanticRepositoryGraphBuilder


def main():
    root = Path(__file__).parent
    graph = SemanticRepositoryGraphBuilder(root).build()

    print("=== Buster v3.3.4 Smarter Graph Search Test ===")
    print("Calls:", len(graph.calls))
    print("Inheritance:", len(graph.inheritance))
    print("Dependencies:", len(graph.dependencies))
    print("Unused import hints:", len(graph.unused_import_hints))
    print("Errors:", len(graph.errors))

    print()
    print('Ask: "Who calls start?"')
    print(graph.ask("Who calls start?"))

    print()
    print('Ask: "Who calls VisionEngine.start?"')
    print(graph.ask("Who calls VisionEngine.start?"))

    print()
    print('Ask: "Exact calls self.timer.start"')
    print(graph.ask("Exact calls self.timer.start"))

    print()
    print('Ask: "Which classes inherit Agent?"')
    print(graph.ask("Which classes inherit Agent?"))

    print()
    print('Ask: "Dependencies for buster\\vision\\engine.py"')
    print(graph.ask("Dependencies for buster\\vision\\engine.py"))

    print()
    print("SUCCESS: v3.3.4 Smarter Graph Search installed.")


if __name__ == "__main__":
    main()
