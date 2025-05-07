from src.ngram import n_gram  # Importa a classe n_gram

##################################################################
# These functions are the different glue functions (they must be implemented). (Maybe we can put that in a different file like cohesion_metrics.py)
###################################################################

# Scp glue function
def scp_glue(ngram: n_gram, all_n_grams: dict[str, n_gram], total_count: int) -> float:
    """
    Compute the SCP cohesion score for an n-gram.
    Parameters:
        ngram (n_gram): the n-gram object
        all_n_grams (dict): all n-grams in the corpus
        total_count (int): total number of n-grams
    Returns:
        float: the SCP cohesion score between 0 and 1
    """
    return 0.0

# Dice glue function
def dice_glue(ngram: n_gram, all_n_grams: dict[str, n_gram]) -> float:
    """
    Compute the Dice cohesion score for an n-gram using FDPN (pseudo-2-gram splits).
    Parameters:
        ngram (n_gram): the n-gram object
        all_n_grams (dict): all n-grams in the corpus
    Returns:
        float: the Dice cohesion score between 0 and 1
    """
    return 0.0

# MI glue function
def mi_glue(ngram: n_gram, all_n_grams: dict[str, n_gram], total_count: int) -> float:
    """
    Compute the Mutual Information-based cohesion score for an n-gram using FDPN.
    Parameters:
        ngram (n_gram): the n-gram object
        all_n_grams (dict): all n-grams in the corpus
        total_count (int): total number of n-grams in the corpus
    Returns:
        float: the MI cohesion score
    """
    return 0.0