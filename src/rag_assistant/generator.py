from prompt_builder import build_prompt

def build_answer(llm, query, docs):
    prompt = build_prompt(query, docs)
    return llm.invoke(prompt)

