# import os
# import asyncio
# import streamlit as st
# from dotenv import load_dotenv
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# from langchain.chains import RetrievalQA
# from langchain.prompts import PromptTemplate
# from src import vector_store, embedder

# # --- Ensure event loop exists (fix for Python 3.13 + Streamlit threads) ---
# try:
#     asyncio.get_event_loop()
# except RuntimeError:
#     asyncio.set_event_loop(asyncio.new_event_loop())

# load_dotenv()

# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/embedding-001",
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-pro",
#     temperature=0,
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )

# CATEGORY_INDEXES = {
#     "HR": "data/embeddings/hr",
#     "Offline Reports": "data/embeddings/offline_reports",
#     "Online Reports": "data/embeddings/online_reports",
#     "Videos": "data/embeddings/videos"
# }

# prompt_template = """
# You are a helpful assistant. Based on the retrieved context,
# list every matching result without omitting any.
# If multiple matches exist, return them as a bullet list.

# Context:
# {context}

# Question:
# {question}

# Answer:
# """
# PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# def query_category(category, query):
#     index_path = CATEGORY_INDEXES[category]
#     if category == "Videos":
#         index_file = os.path.join(index_path, "index.faiss")
#         chunks_file = os.path.join(index_path, "chunks.npy")
#         if not os.path.exists(index_file):
#             return "❌ No video index found."
#         index, chunks = vector_store.load_embeddings(index_file, chunks_file)
#         query_vec = embedder.embed_query(query)
#         retrieved = vector_store.search(query_vec, index, chunks, top_k=10)
#         context = "\n".join([r[0] for r in retrieved])
#         return f"📄 Context:\n{context}"
#     else:
#         if not os.path.exists(index_path):
#             return f"❌ No index found for {category}"
#         db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
#         retriever = db.as_retriever(search_kwargs={"k": 15})
#         qa_chain = RetrievalQA.from_chain_type(
#             llm=llm,
#             retriever=retriever,
#             chain_type_kwargs={"prompt": PROMPT}
#         )
#         return qa_chain.run(query)

# # ---- Streamlit UI ----
# st.set_page_config(page_title="Multi-Modal RAG", page_icon="🤖", layout="centered")
# st.title("🎙️📂 Multi-Modal RAG Chatbot")

# category = st.selectbox("Select Category", list(CATEGORY_INDEXES.keys()))
# query = st.text_input("Ask your question:")

# if query:
#     with st.spinner(f"Searching in {category} knowledge base..."):
#         answer = query_category(category, query)
# #         st.write("**Answer:**", answer)
# import os
# import asyncio
# import streamlit as st
# from dotenv import load_dotenv
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# from langchain.chains import RetrievalQA
# from langchain.prompts import PromptTemplate
# from src import vector_store, embedder

# # --- Ensure event loop exists (Python 3.13 + Streamlit fix) ---
# try:
#     asyncio.get_running_loop()
# except RuntimeError:
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)

# load_dotenv()

# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/embedding-001",
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-pro",
#     temperature=0,
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )

# CATEGORY_INDEXES = {
#     "HR": "faiss_index_hr",
#     "Offline Reports": "faiss_index_offline_reports",
#     "Online Reports": "faiss_index_online_reports",
#     "Videos": "data/embeddings/videos"
# }

# prompt_template = """
# You are a helpful assistant. Based on the retrieved context,
# list every matching result without omitting any.
# If multiple matches exist, return them as a bullet list.

# Context:
# {context}

# Question:
# {question}

# Answer:
# """
# PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# def query_category(category, query):
#     index_path = CATEGORY_INDEXES[category]

#     if category == "Videos":
#         index_file = os.path.join(index_path, "index.faiss")
#         chunks_file = os.path.join(index_path, "chunks.npy")
#         if not os.path.exists(index_file):
#             return "❌ No video index found. Please build it first."
#         index, chunks = vector_store.load_embeddings(index_file, chunks_file)
#         query_vec = embedder.embed_query(query)
#         retrieved = vector_store.search(query_vec, index, chunks, top_k=10)
#         context = "\n".join([r[0] for r in retrieved])
#         return f"📄 Context:\n{context}"
#     else:
#         if not os.path.exists(index_path):
#             return f"❌ No index found for {category}. Please build it first."
#         db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
#         retriever = db.as_retriever(search_kwargs={"k": 30})
#         qa_chain = RetrievalQA.from_chain_type(
#             llm=llm,
#             retriever=retriever,
#             chain_type_kwargs={"prompt": PROMPT}
#         )
#         return qa_chain.run(query)

# # ---- Streamlit UI ----
# st.set_page_config(page_title="Multi-Modal RAG", page_icon="🤖", layout="centered")
# st.title("🎙️📂 Multi-Modal RAG Chatbot")

# category = st.selectbox("Select Category", list(CATEGORY_INDEXES.keys()))
# query = st.text_input("Ask your question:")

# if query:
#     with st.spinner(f"🔍 Searching in {category} knowledge base..."):
#         answer = query_category(category, query)
#         st.write("**Answer:**", answer)
import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src import vector_store, embedder

# --- Ensure event loop exists (Python 3.13 + Streamlit fix) ---
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

CATEGORY_INDEXES = {
    "HR": "faiss_index_hr",
    "Offline Reports": "faiss_index_offline_reports",
    "Online Reports": "faiss_index_online_reports",
    "Videos": "data/embeddings/videos"
}

# category-specific k values
CATEGORY_K = {
    "HR": 10,
    "Offline Reports": 50,
    "Online Reports": 50,
    "Videos": 20
}

prompt_template = """
You are a helpful assistant. Based on the retrieved context,
list every matching result without omitting any.
If multiple matches exist, return them as a bullet list.

Context:
{context}

Question:
{question}

Answer:
"""
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

def query_category(category, query):
    index_path = CATEGORY_INDEXES[category]
    k = CATEGORY_K[category]  # fetch k value

    if category == "Videos":
        index_file = os.path.join(index_path, "index.faiss")
        chunks_file = os.path.join(index_path, "chunks.npy")
        if not os.path.exists(index_file):
            return "❌ No video index found. Please build it first."
        index, chunks = vector_store.load_embeddings(index_file, chunks_file)
        query_vec = embedder.embed_query(query)
        retrieved = vector_store.search(query_vec, index, chunks, top_k=k)
        context = "\n".join([r[0] for r in retrieved])
        return f"📄 Context:\n{context}"
    else:
        if not os.path.exists(index_path):
            return f"❌ No index found for {category}. Please build it first."
        db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        retriever = db.as_retriever(search_kwargs={"k": k})
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type_kwargs={"prompt": PROMPT}
        )
        return qa_chain.run(query)

# ---- Streamlit UI ----
st.set_page_config(page_title="Multi-Modal RAG", page_icon="🤖", layout="centered")
st.title("🎙️📂 Multi-Modal RAG Chatbot")

category = st.selectbox("Select Category", list(CATEGORY_INDEXES.keys()))
query = st.text_input("Ask your question:")

if query:
    with st.spinner(f"🔍 Searching in {category} knowledge base... (k={CATEGORY_K[category]})"):
        answer = query_category(category, query)
        st.write("**Answer:**", answer)
