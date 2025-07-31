# pytest test suite for lines_of_py.py

import os
import fnmatch
import pytest
from lines_of_py import find_files, count_lines, generate_histogram, shorten_path

def test_find_files_basic(tmp_path):
    d = tmp_path / "proj"
    d.mkdir()
    (d / "a.py").write_text("print('hello')")
    (d / "b.txt").write_text("nope")
    files = find_files(str(d), [], ["py"])
    assert len(files) == 1
    assert files[0].endswith("a.py")

def test_find_files_multiple_exts(tmp_path):
    d = tmp_path / "proj"
    d.mkdir()
    (d/"a.py").write_text("")
    (d/"b.js").write_text("")
    (d/"c.sh").write_text("")
    files = find_files(str(d), [], ["py","js"])
    assert any(f.endswith("a.py") for f in files)
    assert any(f.endswith("b.js") for f in files)
    assert all(not f.endswith("c.sh") for f in files)

def test_exclude_dirs(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    keep = root / "keep"; keep.mkdir()
    skip = root / "skip_me"; skip.mkdir()
    (keep/"f.py").write_text("x")
    (skip/"g.py").write_text("y")
    files = find_files(str(root), ["skip_me"], ["py"])
    assert files == [str(keep/"f.py")]

def test_empty_directory(tmp_path):
    # No files present
    files = find_files(str(tmp_path), [], ["py"])
    total, raw, filt = count_lines(files)
    assert total == 0
    assert raw == {}
    assert filt == {}
    assert generate_histogram(raw, limit=5) == []

def test_count_lines_and_duplicates(tmp_path):
    # create two py files with duplicate line
    f1 = tmp_path / "a.py"
    f1.write_text("line1\nline2\n")
    f2 = tmp_path / "b.py"
    f2.write_text("line2\nline3\n")
    files = [str(f1), str(f2)]
    total_raw, raw, filt = count_lines(files, ignore_duplicates=False)
    assert total_raw == 4
    total_uniq, raw2, filt2 = count_lines(files, ignore_duplicates=True)
    assert total_uniq == 3  # line2 counted once

def test_shorten_path_short():
    p = "/a/b.py"
    assert shorten_path(p, max_len=20) == p

def test_shorten_path_long():
    parts = ["folder"] * 10 + ["file.py"]
    path = "/" + "/".join(parts)
    s = shorten_path(path, max_len=30)
    assert s.startswith(".../")
    assert len(s) <= 30

def test_hist_limit_zero():
    counts = {"a.py": 3, "b.py": 1}
    assert generate_histogram(counts, limit=0) == []

def test_hist_limit_overflow():
    counts = {"a.py":3, "b.py":1}
    hist = generate_histogram(counts, limit=10)
    assert len(hist) == 2
    assert "a.py" in hist[0]
    assert "b.py" in hist[1]

