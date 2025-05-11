import os
import matplotlib.pyplot as plt

##################################################################
# Stop Words Our Algorithm
###################################################################



# syllable_counter
EXCEPTIONS = {
    "cafe": 2,
    "resume": 2,
    "fiance": 2,
    "cliche": 2,
    # add more known exceptions here
}

def count_syllables(word: str) -> int:
    """
    Estimate English syllable count by:
      0) overriding via EXCEPTIONS map if present
      1) collapsing true diphthongs into a placeholder '1'
      2) counting every vowel or placeholder as one syllable
      3) dropping a silent final 'e' (but not in words ending 'le' or exceptions)
    """
    w = word.lower().strip()

    # 0) exception override
    if w in EXCEPTIONS:
        return EXCEPTIONS[w]

    # 1) collapse true diphthongs into placeholder '1'
    for d in ("ai", "au", "ae", "oi", "ou", "ow"):
        w = w.replace(d, "1")

    # 2) count each remaining vowel or placeholder
    accented = "áéíóúãõâêô"
    vowels = set("aeiou") | set(accented)
    count = sum(1 for ch in w if ch == "1" or ch in vowels)

    # 3) drop silent final 'e' (but not for 'le' endings or exceptions)
    if w.endswith("e") and not w.endswith("le") and word.lower() not in EXCEPTIONS and count > 1:
        count -= 1

    return max(1, count)


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
def find_elbow(neigsyl_dict: dict[str, float], delta_k=4, target_slope=-1.0, tolerance=0.1) -> list[str]:
    """
    Use the elbow method to identify stopwords by analyzing the slope of the NeigSyl score curve.

    Parameters:
    neigsyl_dict (dict[str, float]): Words and their NeigSyl scores.
    delta_k (int): Distance between points to calculate slope.
    target_slope (float): The slope you're trying to detect (default -1.0).
    tolerance (float): Acceptable deviation from the target slope (default 0.1).

    Returns:
    list[str]: List of identified stopwords.
    """
    sorted_items = sorted(neigsyl_dict.items(), key=lambda x: -x[1])
    values = [val for _, val in sorted_items]

    for r in range(len(values) - delta_k):
        slope = (values[r + delta_k] - values[r]) / delta_k
        if abs(slope - target_slope) < tolerance:
            return [word for word, _ in sorted_items[:r + delta_k]]

    return [word for word, _ in sorted_items]


# Plot the neigsyl_curve
def plot_neigsyl_curve(neigsyl_dict: dict[str, float],plot_name:str):
    sorted_scores = sorted(neigsyl_dict.values(), reverse=True)
    plt.figure(figsize=(10, 5))
    plt.plot(sorted_scores, marker='o')
    plt.title("NeigSyl Score Curve")
    plt.xlabel("Words (sorted by NeigSyl)")
    plt.ylabel("NeigSyl Score")
    plt.grid(True)

    # Salva o gráfico
    # Caminho correto da pasta de plots
    PLOT_DIR = os.path.join("tests", "stop_words_plots")
    os.makedirs(PLOT_DIR, exist_ok=True)
    # Salva na pasta correta
    plot_path = os.path.join(PLOT_DIR, f"{plot_name}_neigsyl_plot.png")
    plt.savefig(plot_path)
    plt.close()


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
  stop_words: list[str] = find_elbow(neigsyl_scores, delta_k=5,target_slope=-0.8,tolerance=0.05)

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