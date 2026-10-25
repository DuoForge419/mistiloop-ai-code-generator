from langchain_ollama import ChatOllama

model = ChatOllama(
    model="qwen2.5-coder:3b",
    temperature=0
)

response = model.invoke(
    "Design a simple NestJS product listing API."
)

print(response.content)