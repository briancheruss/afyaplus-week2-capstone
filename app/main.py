"""CLI entry point. Never use real patient data in this educational demo."""

import argparse

from app.agent import AgentSession, ask, create_agent
from app.rag_pipeline import build_index


def main() -> None:
    parser = argparse.ArgumentParser(description="AfyaPlus Week 2 RAG agent demo")
    parser.add_argument(
        "--reindex", action="store_true", help="Rebuild local vector index"
    )
    parser.add_argument(
        "--index-only", action="store_true", help="Build index and exit"
    )
    args = parser.parse_args()
    print("Loading local knowledge index (first run downloads an embedding model)...")
    index = build_index(reset=args.reindex)
    if args.index_only:
        print("Index ready.")
        return
    agent = create_agent(index)
    session = AgentSession()
    print("AfyaPlus demo. No real patient data. Type 'exit' to quit.")
    try:
        while True:
            question = input("You: ").strip()
            if question.lower() in {"exit", "quit"}:
                break
            if not question:
                continue

            try:
                print("AfyaPlus:", ask(agent, session, question))
            except (ConnectionError, TimeoutError, ValueError, RuntimeError) as exc:
                print(
                    f"Agent unavailable ({type(exc).__name__}). "
                    "Check Ollama and local model."
                )

    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        session.close()


if __name__ == "__main__":
    main()
