"""Offline tests for citation validation; full embedding integration is opt-in."""

from app.rag_pipeline import retrieve_context


class FakeNode:
    def __init__(self):
        self.metadata = {"file_name": "insurance_policy.md"}
        self.node_id = "abc123"

    def get_content(self):
        return "Coverage requires human verification."


class FakeHit:
    node = FakeNode()


class FakeIndex:
    def as_retriever(self, similarity_top_k):
        assert similarity_top_k == 2
        return self

    def retrieve(self, query):
        return [FakeHit()]


def test_citations_present():
    result = retrieve_context("outpatient coverage", index=FakeIndex(), top_k=2)
    assert "[SOURCE: insurance_policy.md" in result
    assert "human verification" in result


def test_empty_question():
    assert "NO_VERIFIED_CONTEXT" in retrieve_context("  ", index=FakeIndex())
