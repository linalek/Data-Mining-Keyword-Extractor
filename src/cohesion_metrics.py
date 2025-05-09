## Function to compute SCP cohesion score for an n-gram
from math import log2


def scp_glue(ngram, all_n_grams, total_count: int) -> float:
    """
    SCP(w1 w2) = (P(w1w2))^2 / (P(w1) * P(w2))
    """
    tokens = ngram.get_tokens()
    if len(tokens) < 2:
        return 0.0
    left = " ".join(tokens[:-1])
    right = " ".join(tokens[1:])

    freq_full = ngram.get_frequency()
    freq_left = all_n_grams[left].get_frequency() if left in all_n_grams else 1
    freq_right = all_n_grams[right].get_frequency() if right in all_n_grams else 1

    prob_full = freq_full / total_count
    prob_left = freq_left / total_count
    prob_right = freq_right / total_count

    scp = (prob_full ** 2) / (prob_left * prob_right) if prob_left * prob_right > 0 else 0.0
    return scp

## Function to compute Dice coefficient for an n-gram
def dice_glue(ngram, all_n_grams) -> float:
    """
    Dice(w1 w2) = 2 * freq(w1 w2) / (freq(w1) + freq(w2))
    """
    tokens = ngram.get_tokens()
    if len(tokens) < 2:
        return 0.0
    left = " ".join(tokens[:-1])
    right = " ".join(tokens[1:])

    freq_full = ngram.get_frequency()
    freq_left = all_n_grams[left].get_frequency() if left in all_n_grams else 1
    freq_right = all_n_grams[right].get_frequency() if right in all_n_grams else 1

    denominator = freq_left + freq_right
    dice = (2 * freq_full) / denominator if denominator > 0 else 0.0
    return dice

## Function to compute Mutual Information for an n-gram
def mi_glue(ngram, all_n_grams, total_count: int) -> float:
    """
    MI(w1 w2) = log2(P(w1 w2) / (P(w1) * P(w2)))
    """
    tokens = ngram.get_tokens()
    if len(tokens) < 2:
        return 0.0
    left = " ".join(tokens[:-1])
    right = " ".join(tokens[1:])

    freq_full = ngram.get_frequency()
    freq_left = all_n_grams[left].get_frequency() if left in all_n_grams else 1
    freq_right = all_n_grams[right].get_frequency() if right in all_n_grams else 1

    prob_full = freq_full / total_count
    prob_left = freq_left / total_count
    prob_right = freq_right / total_count

    denominator = prob_left * prob_right
    if denominator > 0 and prob_full > 0:
        mi = log2(prob_full / denominator)
        return mi
    else:
        return 0.0