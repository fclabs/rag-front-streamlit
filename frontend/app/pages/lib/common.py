import os
from typing import List, Tuple

def load_sample_files(path : str) -> Tuple[List[str], List[str]]:  
    files = os.listdir(path)
    ext = [f.split(".")[1] for f in files]
    return files, ext
