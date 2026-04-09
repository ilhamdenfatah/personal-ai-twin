import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# ==============================
# CONFIG
# ==============================
KNOWLEDGE_DIR = "knowledge"
VECTORSTORE_DIR = "vectorstore"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def ingest():
    # ==============================
    # LOAD
    # ==============================
    print("📂 Loading knowledge files...")
    loader = DirectoryLoader(
        KNOWLEDGE_DIR,
        glob="**/*.*",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )
    documents = loader.load()
    print(f"✅ Loaded {len(documents)} files")

    # ==============================
    # CHUNK
    # ==============================
    print("\n✂️  Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")

    # ==============================
    # EMBED + STORE
    # ==============================
    print("\n🔢 Embedding and storing to ChromaDB...")
    print("⏳ First run will download the embedding model (~90MB)...")
    
    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
    )

    if os.path.exists(VECTORSTORE_DIR):
        shutil.rmtree(VECTORSTORE_DIR)
        print("🗑️  Cleared existing vectorstore")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=VECTORSTORE_DIR,
    )

    print(f"\n🎉 Done! {len(chunks)} chunks embedded and stored in '{VECTORSTORE_DIR}/'")

if __name__ == "__main__":
    ingest()