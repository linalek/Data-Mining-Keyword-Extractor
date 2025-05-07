from src.text_processing import preprocess_text
from src.ngram import build_ngram_dict
from src.cohesion_metrics import calculate_cohesion
from src.stopwords import get_stopwords

def main():
    text = "Exemplo de texto para análise."
    
    # Pré-processamento
    tokens = preprocess_text(text)
    
    # Stopwords (se necessário)
    stop_words = get_stopwords()
    tokens = [t for t in tokens if t not in stop_words]

    # Construção de n-gramas
    ngram_dict = build_ngram_dict(tokens, n=2)

    # Cálculo de métrica de coesão
    for ngram, obj in ngram_dict.items():
        cohesion = calculate_cohesion(obj)
        print(f"{ngram} -> Cohesion: {cohesion}")

if __name__ == "__main__":
    main()
