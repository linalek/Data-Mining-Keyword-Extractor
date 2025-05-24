from src.text_processing import text_processing,read_text_files, add_spaces, tokenize_text
from src.ngram import *
from src.stopwords import get_stop_words, get_nltk_stopwords_in_corpus
from src.utils import calculate_and_store_glue,extract_random_relevant_expressions, ask_is_RE
from src.evaluation_metrics import precision,recall,f1_score

def extractor(path:str) -> dict[str:n_gram]:
    # Preprocessing
    tokens:list[str] = text_processing(path)
    #print(tokens)

    # Stopwords
    #######################################################################################
    # Still using the python library due to the need of imporvement in our algorithm
    #######################################################################################
    stop_words:list[str] = get_nltk_stopwords_in_corpus(read_text_files(path))
    #print(stop_words)

    # Building n-grams
    ngram_dict:dict[str:n_gram] = create_n_grams(tokens,stop_words)
    #print(ngram_dict)

    # Glue values updated in each n-gram
    ngram_dict:dict[str:n_gram] = calculate_and_store_glue(ngram_dict, "dice", stop_words)
    #print(ngram_dict)

    # Calculate Relevant Expressions
    for n_gram in ngram_dict.values():
        n_gram.localMax()
    
    return ngram_dict


def evaluation(relevant_expressions:list[str]) -> None:
    """
    Evaluates the performance of the LocalMaxs algorithm by calculating precision, recall and f1.
    Parameters:
        total_list (dict[str, n_gram]): Dictionary of n-grams.
        relevant_expressions (list[str]): List of expressions identified as relevant.
    Returns:
        None
    """

    # Compute the precision of the algorithm
    print("The list of relevant expressions is:", relevant_expressions)
    real_RE:list[bool] = []

    # True positives: relevant expressions that were identified and False positives: relevant expressions that were not identified by the user
    true_positive:int = 0
    false_positive:int = 0

    for expr in relevant_expressions:
        is_re:bool = ask_is_RE(expr)
        real_RE.append(is_re)

    for i in range(len(relevant_expressions)):
        if real_RE[i]:
            true_positive += 1
        else:
            false_positive += 1

    precision_value:float = precision(float(true_positive), float(false_positive))
    print("The precision of our LocalMaxs algorithm is:", precision_value )

    # Compute the recall
    # False negatives: real relevant expressions that were not identified
    false_negative:int = len(real_RE) - len(relevant_expressions)
    recall_value:float = recall(float(true_positive), float(false_negative))
    print("The recall of our LocalMaxs algorithm is:", recall_value )

    # Compute the f1
    f1_value:float = f1_score(precision_value,recall_value)
    print("The f1_score of our LocalMaxs algorithm is:", f1_value )



def main() -> None:    
    total_list:dict[str:n_gram] = extractor("../corpus2mw")
    relevant_expressions:list[str] = extract_random_relevant_expressions(total_list)
    evaluation(relevant_expressions)


if __name__ == "__main__":
    main()
