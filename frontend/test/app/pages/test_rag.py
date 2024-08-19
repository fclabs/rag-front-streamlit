
from app.pages.common import load_sample_files

def test_load_sample_files():
    files, ext = load_sample_files("app/sample_files")
    
    assert files and ext
    assert len(files) == len(ext)
    assert all([f for f in files])
    assert all([f for f in ext])
    assert all([files[i].endswith(e) for i,e in enumerate(ext)])
    assert all(['.' not in e for e in ext])