import chromadb
import ollama
from sentence_transformers import SentenceTransformer
from config import *

model = SentenceTransformer(EMBEDDING_MODEL)

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_collection(COLLECTION_NAME)


def ask_rag(question):

    question_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )


    print("Retrieved documents:", len(results["documents"][0]))

    for i, doc in enumerate(results["documents"][0]):
        print(f"Chunk {i}: {len(doc)} characters")
    

    context = "\n\n".join(results["documents"][0])

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You are a helpful assistant.

Answer ONLY from the provided context.

If the answer is not found, say:
'I don't know based on the provided context.'
"""
            },
            {
                "role": "user",
                "content": f"""
Context:

{context}

Question:

{question}
"""
            }
        ]
    )

    return response["message"]["content"]