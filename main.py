from src.text_processing import text_processing,read_text_files
from src.ngram import *
from src.stopwords import get_stop_words, get_nltk_stopwords_in_corpus
from src.utils import calculate_and_store_glue

def main():    
    # Pré-processamento
    #tokens:list[str] = text_processing("data/testCorpus")
    # d = read_text_files("data/testCorpus")
    # for text in d.values():
    #     text = add_spaces(text)
    # Stopwords
    #######################################################################################
    # Still using the python library due to the need of imporvement in our algorithm
    #######################################################################################
    stop_words:list[str] = get_nltk_stopwords_in_corpus(read_text_files("data/corpus2mw"))

    # Construção de n-gramas
    ngram_dict:dict[str:n_gram] = create_n_grams(tokens,stop_words)

    # Glues updated in each n-gram
    ngram_dict = calculate_and_store_glue(ngram_dict, "dice")

    s=0
    # 
    # # Cálculo de métrica de coesão
    # for ngram, obj in ngram_dict.items():
    #     cohesion = calculate_cohesion(obj)
    #     print(f"{ngram} -> Cohesion: {cohesion}")

if __name__ == "__main__":
    main()
