import os
import re

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
    # Add spaces around "." in all other cases, including end of line or document.
    spaced_text = re.sub(r'(?<!\d)(?<!\b[A-Za-z])\.(?!\d)(?![A-Za-z]\b)', ' . ', spaced_text)

    punctuations = r"([;:!?,<>&\)\(\]\[])"
    spaced_text = re.sub(punctuations, r" \1 ", spaced_text)
    # Delete useless spaces
    spaced_text = re.sub(r"\s+", " ", spaced_text)
    return spaced_text.strip()

# Function to tokenize the text
def tokenize_text(text: str) -> list[str]:
    """
    Generate a list of tokens from the text.
    Parameters: text (str): the text to tokenize.
    Returns: tokens (list): a list of tokens (punctuation are also considered as tokens).
    """
    tokens = text.split()  # Divide the text into tokens based on whitespace hence the addition of spaces around punctuation marks
    return tokens

# Function to process all text files in a given corpus path in reading order
def text_processing(corpus_path: str) -> list[str]:
    """
    Process all text files in a given corpus path in reading order.
    Parameters:
        corpus_path (str): Path to the folder containing text files.
    Returns:
        list[str]: A list of tokens from all files, in reading order.
    """
    # Read the text files
    text_files: dict = read_text_files(corpus_path)

    # Sort the files by key (file name)
    sorted_text_files = dict(sorted(text_files.items()))

    # Initialize a list for the tokens
    tokenized_text: list[str] = []

    # Process each file in sorted order
    for text in sorted_text_files.values():
        spaced_text: str = add_spaces(text)  # Add spaces around punctuation marks
        tokenized_text.extend(tokenize_text(spaced_text))  # Tokenize and add to the list

    return tokenized_text