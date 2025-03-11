import re
from collections import Counter

def analyze_text(text):
    """
    Analizuje tekst i zwraca statystyki, takie jak liczba słów i częstotliwość występowania słów.

    Args:
        text (str): Tekst do analizy.

    Returns:
        dict: Słownik zawierający statystyki tekstu.
    """
    word_count = len(re.findall(r'\w+', text))
    word_frequency = Counter(re.findall(r'\w+', text.lower()))
    return {
        "word_count": word_count,
        "word_frequency": dict(word_frequency)
    }

# Przykładowe użycie
if __name__ == "__main__":
    sample_text = "To jest przykładowy tekst do analizy. Przykładowy tekst zawiera kilka słów."
    analysis_result = analyze_text(sample_text)
    print(analysis_result)