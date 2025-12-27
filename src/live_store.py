import os
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple

SUPPORTED_EXTS = {".txt", ".md", ".log"}

@dataclass
class Doc:
    path: str
    mtime: float
    text: str

class LiveStore:
    """
    A tiny 'live knowledge store' for Round-2 demo.
    Watches a folder and keeps the latest text of each file.
    """
    def __init__(self, folder: str):
        self.folder = folder
        self.docs: Dict[str, Doc] = {}

    def _read_text_file(self, path: str) -> str:
        # Safe read (ignore weird chars)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def scan_once(self) -> Tuple[int, int, int]:
        """
        Returns: (added, updated, removed)
        """
        added = updated = removed = 0

        if not os.path.exists(self.folder):
            os.makedirs(self.folder, exist_ok=True)

        seen: set[str] = set()

        for root, _, files in os.walk(self.folder):
            for name in files:
                ext = os.path.splitext(name)[1].lower()
                if ext not in SUPPORTED_EXTS:
                    continue
                path = os.path.join(root, name)
                seen.add(path)
                mtime = os.path.getmtime(path)

                if path not in self.docs:
                    text = self._read_text_file(path)
                    self.docs[path] = Doc(path=path, mtime=mtime, text=text)
                    added += 1
                else:
                    if mtime > self.docs[path].mtime:
                        text = self._read_text_file(path)
                        self.docs[path] = Doc(path=path, mtime=mtime, text=text)
                        updated += 1

        # Removed files
        for path in list(self.docs.keys()):
            if path not in seen:
                del self.docs[path]
                removed += 1

        return added, updated, removed

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, str]]:
        """
        Super simple keyword scoring. Returns [(path, snippet), ...]
        """
        q = (query or "").strip().lower()
        if not q:
            return []

        scored: List[Tuple[int, str, str]] = []
        for path, doc in self.docs.items():
            text_low = doc.text.lower()
            score = text_low.count(q)
            if score > 0:
                idx = text_low.find(q)
                start = max(0, idx - 80)
                end = min(len(doc.text), idx + 120)
                snippet = doc.text[start:end].replace("\n", " ").strip()
                scored.append((score, path, snippet))

        scored.sort(reverse=True, key=lambda x: x[0])
        return [(p, s) for _, p, s in scored[:top_k]]

    def summary(self) -> str:
        return f"{len(self.docs)} live docs loaded from '{self.folder}'."
