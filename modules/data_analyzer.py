from . import text_analyzer, image_analyzer

def analyze_data(data, data_type, file_path=None):
    """
    Koordynuje analizę danych w zależności od typu danych.

    Args:
        data: Dane do analizy (tekst lub inne).
        data_type (str): Typ danych ("text" lub "image").
        file_path (str, optional): Ścieżka do pliku, jeśli typem danych jest obraz.

    Returns:
        dict: Wyniki analizy lub komunikat o błędzie.
    """
    if data_type == "text":
        return text_analyzer.analyze_text(data)
    elif data_type == "image" and file_path:
        return image_analyzer.analyze_image(file_path)
    else:
        return {"error": "Unsupported data type or missing file_path"}

# Przykładowe użycie
if __name__ == "__main__":
    text_data = "Przykładowy tekst do analizy."
    image_file = "image.jpg"  # Zamień na istniejący plik obrazu

    text_result = analyze_data(text_data, "text")
    print("Text Analysis:", text_result)

    image_result = analyze_data(None, "image", image_file)
    print("Image Analysis:", image_result)