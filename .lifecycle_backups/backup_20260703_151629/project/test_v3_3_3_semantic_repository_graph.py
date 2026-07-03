from pathlib import Path

from buster.knowledge.semantic_graph import SemanticRepositoryGraphBuilder


def main():
    root = Path(__file__).parent
    graph = SemanticRepositoryGraphBuilder(root).build()

    print("=== Buster v3.3.3 Semantic Repository Graph Test ===")
    print("Calls:", len(graph.calls))
    print("Inheritance:", len(graph.inheritance))
    print("Dependencies:", len(graph.dependencies))
    print("Unused import hints:", len(graph.unused_import_hints))
    print("Errors:", len(graph.errors))

    print()
    print('Ask: "Who calls start?"')
    print(graph.ask("Who calls start?"))

    print()
    print('Ask: "Which classes inherit Agent?"')
    print(graph.ask("Which classes inherit Agent?"))

    print()
    print('Ask: "Which modules depend on OpenRouter?"')
    print(graph.ask("Which modules depend on OpenRouter?"))

    print()
    print("Unused import hints:")
    for item in graph.unused_import_hints[:20]:
        print("-", item)

    print()
    print("SUCCESS: v3.3.3 Semantic Repository Graph installed.")


if __name__ == "__main__":
    main()
