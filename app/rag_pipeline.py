"""LlamaIndex ingestion and persistent local Chroma vector retrieval."""
from pathlib import Path
from typing import Any

from app.config import EMBEDDING_MODEL, KNOWLEDGE_DIR, STORAGE_DIR, TOP_K


def _embedding_model() -> Any:
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    return HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)


def build_index(*, reset: bool = False, knowledge_dir: Path = KNOWLEDGE_DIR,
                storage_dir: Path = STORAGE_DIR) -> Any:
    """Ingest trusted Markdown manuals; rebuild explicitly after source changes."""
    import chromadb
    from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
    from llama_index.core.node_parser import SentenceSplitter
    from llama_index.core.storage import StorageContext
    from llama_index.vector_stores.chroma import ChromaVectorStore

    knowledge_dir = Path(knowledge_dir)
    paths = sorted(knowledge_dir.glob("*.md"))
    if not paths:
        raise FileNotFoundError(f"No Markdown manuals found in {knowledge_dir}")
    storage_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(storage_dir))
    if reset:
        try:
            client.delete_collection("afyaplus_manuals")
        except ValueError:
            pass
    collection = client.get_or_create_collection("afyaplus_manuals")
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    embedding = _embedding_model()
    if collection.count() > 0:
        return VectorStoreIndex.from_vector_store(vector_store, embed_model=embedding)
    documents = SimpleDirectoryReader(input_files=[str(x) for x in paths]).load_data()
    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=64)
    nodes = splitter.get_nodes_from_documents(documents)
    return VectorStoreIndex(nodes, storage_context=storage_context, embed_model=embedding)


def retrieve_context(query: str, *, index: Any, top_k: int = TOP_K) -> str:
    """Retrieve context with source labels; return explicit failure on no reliable hits."""
    if not query.strip():
        return "NO_VERIFIED_CONTEXT: Empty question."
    retriever = index.as_retriever(similarity_top_k=top_k)
    hits = retriever.retrieve(query)
    parts: list[str] = []
    for hit in hits:
        node = hit.node
        text = node.get_content().strip()
        if not text:
            continue
        filename = Path(str(node.metadata.get("file_name", "unknown"))).name
        # Only manual filenames are valid citations.
        if filename not in {p.name for p in KNOWLEDGE_DIR.glob("*.md")}:
            continue
        parts.append(f"[SOURCE: {filename}; CHUNK: {node.node_id}]\n{text}")
    return "\n\n".join(parts) if parts else "NO_VERIFIED_CONTEXT: No relevant manual passage found."
