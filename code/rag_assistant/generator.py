from code.prompt_builder import build_prompt


def build_answer(llm, query, docs):
    """Build prompt and invoke LLM to get an answer."""
    prompt = build_prompt(query, docs)
    return llm.invoke(prompt)

