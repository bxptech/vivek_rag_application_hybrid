import os
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader,
    JSONLoader
)
from src import sarvam, video2audio, embedder, vector_store
import glob

load_dotenv()
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

CATEGORY_FOLDERS = {
    "hr": "data/hr",
    "offline_reports": "data/offline_reports",
    "online_reports": "data/online_reports",
    "videos": "data/audio"
}

def load_all_docs_from_folder(folder_path):
    docs = []
    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        ext = file.lower()
        try:
            if ext.endswith(".pdf"):
                docs.extend(PyPDFLoader(path).load())
            elif ext.endswith(".docx") or ext.endswith(".doc"):
                docs.extend(UnstructuredWordDocumentLoader(path).load())
            elif ext.endswith(".xlsx"):
                docs.extend(UnstructuredExcelLoader(path).load())
            elif ext.endswith(".json"):
                docs.extend(JSONLoader(file_path=path, jq_schema=".[]", text_content=False).load())
        except Exception as e:
            print(f"⚠️ Could not load {file}: {e}")
    return docs

def build_doc_index(category, folder_path):
    docs = load_all_docs_from_folder(folder_path)
    if not docs:
        return
    splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    index_path = f"data/embeddings/{category}"
    os.makedirs(index_path, exist_ok=True)
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(index_path)
    print(f"✅ Index saved for {category}")

def build_video_index():
    video2audio.transcribe_video2_audio()
    files = glob.glob("data/audio/*.mp3")
    all_chunks = []
    for f in files:
        texts = sarvam.transcribe_audio(f)
        all_chunks.extend([t for t in texts if t.strip()])
    vectors = embedder.embed_chunks(all_chunks)
    vector_store.save_embeddings(vectors, all_chunks,
                                 f"data/embeddings/videos/index.faiss",
                                 f"data/embeddings/videos/chunks.npy")

if __name__ == "__main__":
    for cat, folder in CATEGORY_FOLDERS.items():
        if cat == "videos":
            build_video_index()
        else:
            build_doc_index(cat, folder)
