
from pathlib import Path

# Resolve the workspace relative to this script,
# not relative to the terminal's current directory.
WORKSPACE = (Path(__file__).resolve().parent / "workspace").resolve()

ALLOWED_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx",
    ".json", ".md", ".prisma", ".sql",
    ".html", ".css", ".yml", ".yaml"
}

BLOCKED_NAMES = {
    ".env", ".env.local", ".env.production",
    "id_rsa", "id_ed25519"
}

BLOCKED_DIRS = {
    ".git", ".venv", "venv", "node_modules",
    "__pycache__", "dist", "build"
}


def write_file(relative_path: str, content: str) -> str:
    """Create a new file inside workspace without overwriting."""

    if not isinstance(relative_path, str) or not relative_path.strip():
        raise ValueError("A relative file path is required.")

    if not isinstance(content, str):
        raise ValueError("File content must be a string.")

    requested = Path(relative_path)

    # Reject absolute paths and Windows drive paths.
    if requested.is_absolute() or requested.drive:
        raise ValueError("Absolute paths are not allowed.")

    # Treat both slash styles as path separators.
    parts = relative_path.replace("\\", "/").split("/")

    if any(part in ("", ".", "..") for part in parts):
        raise ValueError("Invalid path component.")

    if any(part.startswith(".") for part in parts):
        raise ValueError("Hidden paths are not allowed.")

    if any(part.lower() in BLOCKED_DIRS for part in parts[:-1]):
        raise ValueError("Writing to this directory is not allowed.")

    filename = parts[-1]

    if filename.lower() in BLOCKED_NAMES:
        raise ValueError("Writing to this file is not allowed.")

    if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("File extension is not allowed.")

    # Resolve the destination to detect traversal and existing
    # symbolic links that point outside the workspace.
    target = (WORKSPACE / Path(*parts)).resolve()

    try:
        target.relative_to(WORKSPACE)
    except ValueError:
        raise ValueError("Destination is outside workspace.")

    # Only create new files in this step.
    if target.exists():
        raise FileExistsError(
            f"{relative_path} already exists. "
            "Existing files will not be overwritten."
        )

    # Create parent directories only after path validation.
    target.parent.mkdir(parents=True, exist_ok=True)

    # Exclusive creation prevents silently replacing an existing file.
    try:
        with target.open("x", encoding="utf-8", newline="\n") as file:
            file.write(content)
    except FileExistsError:
        raise FileExistsError(
            f"{relative_path} already exists."
        )

    return f"Created successfully: {relative_path}"


if __name__ == "__main__":
    print(f"Workspace: {WORKSPACE}")
    print("Safe file writer is ready.")
