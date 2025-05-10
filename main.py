from src.text_processing import text_processing,read_text_files, add_spaces, tokenize_text
from src.ngram import *
from src.stopwords import get_stop_words, get_nltk_stopwords_in_corpus
from src.utils import calculate_and_store_glue

def main():    
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

    # Glues updated in each n-gram
    ngram_dict2 = calculate_and_store_glue(ngram_dict, "dice", stop_words)
    print(ngram_dict2)


    s=0
    # 
    # # Computing cohesion
    # for ngram, obj in ngram_dict.items():
    #     cohesion = calculate_cohesion(obj)
    #     print(f"{ngram} -> Cohesion: {cohesion}")

if __name__ == "__main__":
    main()
