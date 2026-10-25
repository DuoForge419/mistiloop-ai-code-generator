
from langchain_ollama import ChatOllama
from project_context import get_project_context


model = ChatOllama(
    model="qwen2.5-coder:3b",
    temperature=0
)


def create_plan(task: str) -> str:
    project_context = get_project_context()

    messages = [
        (
            "system",
            """
You are the Orchestrator Agent for MistiLoop Crochet.

Your responsibility is to analyze development tasks and
create implementation plans.

Rules:
1. Use the supplied project context.
2. Respect the existing technology stack and conventions.
3. Identify relevant files and files that may need to be created.
4. Break the task into clear, ordered steps.
5. Identify validation and testing requirements.
6. Do not claim to have modified files or executed tests.
7. If essential project information is missing, state the
   assumptions that need verification.

Return your response using these headings:
- Task Understanding
- Relevant Existing Files
- Implementation Plan
- Validation and Testing
- Assumptions and Risks
"""
        ),
        (
            "human",
            f"""
DEVELOPMENT TASK:
{task}

PROJECT CONTEXT:
{project_context}
"""
        )
    ]

    response = model.invoke(messages)
    return response.content


if __name__ == "__main__":
    task = input("Enter your MistiLoop development task: ")

    if not task.strip():
        print("Please enter a development task.")
    else:
        print("\nGenerating implementation plan...\n")
        plan = create_plan(task)

        print("=" * 60)
        print("ORCHESTRATOR PLAN")
        print("=" * 60)
        print(plan)
