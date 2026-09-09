import json
import os
import hashlib


CACHE_FILE = "outputs/triage_cache.json"


def _ticket_key(subject: str, message: str) -> str:
    content = f"{subject}|{message}"
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def get_cached_result(subject: str, message: str):
    cache = load_cache()
    key = _ticket_key(subject, message)
    return cache.get(key)


def save_result(subject: str, message: str, result):
    cache = load_cache()
    key = _ticket_key(subject, message)

    cache[key] = {
        "category": result.category,
        "urgency": result.urgency,
        "confidence": result.confidence,
        "route_to": result.route_to,
        "human_review": result.human_review,
        "reason": result.reason,
    }

    save_cache(cache)