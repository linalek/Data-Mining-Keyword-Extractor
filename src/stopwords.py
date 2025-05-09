##################################################################
# Stop Words Our Algorithm
###################################################################

#silabas = #vowels - #2*vowels in a row
# se a palavra tiver um acento em alguma vowel não subtrai

# Count syllables
def count_syllables(word: str) -> int:
  """
  Count the number of syllables in a given word based on vowel sequences.

  This function counts the number of syllables by detecting sequences of vowels in the word. 
  It considers the vowels 'aeiouáéíóúãõâêô' (including accented and special characters). 
  The function works by iterating through each character in the word and counting the transitions 
  between consonants and vowel sequences as a new syllable.

  Parameters:
  word (str): The word whose syllables are to be counted.

  Returns:
  int: The total number of syllables in the word.
  """

  vowels:str = "aeiou" # List of vowels
  accent_vowels:str = "áéíóúãõâêô" # List of accent vowels
  
  word = word.lower()
  syllables:int = 0
  in_vowel_sequence:bool = False # Check if we are already in a sequence of vowels
  
  for char in word:
      if char in vowels:
          # If we are not already in a sequence of vowels, we start a new sequence
          if not in_vowel_sequence:
              syllables += 1
              in_vowel_sequence = True
      else:
          # If we find a consonant, the sequence of vowels is finished
          in_vowel_sequence = False
  
  return syllables

# Extract bigrams and count the frequency
def extract_bigram_neighbors(texts: list[str]) -> dict[str, int]:
  """
  Extracts bigrams (pairs of consecutive words) from the given texts and counts 
  the number of unique neighbors for each word in the bigrams.
  
  Parameters:
  texts (list[str]): List of text strings to analyze
  
  Returns:
  dict[str, int]: A dictionary where the keys are words, and the values are 
                  the number of unique neighboring words (words that appear before 
                  or after the word in the bigrams).
  """

  # Dictionary to store words and their unique neighbors
  word_neighbors: dict[str, set[str]] = {}

  for text in texts:
      # Clean and split the phrases into words
      words:list[str] = [w.lower().strip(".,!?;:\"'()[]") for w in text.split()]
      # Iterate over the list of words to create bigrams (pairs of consecutive words)
      for i in range(len(words) - 1):
          w1, w2 = words[i], words[i + 1] # Two consecutive words

          # Ensure each word is in the dictionary and initialize its neighbor set if not already present
          if w1 not in word_neighbors:
              word_neighbors[w1] = set()
          if w2 not in word_neighbors:
              word_neighbors[w2] = set()

          # Add each word to the other's set of neighbors (bidirectional relationship)
          word_neighbors[w1].add(w2)  # w1 precede w2
          word_neighbors[w2].add(w1)  # w2 sucede w1

  # Return a dictionary where each word is mapped to the number of unique neighbors (words that appear before or after it in the bigrams)
  return {word: len(neighbors) for word, neighbors in word_neighbors.items()}

# Calculate NeigSyl(w)
def compute_neigsyl(words: set[str], bigram_freqs: dict[str, int]) -> dict[str, float]:
  """
  Compute the NeigSyl score for each word based on its bigram frequency and syllable count.

  This function calculates the NeigSyl score for each word, which is defined as the ratio of 
  the word's bigram frequency to its syllable count. The bigram frequency represents the number 
  of neighboring words that appear before or after the word, and the syllable count is obtained 
  using the `count_syllables` function.

  Parameters:
  words (set[str]): A set of words for which NeigSyl scores will be computed.
  bigram_freqs (dict[str, int]): A dictionary where keys are words and values are their bigram frequencies.

  Returns:
  dict[str, float]: A dictionary where keys are words and values are their corresponding NeigSyl scores.
  """

  neigsyl:dict[str:float] = {}
  for word in words:
      neig = bigram_freqs.get(word, 0)
      syll = count_syllables(word)
      if syll > 0:  # evitar divisão por zero
          neigsyl[word] = neig / syll
  return neigsyl

# Elbow method
def find_elbow(neigsyl_dict: dict[str, float], delta_k=4) -> list[str]:
  """
  Use the elbow method to identify stopwords by analyzing the slope of the NeigSyl score curve.

  This function sorts words by their NeigSyl scores in descending order, then computes the slope 
  between consecutive NeigSyl values. The stopwords are determined by identifying a "knee" 
  in the curve, where the slope becomes approximately -1. This is interpreted as a change 
  in the nature of the words from frequent and informative to less frequent and less informative.

  Parameters:
  neigsyl_dict (dict[str, float]): A dictionary where keys are words and values are their NeigSyl scores.
  delta_k (int, optional): The number of positions to look ahead for slope calculation, default is 4.

  Returns:
  list[str]: A list of words identified as stopwords based on the elbow method.
  """

  # Sort NeigSyl values ​​in descending order
  sorted_items:list[tuple[str, float]] = sorted(neigsyl_dict.items(), key=lambda x: -x[1])
  values:list[float] = [val for _, val in sorted_items]
  
  # Iterate over the values ​​to calculate the slope
  for r in range(len(values) - delta_k):
      # Calculate slope: (NeigSyl(r + delta_k) - NeigSyl(r)) / delta_k
      slope:float = (values[r + delta_k] - values[r]) / delta_k
      # Check if the slope is approximately -1 (tolerance to avoid numerical problems)
      if abs(slope + 1) < 0.1:  # Tolerance of 0.1 for proximity to -1
          stopwords:list[str] = [word for word, _ in sorted_items[:r + delta_k]]
          return stopwords

  # Return all words if dot is not found
  return [word for word, _ in sorted_items]

# Stop Words
def get_stop_words(corpus:dict) -> list[str]:
  """
  Identify and return a list of stopwords from a given corpus using the NeigSyl elbow method.

  This function processes the corpus to extract all unique words, computes their bigram frequencies,
  calculates the NeigSyl scores for each word, and then identifies stopwords using the elbow method.
  The stopwords are those words with the smallest change in NeigSyl values, which correspond 
  to less informative and more frequent words.

  Parameters:
  corpus (dict): A dictionary where keys are document identifiers and values are the text content.

  Returns:
  list[str]: A list of identified stopwords based on the NeigSyl elbow method.
  """

  all_words:set[str] = set() # Set to hold all unique words in the corpus
  for text in corpus.values():
      for word in text.split():
          clean:str = word.lower().strip(".,!?;:\"'()[]")
          if clean:
              all_words.add(clean)
  # Extract bigram frequencies from the corpus
  bigram_freqs: dict[str, int] = extract_bigram_neighbors(corpus.values())
  # Compute NeigSyl scores for all words
  neigsyl_scores: dict[str, float] = compute_neigsyl(all_words, bigram_freqs)
  # Identify stopwords using the elbow method
  stop_words: list[str] = find_elbow(neigsyl_scores, delta_k=4)

  return stop_words


##################################################################
# Stop Words Python Library Algorithm
###################################################################
import nltk
from nltk.corpus import stopwords

# Download stopwords if needed
nltk.download('stopwords')

# Get stopwords in English
nltk_stop_words = set(stopwords.words('english'))

# Function to count and return the stopwords found in the corpus
def get_nltk_stopwords_in_corpus(corpus: dict) -> list:
  """
  Identify and return a list of stopwords present in a given corpus using the NLTK stopwords list.

  This function processes the corpus to extract all unique words, cleans and normalizes them,
  then finds the intersection between the words in the corpus and the NLTK stopwords list. 
  The function returns the stopwords from the corpus that are also found in the NLTK stopwords list.

  Parameters:
  corpus (dict): A dictionary where keys are document identifiers and values are the text content.

  Returns:
  list: A list of stopwords found in the corpus that are also present in the NLTK stopwords list.
  """
  words_in_corpus = set()
  
  for text in corpus.values():
      for word in text.split():
          clean = word.lower().strip(".,!?;:\"'()[]")
          if clean.isalpha():  # Consider only alphabetic words
              words_in_corpus.add(clean)
  
  # Find the stopwords present in the corpus
  found_stopwords = words_in_corpus.intersection(nltk_stop_words)
  
  return list(found_stopwords)