import os
from dotenv import load_dotenv
from code.vectordb_and_ingestion import VectorDBManager
from code.prompt_builder import build_prompt
from code.logger import logger


def retrieve_relevant_chunks(vector_db, query, top_k=2, similarity_threshold=1.0):
    """Retrieve top-k relevant chunks under the distance threshold, deduplicated."""
    if not vector_db:
        logger.error("Vector DB not initialized.")
        return []
    results = vector_db.similarity_search_with_score(query, k=top_k * 5)
    results = sorted(results, key=lambda x: (x[1] is None, x[1]))
    unique_contexts = []
    seen = set()
    for doc, score in results:
        if score is not None and score > similarity_threshold:
            continue
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            unique_contexts.append((doc, score))
        if len(unique_contexts) >= top_k:
            break
    return unique_contexts


def respond_to_query(query, top_k=2, similarity_threshold=1.0):
    """Retrieve relevant chunks and generate a concise answer using Groq LLM."""
    load_dotenv()
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        logger.error("GROQ_API_KEY missing in .env")
        return "Error: GROQ_API_KEY missing."

    from langchain_groq import ChatGroq

    vm = VectorDBManager()
    vm.load_db()
    if not vm.vector_db:
        vm.embed_and_insert()
    docs = retrieve_relevant_chunks(vm.vector_db, query, top_k=top_k, similarity_threshold=similarity_threshold)
    if not docs:
        return "No relevant information found."
    prompt = build_prompt(query, docs)
    try:
        llm = ChatGroq(api_key=groq_key, model="llama-3.1-8b-instant", temperature=0)
        answer = llm.invoke(prompt)
        logger.info(f"Query: {query}\nAnswer: {answer}")
        return answer
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        return f"Error: {e}"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ethiopian History RAG CLI")
    parser.add_argument("query", type=str, help="Your question about Ethiopian history")
    parser.add_argument("--top_k", type=int, default=2, help="Number of top chunks to retrieve")
    parser.add_argument("--threshold", type=float, default=1.0, help="Distance threshold (lower = more similar)")
    args = parser.parse_args()

    answer = respond_to_query(args.query, top_k=args.top_k, similarity_threshold=args.threshold)
    print("\nAnswer:\n", answer)

