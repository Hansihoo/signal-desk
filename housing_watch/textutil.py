import html
import math
import re
from collections import Counter


TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")
TOKEN_RE = re.compile(r"[가-힣]{2,}|[A-Za-z0-9][A-Za-z0-9_+-]*")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def clean_text(value):
    if value is None:
        return ""
    text = html.unescape(str(value))
    text = TAG_RE.sub(" ", text)
    text = SPACE_RE.sub(" ", text)
    return text.strip()


def first_date(value):
    match = DATE_RE.search(value or "")
    return match.group(0) if match else ""


def stable_space(value):
    return SPACE_RE.sub(" ", value or "").strip()


def tokens(value):
    text = (value or "").lower()
    raw_tokens = TOKEN_RE.findall(text)
    expanded = []
    for token in raw_tokens:
        expanded.append(token)
        if re.search(r"[가-힣]", token) and len(token) > 2:
            expanded.extend(token[index : index + 2] for index in range(len(token) - 1))
    return expanded


def vector(value):
    counts = Counter(tokens(value))
    norm = math.sqrt(sum(weight * weight for weight in counts.values()))
    return counts, norm


def cosine(query, target):
    query_counts, query_norm = vector(query)
    target_counts, target_norm = vector(target)
    if not query_norm or not target_norm:
        return 0.0
    overlap = set(query_counts).intersection(target_counts)
    dot = sum(query_counts[token] * target_counts[token] for token in overlap)
    return dot / (query_norm * target_norm)


def content_hash(parts):
    import hashlib

    joined = "\n".join(part or "" for part in parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()

