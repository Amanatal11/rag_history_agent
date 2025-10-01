from typing import List, Tuple

def deduplicate_and_filter(results: List[Tuple[object, float]], top_k: int, threshold: float):
    unique = []
    seen = set()
    for doc, score in results:
        if score is not None and score < threshold:
            continue
        if getattr(doc, "page_content", None) not in seen:
            seen.add(getattr(doc, "page_content", None))
            unique.append((doc, score))
        if len(unique) >= top_k:
            break
    return unique

