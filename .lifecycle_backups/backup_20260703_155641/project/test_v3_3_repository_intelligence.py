from pathlib import Path

from buster.knowledge.intelligence import RepositoryIntelligenceBuilder


def main():
    root = Path(__file__).parent

    print("=== Buster v3.3 Repository Intelligence Test ===")

    intel = RepositoryIntelligenceBuilder(root).build()

    print("Root:", intel.root)
    print("Symbols:", len(intel.symbols))
    print("Imports:", len(intel.imports))
    print("TODOs:", len(intel.todos))
    print("Largest files:", len(intel.largest_files))
    print("Test files:", len(intel.test_files))
    print("Errors:", len(intel.errors))

    print()
    print("Largest files:")
    for f in intel.largest_files[:10]:
        print(f"- {f.file} | {f.lines} lines | {f.size} bytes")

    print()
    print('Ask: "Where is vision engine?"')
    print(intel.ask("Where is vision engine?"))

    print()
    print('Search symbols: "Agent"')
    for s in intel.find_symbols("Agent")[:20]:
        print(f"- {s.kind}: {s.name} ({s.file}:{s.line})")

    print()
    print('Search imports: "openrouter"')
    for i in intel.find_imports("openrouter")[:20]:
        print(f"- {i.module}.{i.name} ({i.file}:{i.line})")

    print()
    print("SUCCESS: v3.3 Repository Intelligence installed.")


if __name__ == "__main__":
    main()
