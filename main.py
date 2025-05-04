##################################################################
# N-gram class
###################################################################
class n_gram:
  size:int = 0
  frequency:int = 0
  tokens:list[str] = []
  glue_n_grams_minus_1:dict = {}
  glue_n_grams_plus_1:dict = {}

  #Constructor
  def __init__(self,size:int, frequency:int, tokens:list[str]) -> None:
    self.size = size
    self.frequency = frequency
    self.tokens = tokens

  #Getters and Setters
  def get_size(self) -> int:
    return self.size
  def set_size(self,size:int) -> None:
    self.size = size

  def get_frequency(self) -> int:
    return self.frequency
  def set_frequency(self, frequency:int) -> None:
    self.frequency = frequency

  def get_tokens(self) -> list[str]:
    return self.tokens
  def set_tokens(self, tokens:list[str]) -> None:
    self.tokens = tokens

  def get_glue_n_grams_minus_1(self) -> dict:
    return self.glue_n_grams_minus_1
  def set_glue_n_grams_minus_1(self, glue_n_grams_minus_1:dict) -> None:
    self.glue_n_grams_minus_1 = glue_n_grams_minus_1
  def add_glue_n_grams_minus_1(self, key:str, value:float) -> None:
    self.glue_n_grams_minus_1[key] = value

  def get_glue_n_grams_plus_1(self) -> dict:
    return self.glue_n_grams_plus_1
  def set_glue_n_grams_plus_1(self, glue_n_grams_plus_1:dict) -> None:  
    self.glue_n_grams_plus_1 = glue_n_grams_plus_1
  def add_glue_n_grams_plus_1(self, key:str, value:float) -> None:
    self.glue_n_grams_plus_1[key] = value

  # Methods
  # This method is used to compute the glue of the n-gram.
  def glue(self, glue_function: str, all_n_grams: dict, total_count: int = None) -> float:
    """
    Compute the glue of the n-gram.
    Parameters:
        self: The n-gram to compute the glue for.
        glue_function (str): The glue function to use ("scp", "dice", "mi").
    Returns: float: The computed glue value.
    """
    if glue_function == "scp":
        return scp_glue(self, all_n_grams, total_count)
    elif glue_function == "dice":
        return dice_glue(self, all_n_grams)
    elif glue_function == "mi":
        return mi_glue(self, all_n_grams, total_count)
    else:
        return 0.0

##################################################################
# Function to create n-grams from a list of tokens
###################################################################

def create_n_grams(tokens:list[str], stop_words:list[str]) -> dict[str,n_gram]:
  n_grams:dict[str,n_gram] = {} # dictionary to store all n-grams
  l_list:int = len(tokens) # length of the list of tokens

  # cycle through all the tokens 
  for index in range(l_list):
    # foreach token we can have until 8 n-grams
    for size in range(2,9):
      if index+size > l_list-1:
        break
      
      # Check if the first or last tokens in the n-gram are a stop_word because this is forbiden
      if(tokens[index] in stop_words):
        break
      if(tokens[index+size-1] in stop_words):
        continue
      
      # Transform our list of tokens in our key of type string for the dictionary
      key:str = " ".join(tokens[index:index+size])
      
      # If the n-gram already exist we only add 1 to their frequency
      if key in n_grams:
        n_grams[key].set_frequency(n_grams[key].get_frequency()+1)
      else: # if not we create  this new n-gram and store it in the dict
        n_grams[key] = n_gram(size,1,tokens[index:index+size])

  return n_grams

import os
import re
from collections import Counter

##################################################################
# These functions are used to read text files from a directory and tokenize the text.
###################################################################

# Function to read text files from a corpus directory
def read_text_files(directory_path: str) -> dict:
    """
    Read all the files in a given directory
    Parameters: directory_path (str): Path to the corpus containing the text files.
    Returns: text_files_content (dict): A dictionary where keys are filenames and values are the file contents as string.
    """
    text_files_content = {} # Dictionary to store the content
    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # Only read files, so we check if it's a file and not a folder
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                text_files_content[filename] = file.read()
    return text_files_content

# Function to add spaces around punctation mark: ";", ":", "!", "?", "<", ">", "&", ")", "(", "]", "[", "."
def add_spaces(text : str) -> str:
    """
    Add a space before and after punctuation marks in the text.
    Parameters: text (str): the text to process.
    Returns: spaced_text (str): the text with spaces added around punctuation marks.

    NOTE: We must have a special case for the punctuation "." 
    """
    # We use regex to add spaces around punctuation marks: re.sub(pattern, replacement, string)

    # Special case for the punctuation "."
    # Decimal numbers
    spaced_text = re.sub(r'(?<=\d)\.(?=\d)', '.', text)
    # Acronyms
    spaced_text = re.sub(r'(?<=\b[A-Za-z])\.(?=[A-Za-z]\b)', '.', spaced_text) 
    # All other cases, we add spaces around "."
    spaced_text = re.sub(r'\. ', ' . ', spaced_text)
    ## We do not make the difference with the last dot of an acronym and the dot to end the sentence

    punctuations = r"([;:!?,<>&\)\(\]\[])"
    spaced_text = re.sub(punctuations, r" \1 ", spaced_text)
    # Delete useless spaces
    spaced_text = re.sub(r"\s+", " ", spaced_text)
    return spaced_text.strip()


# Function to tokenize the text
def tokenize_text(text: str) -> list:
    """
    Generate a list of tokens from the text.
    Parameters: text (str): the text to tokenize.
    Returns: tokens (list): a list of tokens (punctuation are also considered as tokens).
    """
    tokens = text.split()  # Divide the text into tokens based on whitespace hence the addition of spaces around punctuation marks
    return tokens

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

#############################################################
# These functions are used to compute metrics on the tokens to use in the LocalMaxs extractor.
#############################################################

# Function to return the n-gram given a list of tokens.
def get_element(tokens: list[str], all_n_grams: dict[str,n_gram])-> n_gram:
    """
    Get the ngram object corresponding to the tokens in my dictionary of n-grams.
    Parameters:
        tokens (list): A list of tokens.
        all_n_grams (dict): A dictionary containing all n-grams
    Returns: n_gram (n_gram): The n-gram object corresponding to the tokens."""
    for key, ngram in all_n_grams.items():
        if ngram.get_tokens() == tokens:
            return ngram
    return None


def calculate_and_store_glue(all_n_grams: dict[str,n_gram], glue_function: str) -> dict:
    """
    Compute the glue of n-grams and store them in a dictionary.
    Parameters:
        all_n_grams (dict): A dictionary containing all n-grams.
        glue_function (str): The glue function to use ("scp", "dice", "mi").
    """
    ngrams = list(all_n_grams.keys())
    total_count = len(ngrams)
    
    # Compute the glue for each n-gram
    for ngram in ngrams:
        w = all_n_grams[ngram]
        g = w.glue(glue_function, all_n_grams, total_count)

        n = w.get_size()
        if n>2: # It must be more than a bigram to compute the glue
          to_update1 = w.get_tokens()[:n-1]
          to_update2 = w.get_tokens()[1:n]

          ngram1 = get_element(to_update1, all_n_grams)
          # Get the key of the ngram1
          ngram_key1 = " ".join(to_update1)
          ngram2 = get_element(to_update2, all_n_grams)
          # Get the key of the ngram2
          ngram_key2 = " ".join(to_update2)

          # Check if ngram1 and ngram2 are in all_n_grams
          if ngram1 is not None and ngram2 is not None:
            # Update the glue of ngram1 and ngram2
            g1 = all_n_grams[ngram_key1].glue(glue_function, all_n_grams, total_count)
            g2 = all_n_grams[ngram_key2].glue(glue_function, all_n_grams, total_count)
          else:
            print("ngram1 or ngram2 not found in all_n_grams") # Debugging line

          # Update the sets of glue
          if w.get_size() == 2:
            # We don't need to update the glue of (n-1)grams because we don't use them.
            # Set of glue of (n+1)grams to update
            if ngram1 is not None:
              w.add_glue_n_grams_minus_1(ngram_key1, g1)
            if ngram2 is not None:
              w.add_glue_n_grams_minus_1(ngram_key2, g2)
            
          if w.get_size() >=3 and all_n_grams[ngram].get_size() <= 7:

            # Set of glue of (n-1)grams to update
            if ngram1 is not None:
              ngram1.add_glue_n_grams_plus_1(ngram, g)
            if ngram2 is not None:
              ngram2.add_glue_n_grams_plus_1(ngram, g)
            
            # Set of glue of (n+1)grams to update
            if ngram1 is not None:
              w.add_glue_n_grams_minus_1(ngram_key1, g1)
            if ngram2 is not None:
              w.add_glue_n_grams_minus_1(ngram_key2, g2)
            
          if w.get_size() == 8:
            # We don't need to update the glue of (n+1)grams because we don't use them.
            # Set of glue of (n-1)grams to update
            if ngram1 is not None:
              ngram1.add_glue_n_grams_plus_1(ngram, g)
            if ngram2 is not None:
              ngram2.add_glue_n_grams_plus_1(ngram, g)    
