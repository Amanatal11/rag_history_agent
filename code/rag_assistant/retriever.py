from typing import List, Tuple


def deduplicate_and_filter(results: List[Tuple[object, float]], top_k: int, threshold: float):
    """Filter by distance threshold and deduplicate by page content."""
    unique = []
    seen = set()
    for doc, score in results:
        if score is not None and score > threshold:
            continue
        content = getattr(doc, "page_content", None)
        if content not in seen:
            seen.add(content)
            unique.append((doc, score))
        if len(unique) >= top_k:
            break
    return unique

