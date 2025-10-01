import os
from typing import List


def list_text_files(data_dir: str) -> List[str]:
    """List all .txt files in the given data directory."""
    return [
        os.path.join(data_dir, fname)
        for fname in os.listdir(data_dir)
        if fname.endswith(".txt")
    ]

