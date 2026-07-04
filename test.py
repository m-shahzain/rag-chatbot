import ollama
import time

start = time.time()

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "What is Python?"
        }
    ]
)

print(response["message"]["content"])
print("Time:", time.time() - start)