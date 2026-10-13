import json
import re
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "faqs.json"
STOP = {"what", "when", "where", "how", "does", "do", "the", "a", "an", "is", "are", "i", "my", "for", "can", "college", "about", "tell", "me", "there", "any"}

def tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOP}

def retrieve(message: str, limit: int = 3) -> list[dict]:
    entries = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    query = tokens(message)
    scored = []
    for item in entries:
        keywords = tokens(" ".join(item.get("keywords", [])))
        question = tokens(item["question"])
        score = 3 * len(query & keywords) + len(query & question)
        if score > 0:
            scored.append((score, item))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in scored[:limit]]
