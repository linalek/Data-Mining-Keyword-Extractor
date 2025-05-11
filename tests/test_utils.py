from src.ngram import n_gram
from src.utils import get_element, calculate_and_store_glue

###################################### Test Cases ###################################

def test_get_element():
    print("Testing get_element...")
    tokens1 = ["a", "b"]
    tokens2 = ["c", "d"]
    ngrams = {
        "a b": n_gram(size=2, frequency=1, tokens=tokens1),
        "c d": n_gram(size=2, frequency=1, tokens=tokens2),
    }

    result = get_element(tokens1, ngrams)
    assert result is not None, "get_element failed: Expected a valid n_gram."
    assert result.get_tokens() == tokens1, f"get_element failed: Expected tokens {tokens1}, got {result.get_tokens()}."

    result = get_element(["x", "y"], ngrams)
    assert result is None, "get_element failed: Expected None for non-existing tokens."

    print("get_element: OK")


def test_calculate_and_store_glue():
    print("Testing calculate_and_store_glue...")
    tokens1 = ["a", "b", "c"]
    tokens2 = ["a", "b"]
    tokens3 = ["b", "c"]

    all_n_grams = {
        "a b c": n_gram(size=3, frequency=1, tokens=tokens1),
        "a b": n_gram(size=2, frequency=2, tokens=tokens2),
        "b c": n_gram(size=2, frequency=3, tokens=tokens3),
    }

    stop_words = ["a"]
    glue_function = "scp"

    updated_ngrams = calculate_and_store_glue(all_n_grams, glue_function, stop_words)

    # Verify glue values are calculated and stored for valid n-grams
    trigram = updated_ngrams["a b c"]
    bigram1 = updated_ngrams["a b"]
    bigram2 = updated_ngrams["b c"]

    assert trigram.get_glue_n_grams_minus_1() != {}, "calculate_and_store_glue failed: No glue values for minus_1."
    assert bigram2.get_glue_n_grams_plus_1() != {}, "calculate_and_store_glue failed: No glue values for plus_1."

    print("calculate_and_store_glue: OK")

    ####### Test the LocalMax Algorithm #######
    ng = all_n_grams.values()
    for n in ng:
        n.localMax()
        print(n.is_relevant_expression())
        

if __name__ == "__main__":
    test_get_element()
    test_calculate_and_store_glue()