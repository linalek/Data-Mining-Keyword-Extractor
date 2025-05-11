from src.text_processing import text_processing,read_text_files, add_spaces, tokenize_text
from src.ngram import *
from src.stopwords import get_stop_words, get_nltk_stopwords_in_corpus
from src.utils import calculate_and_store_glue,extract_random_relevant_expressions

def extractor() -> dict[str:n_gram]:
    # Preprocessing
    tokens:list[str] = text_processing("../test")
    print(tokens)

    # Stopwords
    #######################################################################################
    # Still using the python library due to the need of imporvement in our algorithm
    #######################################################################################
    stop_words:list[str] = get_nltk_stopwords_in_corpus(read_text_files("../test"))
    #print(stop_words)

    # Building n-grams
    ngram_dict:dict[str:n_gram] = create_n_grams(tokens,stop_words)
    print(ngram_dict)

    # Glue values updated in each n-gram
    ngram_dict2:dict[str:n_gram] = calculate_and_store_glue(ngram_dict, "dice", stop_words)
    print(ngram_dict2)

    # Calculate Relevant Expressions
    ngram_dict3:dict[str:n_gram] = ngram_dict2.values()
    for n_gram in ngram_dict3:
        n_gram.localMax()
    
    return ngram_dict3


def evaluation(total_list:dict[str:n_gram],relevant_expressions:list[str]):
     return


def main():    
    total_list:dict[str:n_gram] = extractor()
    relevant_expressions:list[str] = extract_random_relevant_expressions(total_list)
    evaluation(total_list,relevant_expressions)


if __name__ == "__main__":
    main()
