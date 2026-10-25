from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent / "workspace"

ALLOWED_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx",
    ".json", ".md", ".prisma", ".sql",
    ".html", ".css", ".yml", ".yaml"
}

IGNORED_DIRS = {
    ".git", "node_modules", ".venv", "venv",
    "__pycache__", "dist", "build", ".next"
}

IGNORED_FILES = {
    ".env", ".env.local", ".env.production",
    "id_rsa", "id_ed25519"
}

MAX_FILES = 40
MAX_FILE_CHARS = 6000
MAX_TOTAL_CHARS = 20000


def get_project_context() -> str:
    """Read a bounded set of approved project files."""

    if not WORKSPACE.exists():
        raise FileNotFoundError(
            f"Workspace not found: {WORKSPACE}\n"
            "Create the workspace folder and add README.md."
        )

    sections = []
    total_chars = 0
    files_read = 0

    for path in sorted(WORKSPACE.rglob("*")):
        if not path.is_file():
            continue

        relative = path.relative_to(WORKSPACE)

        # Ignore generated and hidden directories.
        if any(
            part in IGNORED_DIRS or part.startswith(".")
            for part in relative.parts[:-1]
        ):
            continue

        if path.name in IGNORED_FILES:
            continue

        # Skip hidden files and files outside our allowlist.
        if path.name.startswith("."):
            continue

        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        if files_read >= MAX_FILES:
            break

        try:
            content = path.read_text(
                encoding="utf-8",
                errors="replace"
            )
        except OSError:
            continue

        content = content[:MAX_FILE_CHARS]

        remaining = MAX_TOTAL_CHARS - total_chars
        if remaining <= 0:
            break

        content = content[:remaining]

        sections.append(
            f"\n--- FILE: {relative.as_posix()} ---\n"
            f"{content}"
        )

        total_chars += len(content)
        files_read += 1

    if not sections:
        return "No approved project files found."

    return "\n".join(sections)


if __name__ == "__main__":
    print(get_project_context())
