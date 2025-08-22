import os
import asyncio
import numpy as np
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# --- Ensure event loop exists (fix for Python 3.13 + Streamlit threads) ---
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

load_dotenv()

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def embed_chunks(chunks):
    vectors = embedding_model.embed_documents(chunks)
    return np.array(vectors, dtype="float32")

def embed_query(query):
    vector = embedding_model.embed_query(query)
    return np.array(vector, dtype="float32")
