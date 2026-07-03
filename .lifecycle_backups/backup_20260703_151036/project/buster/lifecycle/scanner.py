import fnmatch
import hashlib
from pathlib import Path


class LifecycleScanner:
    def __init__(self, root: Path, exclude_patterns=None):
        self.root = Path(root)
        self.exclude_patterns = exclude_patterns or []

    def should_exclude(self, path: Path) -> bool:
        text = str(path).replace("\\", "/")
        name = path.name

        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(name, pattern) or pattern in text:
                return True

        return False

    def hash_file(self, path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()

    def scan(self) -> dict:
        files = []
        hashes = {}
        total_size = 0

        for path in self.root.rglob("*"):
            if self.should_exclude(path):
                continue

            if path.is_file():
                rel = path.relative_to(self.root).as_posix()
                try:
                    size = path.stat().st_size
                    file_hash = self.hash_file(path)
                except Exception:
                    continue

                files.append(rel)
                hashes[rel] = file_hash
                total_size += size

        return {
            "root": str(self.root),
            "files": files,
            "hashes": hashes,
            "size": total_size,
            "count": len(files)
        }
