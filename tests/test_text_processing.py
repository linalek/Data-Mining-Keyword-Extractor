import os
from src.text_processing import read_text_files, add_spaces, tokenize_text, text_processing  

# Prepare a test environment with temporary files
test_dir = "test_corpus"
os.makedirs(test_dir, exist_ok=True)
with open(os.path.join(test_dir, "file1.txt"), "w", encoding="utf-8") as f:
    f.write("Hello! This is a test. There is 3.14 as a number.")
with open(os.path.join(test_dir, "file2.txt"), "w", encoding="utf-8") as f:
    f.write("This (is) another file: with tokens & punctuations!")

try:
    # Test the read_text_files function
    print("Testing read_text_files...")
    text_files = read_text_files(test_dir)
    assert len(text_files) == 2, "The number of files read is incorrect."
    assert "file1.txt" in text_files, "file1.txt is missing."
    assert "file2.txt" in text_files, "file2.txt is missing."
    print("read_text_files: OK")

    # Test the add_spaces function
    print("Testing add_spaces...")
    text = "Hello! This is a test. There is 3.14 as a number."
    expected = "Hello ! This is a test . There is 3.14 as a number ."
    result = add_spaces(text)
    assert result == expected, f"add_spaces failed: expected {expected}, got {result}"
    print("add_spaces: OK")

    # Test the tokenize_text function
    print("Testing tokenize_text...")
    text = "Hello ! This is a test ."
    expected = ["Hello", "!", "This", "is", "a", "test", "."]
    result = tokenize_text(text)
    assert result == expected, f"tokenize_text failed: expected {expected}, got {result}"
    print("tokenize_text: OK")

    # Test the text_processing function
    print("Testing text_processing...")
    result = text_processing(test_dir)
    expected_tokens = [
        "Hello", "!", "This", "is", "a", "test", ".", "There", "is", "3.14", "as", "a", "number", ".", 
        "This", "(", "is", ")", "another", "file", ":", "with", "tokens", "&", "punctuations", "!"
    ]
    assert result == expected_tokens, f"text_processing failed: expected {expected_tokens}, got {result}"
    print("text_processing: OK")

finally:
    # Clean up temporary files
    for file in os.listdir(test_dir):
        os.remove(os.path.join(test_dir, file))
    os.rmdir(test_dir)