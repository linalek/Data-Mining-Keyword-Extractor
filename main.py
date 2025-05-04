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

  # get set glues functions

  # Methods

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