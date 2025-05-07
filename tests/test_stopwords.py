from src.text_processing import read_text_files
from src.stopwords import get_stop_words,get_nltk_stopwords_in_corpus



######################################### Test1 ########################################
corpus:dict[str:str] = read_text_files("./data/corpus2mw")
stop_words:list[str] = get_stop_words(corpus)
print(len(stop_words))
print(stop_words)

# NLTK
nltk_stopwords_found = get_nltk_stopwords_in_corpus(corpus)

print(f"Number of stopwords found (NLTK): {len(nltk_stopwords_found)}")
print("Stopwords found:")
print(nltk_stopwords_found)

######################################### Test 2 ########################################
print("\n\n\n\n\n")
corpus1:dict[str:str] = {"text":"Although the weather was cold and the wind was strong, the children decided to go outside and play in the snow until they became tired and returned home."}
stop_words:list[str] = get_stop_words(corpus1)
print(len(stop_words))
print(stop_words)

# NLTK
nltk_stopwords_found = get_nltk_stopwords_in_corpus(corpus1)

print(f"Number of stopwords found (NLTK): {len(nltk_stopwords_found)}")
print("Stopwords found:")
print(nltk_stopwords_found)

######################################### Test 3 ########################################
print("\n\n\n\n\n")
corpus2:dict[str:str] = {"text":"When the old professor entered the lecture hall and saw that the students had already taken their seats, he smiled, adjusted his glasses, and walked to the front of the room before beginning to explain the complex theory that would challenge their understanding of physics more than anything they had studied so far."}
stop_words:list[str] = get_stop_words(corpus2)
print(len(stop_words))
print(stop_words)

# NLTK
nltk_stopwords_found = get_nltk_stopwords_in_corpus(corpus2)

print(f"Number of stopwords found (NLTK): {len(nltk_stopwords_found)}")
print("Stopwords found:")
print(nltk_stopwords_found)
