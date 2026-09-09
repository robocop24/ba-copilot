import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from document.document_processor import DocumentProcessor
from workflow import run_ba_workflow

BASE_DIR = Path(__file__).parent


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    # Silence noisy third-party loggers
    for lib in ("httpx", "httpcore", "openai", "langchain", "langgraph"):
        logging.getLogger(lib).setLevel(logging.WARNING)


def main() -> None:
    _setup_logging()

    requirement = DocumentProcessor().extract_text(BASE_DIR / "input/requirement.txt")

    result = run_ba_workflow(requirement)
    print(result)


if __name__ == "__main__":
    main()