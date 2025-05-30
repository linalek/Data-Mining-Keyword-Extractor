import os
import tempfile
import shutil

from src.keywords import get_explicit_keywords, calculate_implicit_keywords

def test_get_explicit_keywords_simple():
    # Create a minimal temporary corpus
    corpus = {"doc1.txt": "cat dog cat", "doc2.txt": "dog bird cat"}
    relevant_expressions = ["cat dog"]
    stop_words = ["the", "a", "and"]
    total_keywords = 2

    # Create a temporary folder with corpus files
    tmp_dir = tempfile.mkdtemp()
    try:
        for fname, content in corpus.items():
            with open(os.path.join(tmp_dir, fname), "w", encoding="utf-8") as f:
                f.write(content)

        # Call the function
        result = get_explicit_keywords(
            corpus_path=tmp_dir,
            relevant_expressions=relevant_expressions,
            total_keywords=total_keywords,
            stop_words=stop_words
        )
        assert isinstance(result, dict)
        assert set(result.keys()) == set(corpus.keys())
        print("test_get_explicit_keywords_simple: OK")
    finally:
        shutil.rmtree(tmp_dir)


def test_calculate_implicit_keywords_simple():
    corpus = {"doc1.txt": "cat dog cat", "doc2.txt": "dog bird cat"}
    explicit_keywords = {
        "doc1.txt": ["cat", "dog"],
        "doc2.txt": ["dog", "bird"]
    }
    relevant_expressions = ["cat dog"]
    stop_words = set(["the", "a", "and"])
    num_implicit = 1

    tmp_dir = tempfile.mkdtemp()
    try:
        for fname, content in corpus.items():
            with open(os.path.join(tmp_dir, fname), "w", encoding="utf-8") as f:
                f.write(content)

        result = calculate_implicit_keywords(
            corpus_path=tmp_dir,
            explicit_keywords=explicit_keywords,
            relevant_expressions=relevant_expressions,
            num_implicit=num_implicit,
            stop_words=stop_words
        )
        assert isinstance(result, dict)
        assert set(result.keys()) == set(corpus.keys())
        print("test_calculate_implicit_keywords_simple: OK")
    finally:
        shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    test_get_explicit_keywords_simple()
    test_calculate_implicit_keywords_simple()