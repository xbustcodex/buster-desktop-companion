from pathlib import Path

from buster.knowledge.intelligence import RepositoryIntelligenceBuilder


def main():
    root = Path(__file__).parent
    intel = RepositoryIntelligenceBuilder(root).build()

    print("=== Buster v3.3.1 Repository Cleanup Test ===")
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

    bad = [
        f.file for f in intel.largest_files
        if f.file.endswith(".pt")
        or f.file.endswith(".db")
        or f.file.startswith("apply_v")
        or f.file.startswith(root.name)
    ]

    if bad:
        print()
        print("Cleanup failed. Bad files still indexed:")
        for item in bad:
            print("-", item)
        raise SystemExit(1)

    print()
    print("SUCCESS: v3.3.1 Repository Cleanup installed.")


if __name__ == "__main__":
    main()
