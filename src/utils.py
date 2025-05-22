import random
from src.ngram import n_gram  # Classe n_gram
import tkinter as tk
from tkinter import messagebox

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

##################################################################
# Why do we need to store the dict of every single glue value instead of just saving the max of that?
#############################################################
def calculate_and_store_glue(all_n_grams: dict[str, n_gram], glue_function: str, stop_words: list[str]) -> dict:
    """
    Compute the glue of n-grams and store them in a dictionary.
    Parameters:
        all_n_grams (dict): A dictionary containing all n-grams.
        glue_function (str): The glue function to use ("scp", "dice", "mi").
        stop_words (list[str]): List of stop words that n-grams cannot start or end with.
    """
    ngrams = list(all_n_grams.keys())
    total_count = len(ngrams)

    # Compute the glue for each n-gram
    for ngram in ngrams:
        w = all_n_grams[ngram]

        g = w.calculate_glue(glue_function, all_n_grams, total_count)
        w.set_glue(g)

        n = w.get_size()
        #print(n)
        if n > 2:  # It must be more than a bigram to compute the glue
            to_update1 = w.get_tokens()[:n - 1]
            to_update2 = w.get_tokens()[1:n]

            # Check if sub-n_grams start or end with stop words
            if to_update1[0] in stop_words or to_update1[-1] in stop_words:
                #print(f"Skipping sub-n_gram '{' '.join(to_update1)}' due to stop word restriction.")
                ngram1 = None
            else:
                ngram1 = get_element(to_update1, all_n_grams)

            if to_update2[0] in stop_words or to_update2[-1] in stop_words:
                #print(f"Skipping sub-n_gram '{' '.join(to_update2)}' due to stop word restriction.")
                ngram2 = None
            else:
                ngram2 = get_element(to_update2, all_n_grams)

            # Process only valid sub-n_grams
            if ngram1 is not None:
                # Get the key of the ngram1
                ngram_key1 = " ".join(to_update1)
                #print(ngram_key1)
                g1 = all_n_grams[ngram_key1].calculate_glue(glue_function, all_n_grams, total_count)
                w.add_glue_n_grams_minus_1(ngram_key1, g1)
                #print("glue ngram1")
                if w.get_size() >= 3 and all_n_grams[ngram].get_size() <= 7:
                    ngram1.add_glue_n_grams_plus_1(ngram, g)

            if ngram2 is not None:
                # Get the key of the ngram2
                ngram_key2 = " ".join(to_update2)
                #print(ngram_key2)
                g2 = all_n_grams[ngram_key2].calculate_glue(glue_function, all_n_grams, total_count)
                w.add_glue_n_grams_minus_1(ngram_key2, g2)
                #print("glue ngram2")
                if w.get_size() >= 3 and all_n_grams[ngram].get_size() <= 7:
                    ngram2.add_glue_n_grams_plus_1(ngram, g)
            
            if w.get_size() == 8:
                # We don't need to update the glue of (n+1)grams because we don't use them.
                if ngram1 is not None:
                    ngram1.add_glue_n_grams_plus_1(ngram, g)
                    #print("glue ngram1")
                if ngram2 is not None:
                    ngram2.add_glue_n_grams_plus_1(ngram, g)
    
    for ngram in ngrams:
        ng = all_n_grams[ngram]
        #Calculate the max for the minus1
        ng.set_max_glue_n_grams_minus_1(max(ng.get_glue_n_grams_minus_1().values())) if ng.get_glue_n_grams_minus_1() else ng.set_max_glue_n_grams_minus_1(0.0)
        #Calculate the max for the plus1
        ng.set_max_glue_n_grams_plus_1(max(ng.get_glue_n_grams_plus_1().values())) if ng.get_glue_n_grams_plus_1() else ng.set_max_glue_n_grams_plus_1(0.0)

    return all_n_grams

###################################### ASK ASK ASK THE PROFESSOR #####################################
# we need to create 8-grams or just 7-grams? if its 7-grams we need to change the values in create_n_grams funciton and calculate_and_store_glue
############################# ############################### ########################## ##############


#############################################################################
# Extract all the relevant expressions from the all_n_grams dictionary
#############################################################################
def extract_random_relevant_expressions(all_n_grams: dict[str, n_gram], size: int = 200) -> list[str]:
    """
    Extracts a random sample of relevant expressions from a dictionary of n-grams.
    The function filters n-grams marked as relevant expressions and returns a random
    sample of up to the specified size.
    
    Args:
        all_n_grams: A dictionary mapping strings to n_gram objects.
        size: The maximum number of expressions to return (default is 200).
    
    Returns:
        A list of randomly selected relevant expression strings.
    """
    # Extract all relevant expressions
    relevant_expressions: list[str] = [key for key, ng in all_n_grams.items() if ng.is_relevant_expression()]
    
    # Returns a random sample of up to size 200
    return random.sample(relevant_expressions, min(size, len(relevant_expressions)))

##############################################################################
# Function to ask the user if the relevant expression is correct or not
##############################################################################
def ask_is_RE(expression: str) -> bool:
    """
    Prompts the user to evaluate whether a given expression is relevant.
    Displays a dialog box asking the user to confirm if the expression is a relevant
    expression (RE) and returns their response as a boolean.
    
    Args:
        expression: The expression to be evaluated.
    
    Returns:
        True if the user confirms the expression is relevant, False otherwise.
    """
    root: tk.Tk = tk.Tk()
    root.withdraw()  # Hide the main window

    result: bool = messagebox.askyesno("Evaluation", f"Is this expression a RE? Answer True or False.\n\n{expression}")
    root.destroy()
    return result

