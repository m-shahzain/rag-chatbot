import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import chromadb
from config import *

print("Downloading website...")

response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")

for tag in soup(["script", "style", "noscript"]):
    tag.decompose()

text = soup.get_text(separator="\n", strip=True)

chunks = []

for i in range(0, len(text), CHUNK_SIZE):
    chunks.append(text[i:i + CHUNK_SIZE])

print("Chunks:", len(chunks))

model = SentenceTransformer(EMBEDDING_MODEL)

embeddings = model.encode(chunks).tolist()

client = chromadb.PersistentClient(path=DB_PATH)

try:
    client.delete_collection(COLLECTION_NAME)
except:
    pass

collection = client.create_collection(COLLECTION_NAME)

collection.add(
    ids=[str(i) for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings
)
print("Documents:", collection.count())

print("Database Created Successfully!")