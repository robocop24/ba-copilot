from pathlib import Path


def load_and_chunk(file_path: str) -> list:
    content = Path(file_path).read_text(encoding="utf-8")

    chunks = [
        chunk.strip()
        for chunk in content.split("\n\n")
        if chunk.strip()
    ]

    return chunks