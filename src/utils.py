from src.ngram import n_gram  # Classe n_gram

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