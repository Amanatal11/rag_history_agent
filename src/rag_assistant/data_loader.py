import os
from typing import List

def list_text_files(data_dir: str) -> List[str]:
    return [
        os.path.join(data_dir, fname)
        for fname in os.listdir(data_dir)
        if fname.endswith(".txt")
    ]

