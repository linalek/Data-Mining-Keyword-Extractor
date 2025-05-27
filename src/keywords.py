from text_processing import read_text_files,tokenize_text
import math

def get_explicit_keywords(corpus_path: str,relevant_expressions: list[str],total_keywords: int,stop_words: list[str]) -> dict[str, list[str]]:
  """
  For each document in the corpus:
      1) Tokenizes the text.
      2) Calculates TF-IDF scores for unigrams and relevant expressions (REs).
      3) Selects top-K keywords (half from unigrams, half from REs).

  Args:
      corpus_path (str): Path to the corpus directory.
      relevant_expressions (List[str]): Predefined list of relevant expressions (REs).
      total_keywords (int): Total number of keywords to extract per document.
      stop_words (List[str]): List of stopwords to ignore.

  Returns:
      Dict[str, List[str]]: Mapping of {filename: [keyword1, ..., keywordN]}.
  """

  # 1) Load all documents
  text_files: dict[str, str] = read_text_files(corpus_path)
  num_docs: int = len(text_files)
  num_res: int = total_keywords // 2
  num_unigrams: int = total_keywords - num_res

  df_unigrams: dict[str, int] = {}
  df_res: dict[str, int] = {}
  doc_tokens: dict[str, list[str]] = {}
  doc_re_matches: dict[str, list[str]] = {}

  # 2) Calculate Document Frequencies
  for fname, text in text_files.items():
      tokens: list[str] = tokenize_text(text)
      doc_tokens[fname] = tokens

      unique_unigrams: set[str] = set(w for w in tokens if w.lower() not in stop_words)
      for w in unique_unigrams:
          df_unigrams[w] = df_unigrams.get(w, 0) + 1

      matched:list[str] = [expr for expr in relevant_expressions if expr in text]
      doc_re_matches[fname] = matched
      for expr in set(matched):
          df_res[expr] = df_res.get(expr, 0) + 1

  results: dict[str, list[str]] = {}

  for fname, tokens in doc_tokens.items():
      total_terms:int = len(tokens)

      # Term frequency (excluding stopwords)
      counts: dict[str, int] = {}
      for w in tokens:
          if w.lower() in stop_words:
              continue
          counts[w] = counts.get(w, 0) + 1

      # 3.1) TF-IDF for unigrams
      tfidf_unigrams: dict[str, float] = {}
      for w, cnt in counts.items():
          tf = cnt / total_terms
          idf = math.log(num_docs / df_unigrams[w]) if df_unigrams[w] > 0 else 0.0
          tfidf_unigrams[w] = tf * idf

      # 3.2) TF-IDF for relevant expressions
      tfidf_res: dict[str, float] = {}
      doc_text = text_files[fname]
      for expr in doc_re_matches[fname]:
          cnt:int = doc_text.count(expr)
          tf:float = cnt / total_terms
          idf:float = math.log(num_docs / df_res[expr]) if df_res[expr] > 0 else 0.0
          tfidf_res[expr] = tf * idf

      # 3.3) Select top keywords
      top_unigrams: list[tuple[str, float]] = sorted(tfidf_unigrams.items(), key=lambda x: -x[1])[:num_unigrams]
      top_res: list[tuple[str, float]] = sorted(tfidf_res.items(), key=lambda x: -x[1])[:num_res]

      keywords: list[str] = [term for term, _ in (top_res + top_unigrams)]
      results[fname] = keywords

  return results

def calculate_implicit_keywords(corpus_path: str,explicit_keywords: dict[str, list[str]],relevant_expressions: list[str],num_implicit: int,stop_words: set[str]) -> dict[str, list[str]]:
  """
  Calculate implicit keywords for a set of documents based on their semantic proximity
  to a given list of explicit keywords.

  This function processes a text corpus to identify additional, non-explicit keywords 
  that are semantically related to given explicit keywords using co-occurrence statistics 
  and intra-document proximity measures. It returns the top N implicit keywords for each document.

  Parameters:
      corpus_path (str): Path to the corpus containing text documents.
      explicit_keywords (Dict[str, List[str]]): A dictionary mapping document names to lists of explicit keywords.
      relevant_expressions (List[str]): List of relevant multi-word expressions to consider.
      num_implicit (int): Number of top implicit keywords to return per document.

  Returns:
      Dict[str, List[str]]: A dictionary mapping each document to a list of top implicit keywords.
  """

  # Read and tokenize all documents in the corpus
  text_files: dict[str, str] = read_text_files(corpus_path)
  doc_tokens: dict[str, list[str]] = {fname: tokenize_text(text.lower()) for fname, text in text_files.items()}
  num_docs:int = len(text_files)

  # Gather all unique unigrams and multi-word expressions
  all_unigrams: set[str] = set()
  for tokens in doc_tokens.values():
      all_unigrams.update(tokens)
  all_terms: list[str] = list(all_unigrams.union(set(relevant_expressions)))

  # Step 1: Compute P(A, .) for each term (mean relative frequency across all documents)
  p_a_dot: dict[str, float] = {}
  for term in all_terms:
      total_prob:float = 0.0
      for fname, tokens in doc_tokens.items():
          text:str = text_files[fname].lower()
          total_words:int = len(tokens)
          # Use count in tokens if unigram, otherwise count in text
          if term in all_unigrams:
              freq:int = tokens.count(term)
          else:
              freq:int = text.count(term.lower())
          total_prob += freq / total_words if total_words > 0 else 0
      p_a_dot[term] = total_prob / num_docs

  # Step 2: Compute semantic proximity between all term pairs
  sem_prox: dict[tuple[str, str], float] = {}
  for i, term_a in enumerate(all_terms):
      for term_b in all_terms[i+1:]:
          pair: tuple[str, str] = tuple(sorted((term_a, term_b)))
          co_docs: list[str] = []

          # Identify documents containing both term_a and term_b
          for fname in text_files:
              tokens: list[str] = doc_tokens[fname]
              text:str = text_files[fname].lower()
              in_a:bool = term_a in tokens if term_a in all_unigrams else term_a.lower() in text
              in_b:bool = term_b in tokens if term_b in all_unigrams else term_b.lower() in text
              if in_a and in_b:
                  co_docs.append(fname)

          if not co_docs:
              sem_prox[pair] = 0.0
              continue

          # Compute inter-document correlation
          cov = var_a = var_b = 0.0
          for fname in text_files:
              tokens: list[str] = doc_tokens[fname]
              text:str = text_files[fname].lower()
              total_words:int = len(tokens)
              p_a:float = tokens.count(term_a) / total_words if term_a in all_unigrams else text.count(term_a.lower()) / total_words
              p_b:float = tokens.count(term_b) / total_words if term_b in all_unigrams else text.count(term_b.lower()) / total_words
              cov += (p_a - p_a_dot[term_a]) * (p_b - p_a_dot[term_b])
              var_a += (p_a - p_a_dot[term_a]) ** 2
              var_b += (p_b - p_a_dot[term_b]) ** 2

          var_a = math.sqrt(var_a / num_docs)
          var_b = math.sqrt(var_b / num_docs)
          corr:float = cov / (var_a * var_b) if var_a > 0 and var_b > 0 else 0.0

          # Compute intra-document proximity (based on token distance)
          ip_sum:float = 0.0
          for fname in co_docs:
              tokens:list[str] = doc_tokens[fname]
              positions_a, positions_b = [], []
              for i in range(len(tokens)):
                  # Locate positions of term_a
                  if term_a in all_unigrams and tokens[i] == term_a:
                      positions_a.append(i)
                  elif term_a not in all_unigrams and ' '.join(tokens[i:i+len(term_a.split())]) == term_a.lower():
                      positions_a.append(i)
                  # Locate positions of term_b
                  if term_b in all_unigrams and tokens[i] == term_b:
                      positions_b.append(i)
                  elif term_b not in all_unigrams and ' '.join(tokens[i:i+len(term_b.split())]) == term_b.lower():
                      positions_b.append(i)

              # Compute normalized minimum distance between terms
              if positions_a and positions_b:
                  min_dist:float = min(abs(a - b) for a in positions_a for b in positions_b)
                  max_dist:float = max(abs(a - b) for a in positions_a for b in positions_b)
                  if max_dist > 0:
                      ip_sum += 1 - (min_dist / max_dist)
          ip:float = ip_sum / len(co_docs)
          sem_prox[pair] = corr * math.sqrt(ip) if ip > 0 else 0.0

  # Step 3: For each document, select top implicit keywords based on semantic proximity to explicit ones
  results: dict[str, list[str]] = {}
  for fname, explicit in explicit_keywords.items():
      explicit_lower: list[str] = [e.lower() for e in explicit]
      tokens:list[str] = doc_tokens[fname]
      text:str = text_files[fname].lower()

      # Filter out terms that are explicit, stopwords, or too short
      candidates: list[str] = []
      for term in all_terms:
          term_lower:str = term.lower()
          if (
              term_lower in explicit_lower or
              term_lower in stop_words or
              len(term_lower) <= 2
          ):
              continue
          if term in all_unigrams and term_lower not in tokens:
              candidates.append(term)
          elif term not in all_unigrams and term_lower not in text:
              candidates.append(term)

      # Score candidates by their proximity to explicit keywords (weighted by inverse position)
      scores: dict[str, float] = {}
      for cand in candidates:
          score:float = 0.0
          for i, exp in enumerate(explicit, 1):
              key: tuple[str, str] = tuple(sorted((cand, exp)))
              score += sem_prox.get(key, 0.0) / i
          scores[cand] = score

      # Select top-N implicit keywords
      top_implicit: list[tuple[str, float]] = sorted(scores.items(), key=lambda x: -x[1])[:num_implicit]
      results[fname] = [term for term, _ in top_implicit]

  return results