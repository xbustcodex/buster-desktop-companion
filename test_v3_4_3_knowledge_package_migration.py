from pathlib import Path

from buster.knowledge import RepositoryKnowledgeEngine
from buster.knowledge.intelligence import RepositoryIntelligenceBuilder
from buster.knowledge.semantic_graph import SemanticRepositoryGraphBuilder

# compatibility imports should also still work
from buster.repository.knowledge_engine import RepositoryKnowledgeEngine as CompatKnowledgeEngine


def main():
    root = Path(__file__).parent

    intel = RepositoryIntelligenceBuilder(root).build()
    graph = SemanticRepositoryGraphBuilder(root).build()
    engine = RepositoryKnowledgeEngine(root)
    engine.build()

    compat = CompatKnowledgeEngine(root)
    compat.build()

    print("=== Buster v3.4.3 Knowledge Package Migration Test ===")
    print("Knowledge package OK")
    print("Symbols:", len(intel.symbols))
    print("Calls:", len(graph.calls))
    print("Files:", engine.stats()["files"])
    print("Compat files:", compat.stats()["files"])

    print()
    print(engine.ask("Which classes inherit Agent?"))

    print()
    print("SUCCESS: v3.4.3 Knowledge Package Migration installed.")


if __name__ == "__main__":
    main()
