#!/usr/bin/env python3
# tests/test_stopwords.py

from src.stopwords import (
    count_syllables,
    EXCEPTIONS,
    extract_bigram_neighbors,
    compute_neigsyl,
    find_elbow,
)
from src.text_processing import read_text_files

def test_count_syllables():
    # Test 1: Simple word with silent 'e'
    word1 = "house"      # 1 syllable
    result1 = count_syllables(word1)
    assert result1 == 1, f"Test 1 failed: {word1} -> {result1} (expected 1)"

    # Test 2: Loanword override via EXCEPTIONS
    assert "cafe" in EXCEPTIONS, "cafe must be in EXCEPTIONS map"
    result2 = count_syllables("cafe")
    assert result2 == EXCEPTIONS["cafe"], f"Test 2 failed: cafe -> {result2} (expected {EXCEPTIONS['cafe']})"

    # Test 3: Consecutive vowels but not collapsed diphthong
    result3 = count_syllables("aerial")  # a-e-ri-al
    assert result3 == 3, f"Test 3 failed: aerial -> {result3} (expected 3)"

    # Test 4: Another loanword override
    assert "resume" in EXCEPTIONS, "resume must be in EXCEPTIONS map"
    result4 = count_syllables("resume")
    assert result4 == EXCEPTIONS["resume"], f"Test 4 failed: resume -> {result4} (expected {EXCEPTIONS['resume']})"

    # Test 5: True diphthong collapse
    result5 = count_syllables("train")   # train
    assert result5 == 1, f"Test 5 failed: train -> {result5} (expected 1)"

    # Test 6: Longer multisyllable word
    result6 = count_syllables("mathematics")
    assert result6 == 4, f"Test 6 failed: mathematics -> {result6} (expected 4)"

    print("✅ count_syllables tests passed.")

from src.text_processing import read_text_files
from src.stopwords import (
    get_nltk_stopwords_in_corpus,
    extract_bigram_neighbors,
    compute_neigsyl,
    find_elbow
)

# Parameter sets to compare
PARAMS = [
    (3, -0.6, 0.15),
    (3, -0.8, 0.05),
    (5, -0.8, 0.05),
    (3, -0.7, 0.10),
    (3, -0.5, 0.15),
    (3, -0.6, 0.10),
    (3, -0.7, 0.05),
]

# Define test corpora
TEST_CORPORA = [
    ("Test1", read_text_files("./data/corpus2mw")),
    ("Test2", {"text": (
        "Although the weather was cold and the wind was strong, the children decided to go outside "
        "and play in the snow until they became tired and returned home."
    )}),
    ("Test3", {"text": (
        "When the old professor entered the lecture hall and saw that the students had already "
        "taken their seats, he smiled, adjusted his glasses, and walked to the front of the room "
        "before beginning to explain the complex theory that would challenge their understanding of "
        "physics more than anything they had studied so far."
    )}),
]

for test_name, corpus in TEST_CORPORA:
    print(f"\n===== {test_name} =====")
    # Prepare neigsyl_scores
    texts = corpus.values() if isinstance(corpus, dict) else []
    texts = corpus.values()  # covers both dict[str:str] and read_text_files
    bigrams = extract_bigram_neighbors(texts)
    # Build word set
    words = set()
    for t in texts:
        for w in t.split():
            clean = w.lower().strip(".,!?;:\"'()[]")
            if clean:
                words.add(clean)
    neigsyl_scores = compute_neigsyl(words, bigrams)

    # NLTK stopwords
    nltk_sw = set(get_nltk_stopwords_in_corpus(corpus))
    print(f"NLTK: {len(nltk_sw)} stopwords -> {sorted(nltk_sw)}")

    # Compare for each parameter set
    for delta_k, target_slope, tol in PARAMS:
        sw = find_elbow(neigsyl_scores, delta_k=delta_k,
                        target_slope=target_slope, tolerance=tol)
        sw_set = set(sw)
        inter = sw_set & nltk_sw
        extra = sw_set - nltk_sw
        print(
            f"Params Δk={delta_k}, slope={target_slope}, tol={tol}: {len(sw)} -> "
            f"Overlap {len(inter)}, Extra {len(extra)}"
        )