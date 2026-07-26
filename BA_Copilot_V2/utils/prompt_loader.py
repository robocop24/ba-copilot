from pathlib import Path

def load_prompt(file_name):
    
    return(
        Path("prompts")
        .joinpath(file_name)
        .read_text(encoding="utf-8")
    )