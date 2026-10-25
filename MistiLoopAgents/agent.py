from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama


class TaskState(TypedDict):
    task: str
    plan: str
    implementation: str


model = ChatOllama(
    model="qwen2.5-coder:3b",
    temperature=0
)


def orchestrator(state: TaskState):
    response = model.invoke([
        (
            "system",
            "You are the MistiLoop Orchestrator. "
            "Break the requested development task into "
            "clear implementation steps and requirements."
        ),
        ("human", state["task"])
    ])

    return {"plan": response.content}


def code_writer(state: TaskState):
    response = model.invoke([
        (
            "system",
            "You are the MistiLoop Code Writer. "
            "Propose a NestJS implementation using "
            "PostgreSQL and Prisma where appropriate. "
            "Include relevant code and tests. "
            "Do not claim to have executed the code."
        ),
        (
            "human",
            f"Task: {state['task']}\n"
            f"Implementation plan:\n{state['plan']}"
        )
    ])

    return {"implementation": response.content}


workflow = StateGraph(TaskState)

workflow.add_node("orchestrator", orchestrator)
workflow.add_node("code_writer", code_writer)

workflow.add_edge(START, "orchestrator")
workflow.add_edge("orchestrator", "code_writer")
workflow.add_edge("code_writer", END)

app = workflow.compile()

result = app.invoke({
    "task": "Create a product listing API with "
            "add product, get all products, "
            "and validate product name and price.",
    "plan": "",
    "implementation": ""
})

print("IMPLEMENTATION PLAN")
print(result["plan"])

print("\nPROPOSED CODE")
print(result["implementation"])