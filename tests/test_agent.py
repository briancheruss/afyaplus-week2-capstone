"""Offline tests with a stub agent; no Ollama or model download needed."""
from langchain_core.messages import AIMessage

from app.agent import AgentSession, ask


class StubAgent:
    def __init__(self):
        self.seen = []

    def invoke(self, payload):
        self.seen.append(payload["messages"])
        return {"messages": [AIMessage(content="Please contact [EMAIL_1] for follow-up.")]}


def test_masked_history_and_authorized_restoration():
    agent, session = StubAgent(), AgentSession()
    output = ask(agent, session, "Email me at demo@example.com")
    assert "demo@example.com" not in output
    assert "demo@example.com" not in str(agent.seen)
    assert "demo@example.com" not in str(session.history)
    restored = ask(agent, session, "What did I ask?", allow_demasking=True)
    assert "demo@example.com" in restored
    session.close()
    assert not session.history and not session.privacy.mapping


def test_sessions_isolated():
    a, b = AgentSession(), AgentSession()
    a.privacy.mask("first@example.com")
    assert not b.privacy.mapping
