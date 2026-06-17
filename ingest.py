"""
ingest.py — Run this ONCE before starting the app
Usage: python ingest.py
"""

import os
import shutil
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

KNOWLEDGE_BASE_PATH = "data/knowledge_base.txt"
VECTORSTORE_DIR     = "vectorstore"
EMBED_MODEL         = "all-MiniLM-L6-v2"

def ingest():
    print("📄 Loading knowledge base...")
    loader = TextLoader(KNOWLEDGE_BASE_PATH, encoding="utf-8")
    documents = loader.load()
    print(f"   → Loaded {len(documents)} document(s)")

    print("✂️  Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
    )
    chunks = splitter.split_documents(documents)
    print(f"   → {len(chunks)} chunks created")

    if len(chunks) == 0:
        print("❌ No chunks created! Check that knowledge_base.txt has content.")
        return

    print("🔢 Loading embedding model (downloads ~90MB on first run)...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"}
    )

    print("💾 Building ChromaDB vector store...")
    if os.path.exists(VECTORSTORE_DIR):
        shutil.rmtree(VECTORSTORE_DIR)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTORSTORE_DIR
    )
    print(f"✅ Done! {len(chunks)} chunks stored in ./{VECTORSTORE_DIR}/")
    print("\n🚀 Now run: streamlit run app.py")

if __name__ == "__main__":
    ingest()