def build_prompt(query, docs):
    """
    Build a concise, factual prompt for the LLM using only relevant context.
    Avoid hedging (e.g., "I don't know") when relevant context is provided.
    """
    context = "\n".join([
        f"- {doc.page_content.strip()[:300].replace('\n', ' ')} (Source: {doc.metadata.get('filename','')})"
        for doc, _ in docs
    ])
    prompt = (
        f"You are a precise historian. Use only the context to answer. "
        f"If the context clearly contains the answer, state it directly without hedging. "
        f"Be concise and include the source filename in parentheses where applicable.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        f"Answer:"
    )
    return prompt