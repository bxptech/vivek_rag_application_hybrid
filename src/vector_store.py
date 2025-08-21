import os
import numpy as np
import faiss

def create_index(dim):
    return faiss.IndexFlatL2(dim)

def save_embeddings(vectors, chunks, index_file, chunks_file):
    vectors_np = np.array(vectors, dtype="float32")
    index = create_index(vectors_np.shape[1])
    index.add(vectors_np)

    os.makedirs(os.path.dirname(index_file), exist_ok=True)
    faiss.write_index(index, index_file)
    np.save(chunks_file, np.array(chunks, dtype=object))

def load_embeddings(index_file, chunks_file):
    index = faiss.read_index(index_file)
    chunks = np.load(chunks_file, allow_pickle=True)
    return index, chunks

def search(query_vector, index, chunks, top_k=5):
    query_vector = np.array(query_vector, dtype="float32").reshape(1, -1)
    D, I = index.search(query_vector, top_k)
    return [(chunks[i], float(D[0][j])) for j, i in enumerate(I[0])]
