from src.rag_assistant.retriever import deduplicate_and_filter


class DummyDoc:
    def __init__(self, content):
        self.page_content = content


def test_deduplicate_and_filter_basic():
    results = [
        (DummyDoc("A"), 0.9),
        (DummyDoc("A"), 0.95),
        (DummyDoc("B"), 0.8),
        (DummyDoc("C"), 0.6),
    ]
    filtered = deduplicate_and_filter(results, top_k=2, threshold=0.7)
    assert len(filtered) == 2
    assert filtered[0][0].page_content == "A"
    assert filtered[1][0].page_content == "B"

