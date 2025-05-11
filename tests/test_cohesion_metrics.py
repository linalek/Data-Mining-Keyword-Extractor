from src.cohesion_metrics import scp_glue, dice_glue, mi_glue
from src.ngram import n_gram

# --------------------------- Helper to create test n-grams ---------------------------

def create_manual_n_grams():
    return {
        'Ola': n_gram(1, 5, ['Ola']),
        'seja': n_gram(1, 5, ['seja']),
        'bem-vindo': n_gram(1, 5, ['bem-vindo']),
        'Ola seja': n_gram(2, 3, ['Ola', 'seja']),
        'seja bem-vindo': n_gram(2, 4, ['seja', 'bem-vindo']),
        'bem-vindo ao': n_gram(2, 2, ['bem-vindo', 'ao']),
        'the': n_gram(1, 100, ['the']),
        'quick': n_gram(1, 80, ['quick']),
        'brown': n_gram(1, 70, ['brown']),
        'fox': n_gram(1, 90, ['fox']),
        'the quick': n_gram(2, 60, ['the', 'quick']),
        'quick brown': n_gram(2, 50, ['quick', 'brown']),
        'brown fox': n_gram(2, 40, ['brown', 'fox']),
        'the quick brown': n_gram(3, 30, ['the', 'quick', 'brown']),
        'quick brown fox': n_gram(3, 25, ['quick', 'brown', 'fox']),
    }

# --------------------------- Run test cases ---------------------------

def run_tests():
    all_n_grams = create_manual_n_grams()
    total_count = sum(ng.get_frequency() for ng in all_n_grams.values())

    test_phrases = ['seja bem-vindo', 'Ola seja', 'the quick brown', 'quick brown fox']

    for phrase in test_phrases:
        print(f"\nTesting n-gram: '{phrase}'")
        ngram = all_n_grams[phrase]

        scp = scp_glue(ngram, all_n_grams, total_count)
        dice = dice_glue(ngram, all_n_grams)
        mi = mi_glue(ngram, all_n_grams, total_count)

        print(f"SCP: {scp:.5f}")
        print(f"Dice: {dice:.5f}")
        print(f"MI: {mi:.5f}")

# --------------------------- Execute ---------------------------

if __name__ == "__main__":
    run_tests()