from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_prompt(file_name):

    return (
        PROMPTS_DIR
        .joinpath(file_name)
        .read_text(encoding="utf-8")
    )