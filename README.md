# PAD_Project2

## About the Project

This project implements an algorithm designed to process and analyze text data by removing stopwords and performing linguistic analysis. The algorithm is built to be efficient and modular, allowing for easy integration into larger text processing pipelines. It leverages Python for its simplicity and robust library ecosystem.

## Setting Up the Environment

To get started with this project, follow these steps to set up your environment:

1. **Create a Virtual Environment**  
   Create a virtual environment to isolate project dependencies:
   ```
   python -m venv venv
   ```

2. **Activate the Virtual Environment**  
   Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

3. **Install Dependencies**  
   Install the required dependencies listed in `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```

## Tests
To run the tests, ensure you are in the root folder `PAD_Project2`. For example, to run the `test_stopwords` test located in the `tests` folder, execute:
```
python -m tests.test_stopwords
```
To run any other test, replace `test_stopwords` with the name of the desired test file in the `tests` folder, using the format `python -m tests.<test_name>`.

## Running the Main Extraction Algorithm

To run the main extraction pipeline on a specific corpus, follow these steps:

1. **Prepare your corpus**  
   Ensure that your corpus is a folder containing plain text files. Each file should represent one document. The algorithm will process all files within the folder.

2. **Set the corpus path**  
   Open the `main.py` file and locate the `extractor()` function call inside the `main()` function. Replace the argument of the `extractor()` with the path to your corpus folder. For example:
   ```python
   extractor("path/to/your/corpus")
   ``` 

3. **Run the main script**
   Once the corpus path is correctly set, execute the main script from the root of the project using:
   ```python main.py```