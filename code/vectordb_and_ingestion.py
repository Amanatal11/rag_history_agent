import os
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from code.logger import logger


class VectorDBManager:
    """Handles chunking, embedding, and persistent vector DB."""

    def __init__(self, data_dir="data", persist_dir="chroma_db", collection_name="ethiopian_history"):
        self.data_dir = data_dir
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_db = None

    def embed_and_insert(self, chunk_size=1000, chunk_overlap=200):
        """Chunk and embed all .txt files in data_dir, insert into ChromaDB."""
        docs = []
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        for fname in os.listdir(self.data_dir):
            if fname.endswith(".txt"):
                path = os.path.join(self.data_dir, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read()
                    if not text.strip():
                        logger.warning(f"Empty file: {fname}")
                        continue
                    chunks = splitter.split_text(text)
                    for i, chunk in enumerate(chunks):
                        doc_id = f"{fname}_{i}"
                        docs.append(Document(page_content=chunk, metadata={"filename": fname, "chunk_id": i, "id": doc_id}))
                except Exception as e:
                    logger.error(f"Error reading {fname}: {e}")
        if docs:
            self.vector_db = Chroma.from_documents(
                docs,
                embedding=self.embeddings,
                persist_directory=self.persist_dir,
                collection_name=self.collection_name
            )
            self.vector_db.persist()
            logger.info(f"Inserted {len(docs)} chunks into ChromaDB collection '{self.collection_name}'.")
        else:
            logger.warning("No valid .txt files found for embedding.")

    def load_db(self):
        """Load the vector DB from disk."""
        if not self.vector_db:
            try:
                self.vector_db = Chroma(
                    persist_directory=self.persist_dir,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
                logger.info("Loaded Chroma vector DB from disk.")
            except Exception as e:
                logger.error(f"Failed to load Chroma DB: {e}")

    def get_vector_db(self):
        if not self.vector_db:
            self.load_db()
        return self.vector_db

