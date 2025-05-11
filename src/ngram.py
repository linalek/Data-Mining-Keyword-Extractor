from math import log2
from src.cohesion_metrics import scp_glue, dice_glue, mi_glue
##################################################################
# N-gram class
###################################################################
class n_gram:
  size:int = 0
  frequency:int = 0
  tokens:list[str] = []
  glue:float = 0.0
  glue_n_grams_minus_1:dict = {}
  glue_n_grams_plus_1:dict = {}
  max_glue_n_grams_minus_1:float = 0.0
  max_glue_n_grams_plus_1:float = 0.0
  relevant_expression:bool = False

  #Constructor
  def __init__(self,size:int, frequency:int, tokens:list[str]) -> None:
    self.size = size
    self.frequency = frequency
    self.tokens = tokens
    self.glue = 0.0
    self.glue_n_grams_minus_1 = {}
    self.glue_n_grams_plus_1 = {}
    self.max_glue_n_grams_minus_1 = 0.0
    self.max_glue_n_grams_plus_1 = 0.0
    self.relevant_expression = False

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

  def get_glue(self) -> float:
     return self.glue
  def set_glue(self,value:float) -> None:
     self.glue = value

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

  def get_max_glue_n_grams_minus_1(self) -> float:
    return self.max_glue_n_grams_minus_1
  def set_max_glue_n_grams_minus_1(self, value: float) -> None:
    self.max_glue_n_grams_minus_1 = value

  def get_max_glue_n_grams_plus_1(self) -> float:
    return self.max_glue_n_grams_plus_1
  def set_max_glue_n_grams_plus_1(self, value: float) -> None:
    self.max_glue_n_grams_plus_1 = value
  
  def is_relevant_expression(self) -> bool:
    return self.relevant_expression
  def set_relevant_expression(self, value: bool) -> None:
    self.relevant_expression = value

  # Methods
  # This method is used to compute the glue of the n-gram.
  def calculate_glue(self, glue_function: str, all_n_grams: dict, total_count: int = None) -> float:
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
  
  # This method is used to compute the local maximum of the n-gram.
  def localMax(self,p:float = 2) -> None:
      formula:float = ((self.get_max_glue_n_grams_minus_1()**p + self.get_max_glue_n_grams_plus_1()**p)/2)**(1/p)
      self.set_relevant_expression(self.get_glue() >= formula and self.get_frequency() > 2)
    

##################################################################
# Function to create n-grams from a list of tokens
###################################################################

def create_n_grams(tokens:list[str], stop_words:list[str]) -> dict[str,n_gram]:
  """
  Generate n-grams from a list of tokens, excluding stop words at the beginning or end of n-grams.

  This function creates n-grams (from size 1 to 7) by iterating through a list of tokens.
  It checks that no n-gram starts or ends with a stop word. If a stop word is encountered,
  the n-gram is either skipped or truncated. The function returns a dictionary where the keys
  are the n-grams (as strings) and the values are the corresponding n-gram objects.

  Parameters:
  tokens (list[str]): A list of tokens (words) from the text.
  stop_words (list[str]): A list of stop words that should not be present at the start or end of n-grams.

  Returns:
  dict[str, n_gram]: A dictionary where the keys are n-grams (as strings) and the values are the corresponding n-gram objects.
  """
  n_grams:dict[str,n_gram] = {} # dictionary to store all n-grams
  l_list:int = len(tokens) # length of the list of tokens

  # cycle through all the tokens 
  for index in range(l_list+1):
    # foreach token we can have until 8 n-grams
    for size in range(2,9):
      if index+size > l_list:
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
