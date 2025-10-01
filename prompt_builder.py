def build_prompt(query, docs):
    """
    Build a concise, factual prompt for the LLM using only relevant context.
    """
    context = "\n".join([
        f"- {doc.page_content.strip()[:300].replace('\n', ' ')} (Source: {doc.metadata.get('filename','')})"
        for doc, _ in docs
    ])
    prompt = (
        f"Answer the following question using only the provided context. "
        f"Keep your answer concise and factual. Cite sources if possible.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        f"Answer:"
    )
    return prompt