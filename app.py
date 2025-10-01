import os
import streamlit as st
from dotenv import load_dotenv
from vectordb_and_ingestion import VectorDBManager
from prompt_builder import build_prompt
from logger import logger

st.set_page_config(page_title="Ethiopian History RAG Assistant", layout="centered")
st.title("Ethiopian History RAG Assistant")

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

@st.cache_resource(show_spinner=True)
def get_db_manager():
    dbm = VectorDBManager()
    dbm.load_db()
    if not dbm.vector_db:
        dbm.embed_and_insert()
    return dbm

db_manager = get_db_manager()
vector_db = db_manager.get_vector_db()

st.markdown("Ask a question about Ethiopian history. The assistant will search the database and answer concisely.")

query = st.text_input("Your question:", "")
top_k = st.slider("Top-K chunks", min_value=1, max_value=5, value=2)
threshold = st.slider("Similarity threshold (distance; lower = more similar)", min_value=0.0, max_value=1.0, value=0.4, step=0.05)

if st.button("Get Answer") and query.strip():
    with st.spinner("Retrieving and generating answer..."):
        results = vector_db.similarity_search_with_score(query, k=top_k*3)
        # Filter by threshold and deduplicate
        unique_contexts = []
        seen = set()
        for doc, score in results:
            # For Chroma distances: lower is more similar. Filter out items with distance > threshold.
            if score is not None and score > threshold:
                continue
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                unique_contexts.append((doc, score))
            if len(unique_contexts) >= top_k:
                break
        if not unique_contexts:
            st.warning("Sorry, I cannot answer your question based on the available documents.")
        else:
            prompt = build_prompt(query, unique_contexts)
            if not groq_key:
                st.error("GROQ_API_KEY missing in .env")
            else:
                try:
                    from langchain_groq import ChatGroq
                    llm = ChatGroq(api_key=groq_key, model="llama-3.1-8b-instant")
                    response = llm.invoke(prompt)
                    # Only show the main answer content
                    answer_text = getattr(response, "content", None) or response.get("content", None) or str(response)
                    logger.info(f"Query: {query}\nAnswer: {answer_text}")
                    st.subheader("Answer")
                    st.write(answer_text)
                except Exception as e:
                    st.error(f"Groq API error: {e}")